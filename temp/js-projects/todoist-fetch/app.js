import syncTodoistToLocal from "./contentStateProcessing.js";
import { renderAndUpdateRemainingTime, renderSyncState } from "./syncState.js";
import { addWaitingEffect, deleteWaitingEffect } from "./waitingEffect.js";

const INITIAL_UPDATE_FREQ_SEC = 30;

function initializeState() {
	const contentState = JSON.parse(localStorage.getItem("contentState")) || {
		syncToken: "*",
		labels: [],
		tasks: [],
		updatedAt: undefined,
	};

	if (contentState.updatedAt) {
		contentState.updatedAt = new Date(contentState.updatedAt);
	}

	const syncState = {
		isOffline: false,
		isServerDown: false,
		syncStatusStr: undefined,

		nextUpdateSec: INITIAL_UPDATE_FREQ_SEC,
		todoistSyncEventId: undefined,
	};

	return { contentState, syncState };
}

function renderContentState(contentState) {
	console.assert(contentState, "Function call with no Arguments");

	function createRowElement(data, order) {
		return `
		<tr class="task-table__data">
			<td>${order}</td>
			<td>${data.content}</td>
			<td>${data.dueDate ? data.dueDate : "&mdash;"}</td>
			<td>${data.score ? data.score : "&mdash;"}</td>
		</tr>
	`;
	}
	let tableContent = "";
	for (let i = 1; i <= contentState.tasks.length; ++i) {
		tableContent += createRowElement(contentState.tasks[i - 1], i);
	}
	const tbody = document.querySelector(".task-table__body");
	tbody.innerHTML = tableContent;
}

export async function incrementalSync(contentState, syncState) {
	addWaitingEffect();
	syncState.nextUpdateSec = INITIAL_UPDATE_FREQ_SEC;
	const res = await syncTodoistToLocal(contentState, syncState);
	deleteWaitingEffect();

	renderSyncState(syncState, contentState.updatedAt);
	if (res.hasNewData) {
		localStorage.setItem("contentState", JSON.stringify(contentState));
		renderContentState(contentState);
	}
}

async function fullSync(contentState, syncState) {
	contentState.syncToken = "*";
	incrementalSync(contentState, syncState);
}

function startApp(contentState, syncState) {
	incrementalSync(contentState, syncState);

	document.querySelector(".button--update").addEventListener("click", () => {
		incrementalSync(contentState, syncState);
	});

	document
		.querySelector(".button--sync")
		.addEventListener("click", () => fullSync(contentState, syncState));

	syncState.todoistSyncEventId = setInterval(
		() => renderAndUpdateRemainingTime(contentState, syncState),
		998
	);

	setInterval(() => renderSyncState(syncState, contentState.updatedAt), 6000);
}

function main() {
	const { contentState, syncState } = initializeState();
	startApp(contentState, syncState);
}

main();
