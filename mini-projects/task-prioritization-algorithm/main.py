# Complete web app with improved sync using Todoist Sync API
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv
import os
import time
import requests
from threading import Thread

LABEL_WEIGHTS = {
	"people": 40,
	"ontime": 30,
	"complex": 25,
	"long": 20,
	"firm": 15,
	"sensitive": 10,
	"habits": 5,
	"soft": -5,
	"weekplan": 3,
	"backlock": 1,
}

def calculate_task_score(task):
	score = 0
	# Deadline urgency
	if task["due"]:
		try:
			due_date = datetime.fromisoformat(task["due"])
			days_left = (due_date - datetime.now()).days
			score += max(0, 100 - days_left * 10)
		except Exception:
			pass
	# Label weights
	for label in task["labels"]:
		score += LABEL_WEIGHTS.get(label.lower(), 0)
	# Inverse of progress (simulated using "progress=XX")
	progress = 0
	if task["description"] and "progress=" in task["description"]:
		try:
			progress = int(task.description.split("progress=")[1].split()[0])
		except Exception:
			pass
	score += (100 - progress) * 0.5
	return score




def get_api_token():
	load_dotenv()
	API_TOKEN: str | None = os.getenv('TODOIST_TOKEN')
	assert API_TOKEN, "Loading Token Failed"
	return API_TOKEN

app = FastAPI()
API_TOKEN = get_api_token()
templates = Jinja2Templates(directory="templates")

# In-memory cache
SYNC_CHECK_INTERVAL_SEC = 30
sync_state = {
	"sync_token": "*",
	"last_sync": None,
	"last_sync_check": None,
}
cached_data = {
	"projects": {}, # id -> projects
	"tasks": {}, # id -> [task, score]
	"ordered_projects": [],
	"ordered_tasks": [], # [task, score]
}

EXCLUDED_LABELS = ["habits", "______end:______"]

def get_sync_data() -> Dict[str, Any]:
	"""
	Get data from Todoist Sync API with incremental sync support
	"""
	global API_TOKEN
	url = "https://api.todoist.com/sync/v9/sync"
	headers = {
		"Authorization": f"Bearer {API_TOKEN}",
		"Content-Type": "application/json"
	}
	
	data = {
		"sync_token": sync_state["sync_token"],
		"resource_types": ["labels", "items"]  # Only sync what we need
	}
	
	response = requests.post(url, headers=headers, json=data)
	response.raise_for_status()
	return response.json()

def get_new_updates(failed_before: bool = False) -> dict[str, Any] | None:
	"""
	Check if there are any updates since last sync
	Returns True if updates found, False otherwise
	"""
	global sync_state
	try:
		new_data = get_sync_data()
		sync_state["last_sync_check"] = time.time()
		has_changes = (
			len(new_data.get("items", [])) > 0 or 
			len(new_data.get("labels", [])) > 0
		)
		
		if not has_changes:
			print("LOOG:\t  [Sync] No changes detected")
			return None
			
		sync_state["sync_token"] = new_data["sync_token"]
		sync_state["last_sync"] = sync_state["last_sync_check"]

		print(f"LOOG:\t  [Sync] Changes detected: {len(new_data.get('items', []))} items, {len(new_data.get('labels', []))} labels")
		return new_data
		
	except Exception as e:
		print(f"LOOG:\t  [Sync Error] {e}")
		if failed_before: return None
		time.sleep(3) # wait 3 seconds.. 
		return get_new_updates(failed_before=True) # and try again

def get_ordered_active_projects(all_projects: list) -> list:
	if not all_projects: return []
	global EXCLUDED_LABELS
	active_projects = list(filter(lambda x: x["is_favorite"] and x["name"] not in EXCLUDED_LABELS, all_projects))
	if not active_projects:
		print("LOOG: [PROCESSING] No active projects exist")
		return []
	return sorted(active_projects, key=lambda x: x["item_order"])

def get_projects_tasks(all_tasks: list[dict], projects: list) -> list:
	projects = list(map(lambda x: x["name"], projects))
	return list(filter(lambda x: any(l in projects for l in x["labels"]), all_tasks))

def initialize_cache():
	"""Initialize cache with initial data load"""
	global API_TOKEN, sync_state, cached_data
	try:
		sync_state["sync_token"] = "*"
		data = get_new_updates()
		if not data: raise Exception()
		ordered_projects: list = get_ordered_active_projects(data.get("labels", []))
		tasks: list[dict] = get_projects_tasks(data.get("items", []), ordered_projects)

		cached_data["tasks"] = {t["id"]: [t, calculate_task_score(t)] for t in tasks}
		cached_data["ordered_tasks"] = sorted(cached_data["tasks"].values(), reverse=True, key=lambda x: x[1])
		cached_data["projects"] = {p["id"]: p for p in ordered_projects}
		cached_data["ordered_projects"] = ordered_projects

		print("LOOG:\t  [Initial Cache Load Complete]")
	except Exception as e:
		print(f"[Initial Cache Load Error]: {e}")


def update_cache(updates: dict[str, Any] | None) -> None:
    """
    Update cache with the new data only (incremental sync)
    """
    if not updates: return
    global cached_data, EXCLUDED_LABELS

    proj = cached_data["projects"]
    updated_or_new_labels = {label["id"]: label for label in updates.get("labels", [])}
    for pid, p_data in updated_or_new_labels.items():
        if p_data.get("is_deleted"):
            if pid in proj:
                del proj[pid]
        else:
            proj[pid] = p_data # Add or update the project data

    all_current_projects = list(proj.values())
    cached_data["ordered_projects"] = get_ordered_active_projects(all_current_projects)
    proj_names = {p["name"] for p in cached_data["ordered_projects"]}

    # --- 2. Update Tasks ---
    tasks = cached_data["tasks"]
    updated_or_new_items = {t["id"]: t for t in updates.get("items", [])}
    for tid, t_data in updated_or_new_items.items():
        is_active_project_related = any(label_name in proj_names for label_name in t_data.get("labels", []))

        if (t_data.get("checked") or
            t_data.get("is_deleted") or
            not is_active_project_related 
        ):
            if tid in tasks: del tasks[tid]
        else:
            score = calculate_task_score(t_data)
            tasks[tid] = [t_data, score]

    cached_data["ordered_tasks"] = sorted(tasks.values(), reverse=True, key=lambda x: x[1])

    print("LOOG:\t  [Cache Updated with New Changes]")


def background_cache_updater():
	while True:
		time.sleep(SYNC_CHECK_INTERVAL_SEC)
		try:
			update_cache(get_new_updates())
		except Exception as e:
			print(f"LOOG:\t  [Background Cache Updater Error]: {e}")

# Start background updater and initialize cache
app.router.on_startup.append(lambda: initialize_cache())
app.router.on_startup.append(lambda: Thread(target=background_cache_updater, daemon=True).start())

@app.get("/", response_class=HTMLResponse)
def update_dashboard(request: Request):
	global sync_state, cached_data
	try:
		tasks = cached_data["ordered_tasks"]
		last_cached = datetime.fromtimestamp(sync_state["last_sync"])
		
		# Calculate next check time
		seconds_since = int(time.time() - sync_state["last_sync_check"])
		seconds_remaining = max(0, SYNC_CHECK_INTERVAL_SEC - (seconds_since % SYNC_CHECK_INTERVAL_SEC))
		
		return templates.TemplateResponse("index.html", {
			"request": request,
			"tasks": tasks,
			"check_updates_url": "/check-updates",
			"force_sync_url": "/force-sync",
			"last_cached": last_cached.strftime('%Y-%m-%d %H:%M:%S'),
			"seconds_remaining": seconds_remaining,
			"cache_interval": SYNC_CHECK_INTERVAL_SEC
		})

	except Exception as e:
		return HTMLResponse(f"<h1>Error fetching tasks: {e}</h1>", status_code=500)

@app.get("/check-updates")
def check_updates():
	"""
	Check if there are updates and apply them if found
	"""
	try:
		updates = get_new_updates()
		if updates:
			update_cache(updates)
			print("LOOG:\t  [Cache Updated - Manual Check]")
		
		return RedirectResponse(url="/", status_code=303)
	except Exception as e:
		return HTMLResponse(f"<h1>Error checking updates: {e}</h1>", status_code=500)

@app.get("/force-sync")
def force_sync():
	"""
	Force a full sync and refresh cache
	"""
	global sync_state
	try:
		initialize_cache()
		print("LOOG:\t  [Cache Updated - Force Sync]")
		return RedirectResponse(url="/", status_code=303)
	except Exception as e:
		return HTMLResponse(f"<h1>Error during force sync: {e}</h1>", status_code=500)