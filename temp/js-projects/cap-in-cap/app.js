async function getVidStream() {
	vidStream = await navigator.mediaDevices.getDisplayMedia();
	return vidStream;
}

video = document.querySelector(".vid-container");
button = document.querySelector(".btn");

button.addEventListener("click", () => {
	if (button.innerText === "start") {
		navigator.mediaDevices
			.getDisplayMedia()
			.then((res) => {
				video.srcObject = res;
				video.onloadedmetadata = () => {
					video.play();
				};
			})
			.catch((e) => {
				console.log("error: ", e);
			});

		button.innerText = "pic in pic";
	} else {
		video.requestPictureInPicture();
		button.innerText = "start";
	}
});
