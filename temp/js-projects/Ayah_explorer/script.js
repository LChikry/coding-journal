class Api {
	#MIN_AYAH = 1;
	#MAX_AYAH = 6236;

	#getRandomAyahNumber() {
		return Math.floor(
			Math.random() * (this.#MAX_AYAH - this.#MIN_AYAH + 1) +
				this.#MIN_AYAH
		);
	}

	#getAPIEndpoint(ayahNumber) {
		console.assert(
			this.#MIN_AYAH <= ayahNumber && ayahNumber <= this.#MAX_AYAH,
			"Wrong Ayah Number"
		);

		return `http://api.alquran.cloud/v1/ayah/${ayahNumber}/quran-uthmani`;
	}

	async getRandomAyah() {
		try {
			const apiUrl = this.#getAPIEndpoint(this.#getRandomAyahNumber());
			const res = await fetch(apiUrl);
			const data = await res.json();
			return {
				ayah: data.data.text,
				surah: data.data.surah.name,
			};
		} catch (error) {
			// retry with expo backoff
			// otherwise throw error
		}
	}
}

class Card {
	#api;
	currentAyah;
	#cardElement;

	constructor(api) {
		this.#cardElement = document.querySelector(".ayah-card");
		this.#api = api;

		this.renderNewAyah();
	}

	renderNewAyah() {
		this.#renderWaitingWindow();
		this.#api
			.getRandomAyah()
			.then((ayah) => {
				this.#cardElement.innerHTML = "";
				this.#cardElement.appendChild(this.#getAyahCard(ayah));
				this.currentAyah = ayah;
			})
			.catch((err) => {
				console.log("error happened");
				// display error message with retry button
			});
	}

	#renderWaitingWindow() {
		this.#cardElement.innerHTML = `<div class="loader"></div>`;
	}

	#shareAyah() {
		console.log("clicked");
		const twitterUrl = `https://twitter.com/intent/tweet?text=${this.currentAyah.ayah} - ${this.currentAyah.surah}`;
		console.log(this.currentAyah);

		window.open(twitterUrl, "_blank");
	}

	#getAyahCard(ayah) {
		const rightQuoteIcon = document.createElement("i");
		rightQuoteIcon.className = "fa-solid fa-quote-right";
		const ayahText = document.createElement("strong");
		ayahText.id = "ayah";
		ayahText.innerText = ayah.ayah;
		const leftQuoteIcon = document.createElement("i");
		leftQuoteIcon.className = "fa-solid fa-quote-left";
		const quote = document.createElement("q");
		quote.className = "ayah-card__ayah";
		quote.append(rightQuoteIcon, ayahText, leftQuoteIcon);

		const surahText = document.createElement("em");
		surahText.innerText = ayah.surah;
		const surah = document.createElement("p");
		surah.className = "ayah-card__surah";
		surah.innerHTML = "&mdash;";
		surah.appendChild(surahText);

		const generateButton = document.createElement("button");
		generateButton.type = "button";
		generateButton.ariaLabel = "generate new quote";
		generateButton.title = "Generate new quote";
		generateButton.className = "button button--new-ayah";
		generateButton.innerHTML = "آية أخرى";
		generateButton.addEventListener("click", () => this.renderNewAyah());

		const shareButton = document.createElement("button");
		shareButton.type = "button";
		shareButton.ariaLabel = "share on twitter/x";
		shareButton.title = "Tweet this!";
		shareButton.className = "button button--share";
		shareButton.innerHTML = "آية أخرى";
		shareButton.innerHTML = `
			<i class="fa-brands fa-x-twitter"></i>
			<i class="fa-solid fa-share-nodes"></i>
		`;
		shareButton.addEventListener("click", () => this.#shareAyah());

		const buttons = document.createElement("div");
		buttons.className = "ayah-card__buttons";
		buttons.append(generateButton, shareButton);

		const fg = document.createDocumentFragment();
		fg.append(quote, surah, buttons);
		return fg;
	}
}

const card = new Card(new Api());
