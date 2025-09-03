export default async function syncTodoistToLocal(contentState, syncState) {
	const data = await fetchNewData(contentState.syncToken);

	if (data.isOffline || data.isServerDown) {
		syncState.isOffline = data.isOffline;
		syncState.isServerDown = data.isServerDown;
		if (syncState.isOffline) syncState.syncStatusStr = "Offline";
		else syncState.syncStatusStr = "ServerDown";
		return { hasNewData: false };
	}

	syncState.syncStatusStr = "Online";
	contentState.syncToken = data.syncToken;
	contentState.labels = getProcessedLabels(contentState.labels, data.labels);
	contentState.tasks = getProcessedTasks(
		contentState.tasks,
		data.tasks,
		contentState.labels
	);
	contentState.updatedAt = data.updatedAt;
	return { hasNewData: true };
}

async function fetchNewData(syncToken) {
	const API_KEY = "";
	const API_URL = "https://api.todoist.com/api/v1/sync";

	try {
		const res = await fetch(API_URL, {
			method: "POST",
			headers: {
				Authorization: `Bearer ${API_KEY}`,
				"Content-Type": "application/x-www-form-urlencoded",
			},
			body: new URLSearchParams({
				sync_token: syncToken,
				resource_types: '["items", "labels"]',
			}),
		});

		if (!res.ok) {
			console.log("Error in Fetching");
			return {
				isOffline: true,
				isServerDown: false,
			};
		}

		const data = await res.json();
		return {
			syncToken: data.sync_token,
			labels: data.labels,
			tasks: data.items,
			updatedAt: new Date(),
			isServerDown: false,
			isOffline: false,
		};
	} catch (error) {
		console.log(error);
		return {
			isServerDown: true,
			isOffline: false,
		};
		// Handle Error
	}
}

function getProcessedLabels(oldLabels, newLabels) {
	let res = newLabels.filter((x) => x.is_favorite);
	res.sort((a, b) => a.item_order - b.item_order);
	res = res.map((x) => {
		return {
			name: x.name,
			item_order: x.item_order,
		};
	});

	oldLabels.push(...res);
	return oldLabels;
}

function getProcessedTasks(oldTasks, newTasks, labels) {
	if (labels.length === 0) return [];

	let res = newTasks.filter((t) => {
		return t.labels.some((ln) => labels.some((lo) => lo.name === ln));
	});

	res = res.map((x) => {
		const score = getTaskScore(x);
		return {
			content: x.content,
			dueDate: x.due ? x.due.data : null,
			id: x.id,
			project_id: x.project_id,
			labels: x.labels,
			score: score,
			description: x.description,
		};
	});

	res.sort((a, b) => a.score - b.score);
	oldTasks.push(...res);
	return oldTasks;
}

function getTaskScore(task) {
	return Math.floor(Math.random() * 300);
}
