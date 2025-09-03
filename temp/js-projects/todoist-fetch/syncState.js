import { incrementalSync } from "./app.js";

function renderUpdatedAt(updatedAt) {
	const lastUpdate = document.querySelector(".uptodate-info__last-update");

	let text = "UpdatedAt: ";
	if (!updatedAt) {
		lastUpdate.innerHTML = text + "Never";
		return;
	}

	const since = Math.floor((new Date() - updatedAt) / 1000);
	if (since < 5) {
		text += "just now";
	} else if (since < 60) {
		text += since + " seconds ago";
	} else if (since < 3600) {
		text += Math.floor(since / 60) + " minutes ago";
	} else if (since < 86400) {
		text += Math.floor(since / 3600) + " hours ago";
	} else {
		text += `${contentState.updatedAt.getDate()} ${contentState.updatedAt.getHours()}:${contentState.updatedAt.getMinutes()}`;
	}
	lastUpdate.innerHTML = text;
}

function renderDataFlowStatus(syncState) {
	document.querySelector(".uptodate-info__status-text").innerHTML =
		syncState.syncStatusStr;

	const syncStatus = document.querySelector(".uptodate-info__status");
	syncStatus.classList.remove("green-color");
	syncStatus.classList.remove("red-color");
	if (syncState.isServerDown) syncStatus.classList.add("red-color");
	else if (!syncState.isOffline) syncStatus.classList.add("green-color");
}

function getFormattedTime(seconds) {
	const minutes = Math.floor(seconds / 60);
	const secs = seconds % 60;
	return (
		String(minutes).padStart(2, "0") + ":" + String(secs).padStart(2, "0")
	);
}

export function renderSyncState(syncState, updatedAt) {
	renderUpdatedAt(updatedAt);
	renderDataFlowStatus(syncState);
}

export function renderAndUpdateRemainingTime(contentState, syncState) {
	document.querySelector(".uptodate-info__next-update").innerHTML =
		getFormattedTime(--syncState.nextUpdateSec);
	if (syncState.nextUpdateSec === 0) incrementalSync(contentState, syncState);
}
