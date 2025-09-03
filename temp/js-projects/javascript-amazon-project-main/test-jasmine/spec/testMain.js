import { isSearchHasResults } from "../../backend/main.js";

describe("Main Product Search Functionality", () => {
	it("ChecksForPossibleResultsOfOneExistedWord", () => {
		const product = { name: "A Frizer for your mom" };
		expect(isSearchHasResults(product, "frizer")).toBe(true);
	});

	it("ChecksForPossibleResultsOfThreeExistedWord", () => {
		const product = {
			name: "A Frizer for your mom by the night it was ther",
		};
		expect(isSearchHasResults(product, "frizer your mom")).toBe(true);
	});

	it("ChecksForNonExistedPossibleResults", () => {
		const product = { name: "A Frizer for your mom" };
		expect(isSearchHasResults(product, "dump thing")).toBe(false);
	});

	it("ChecksForPossibleResultsFromEmptySearch", () => {
		const product = { name: "A Frizer for your mom" };
		expect(isSearchHasResults(product, "")).toBe(false);
	});

	it("ChecksForPossibleResultsFromWhitespaceSearch", () => {
		const product = { name: "the whole market is here" };
		expect(isSearchHasResults(product, " ")).toBe(false);
	});
});
