// const URL = "https://api.dicebear.com/9.x/lorelei/svg?seed=";

// const gallery = document.querySelector(".gallery");

// function getRandomNum() {
// 	const min = 1,
// 		max = 2000;
// 	return Math.floor(Math.random() * (max - min + 1) + min);
// }

// let isLoadingFinished = false;

// function loadImages(numImages = 4) {
// 	for (let i = 0; i < numImages; ++i) {
// 		const img = document.createElement("img");
// 		img.src = `${URL}${getRandomNum()}`;
// 		gallery.append(img);
// 	}
// 	isLoadingFinished = true;
// 	console.log("finished loading");
// }

// loadImages();

// window.addEventListener("scroll", () => {
// 	if (
// 		window.scrollY + window.innerHeight >=
// 			document.body.scrollHeight - 800 &&
// 		isLoadingFinished
// 	) {
// 		isLoadingFinished = false;
// 		loadImages(10);
// 	}
// });

// const img = URL + getRandomNum();
// console.log(img);
// fetch(img)
// 	.then(async (res) => {
// 		console.log(res);
// 	})
// 	.catch(() => {
// 		console.log("hello");
// 	});

const xhr = new XMLHttpRequest();
xhr.addEventListener("load", () => {
	console.log(xhr.response);
});

xhr.open("GET", "https://supersimplebackend.dev");
xhr.send();
