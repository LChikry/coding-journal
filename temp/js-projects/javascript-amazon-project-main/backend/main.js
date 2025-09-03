const stopWords = [
	"a",
	"an",
	"the",
	"is",
	"in",
	"and",
	"at",
	"of",
	"on",
	"for",
	"to",
	"with",
	"from",
	"as",
	"",
];

export function isSearchHasResults(product, query) {
	const res1 = query.toLowerCase().split(" ");
	console.log(res1);

	const res2 = res1.some((word) => {
		if (stopWords.includes(word)) return false;
		return product.name.toLowerCase().includes(word);
	});

	console.log(res2);
	return res2;
}

let allProducts = null;
let cachedPage = null;

function initiatePage() {
	fetch("../backend/products.json")
		.then((res) => res.json())
		.then((products) => {
			allProducts = products;
			const productList = document.querySelector(".product-list");
			const fragment = document.createDocumentFragment();

			products.forEach((product) => {
				fragment.appendChild(createProductItem(product));
			});
			cachedPage = fragment.cloneNode(true);
			if (productList) productList.append(fragment);
		});
}

initiatePage();
// localStorage.removeItem("listProductInCart");
// localStorage.removeItem("NumProductInCart");

let listProductInCart =
	JSON.parse(localStorage.getItem("listProductInCart")) || [];
let NumProductInCart = localStorage.getItem("NumProductInCart");
if (!NumProductInCart) NumProductInCart = 0;
const cartElement = document.querySelector("#cart-number");
if (cartElement) cartElement.textContent = NumProductInCart;

const searchForm = document.querySelector(".main-header__search");
if (searchForm) {
	searchForm.addEventListener("submit", (event) => {
		event.preventDefault();
		const searchBox = document.querySelector(
			".main-header__search__textbox"
		);
		if (!searchBox.value) {
			searchBox.value = "";

			const productList = document.querySelector(".product-list");
			productList.innerHTML = "";
			productList.append(cachedPage.cloneNode(true));
			return;
		}
		const productList = document.querySelector(".product-list");
		const fragment = document.createDocumentFragment();

		allProducts.forEach((product) => {
			if (!isSearchHasResults(product, searchBox.value)) return;
			fragment.appendChild(createProductItem(product));
		});

		productList.innerHTML = "";
		productList.append(fragment);
	});
}

function addOrder(productId) {
	++NumProductInCart;
	listProductInCart.push(productId);
	localStorage.setItem("NumProductInCart", `${NumProductInCart}`);
	localStorage.setItem(
		"listProductInCart",
		JSON.stringify(listProductInCart)
	);

	const cartElement = document.querySelector("#cart-number");
	console.log("we have this value:", NumProductInCart);
	cartElement.textContent = NumProductInCart;
}

function createProductItem(product) {
	const itemImg = document.createElement("img");
	itemImg.className = "product-item__img";
	itemImg.src = `../${product.image}`;
	itemImg.alt = product.image
		.match(/[a-zA-Z\-0-9]+(?=.(jpg|webp|jpeg|png))/g)[0]
		.replace(/-/g, " ");

	const itemImgCaption = document.createElement("figcaption");
	itemImgCaption.className = "removed";
	itemImgCaption.innerHTML = itemImg.alt;

	const itemImgContainer = document.createElement("figure");
	itemImgContainer.className = "product-item__img-container";
	itemImgContainer.append(itemImg, itemImgCaption);

	const itemTitle = document.createElement("h3");
	itemTitle.className = "product-item__title";
	itemTitle.textContent = product.name;

	const itemRatingStars = document.createElement("img");
	itemRatingStars.className = "product-item__rating__stars";
	const roundedStars = (Math.round(product.rating.stars * 2) / 2) * 10;
	itemRatingStars.src = `/images/ratings/rating-${roundedStars}.png`;
	itemRatingStars.alt = `${product.rating.stars} Stars`;

	const itemRatingNumber = document.createElement("figcaption");
	itemRatingNumber.className = "product-item__rating__number";
	itemRatingNumber.innerHTML = `${product.rating.count}`;

	const itemRating = document.createElement("figure");
	itemRating.className = "product-item__rating";
	itemRating.append(itemRatingStars, itemRatingNumber);

	const itemPrice = document.createElement("p");
	itemPrice.className = "product-item__price";
	itemPrice.innerHTML = `&dollar;${(product.priceCents / 100).toFixed(2)}`;

	const itemQuantity = document.createElement("select");
	itemQuantity.required = true;

	itemQuantity.className = "product-item__ordering__quantity";
	itemQuantity.name = "productItemQuantity";

	for (let i = 1; i < 11; ++i) {
		const option = document.createElement("option");
		if (i == 1) option.selected = true;
		option.value = `${i}`;
		option.text = i;
		itemQuantity.append(option);
	}

	const itemInfo = document.createElement("div");
	itemInfo.className = "product-item__info";
	itemInfo.append(itemTitle, itemRating, itemPrice, itemQuantity);

	const itemAddButton = document.createElement("button");
	itemAddButton.type = "button";
	itemAddButton.className = "product-item__ordering__add-btn";
	itemAddButton.textContent = "Add to Cart";
	itemAddButton.addEventListener("click", () => addOrder(product.id));

	const item = document.createElement("section");
	item.className = "product-item";
	item.append(itemImgContainer, itemInfo, itemAddButton);
	return item;
}
