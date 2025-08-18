const State = {
	COMPUTER: "COMPUTER",
	USER: "USER",
	TIE: "TIE",
};

const Move = {
	ROCK: "ROCK",
	PAPER: "PAPER",
	SCISSOR: "SCISSOR",
};

/* 
	------------- Score 
*/

const score = JSON.parse(localStorage.getItem("score")) || {
	USER: 0, // wins
	COMPUTER: 0, // losses
	TIE: 0, // ties
};
displayScore();

function resetScore() {
	score.USER = 0;
	score.COMPUTER = 0;
	score.TIE = 0;
	localStorage.removeItem("score");
}

function updateScore(winner) {
	score[winner]++;
	localStorage.setItem("score", JSON.stringify(score));
}

function displayScore() {
	const scoreElm = document.getElementById("score");
	scoreElm.innerHTML = `<span class="wins">Wins: ${score.USER}</span> | <span class="losses">Losses: ${score.COMPUTER}</span> | <span class="ties">Ties: ${score.TIE}</span>`;
}

/* 
	------------- Reset Button
*/

const resetBtn = document.querySelector(".reset-btn");
resetBtn.addEventListener("click", () => {
	resetScore();
	displayScore();
});

/* 
	------------- Computer Move
*/
function getComputerMove() {
	let choice = Math.floor(Math.random() * 3);
	if (choice === 1) return Move.ROCK;
	else if (choice === 2) return Move.PAPER;
	return Move.SCISSOR;
}

function displayComputerMove(computerMove) {
	const btnClass = ".computer-" + computerMove.toLowerCase() + "-btn";
	const computerMoveBtn = document.querySelector(btnClass);
	computerMoveBtn.classList.toggle("hidden");
	setTimeout(() => {
		computerMoveBtn.classList.toggle("hidden");
	}, 1250);
}

/* 
	------------- User Move
*/
function getUserMove(btn) {
	if (btn.classList.contains("user-rock-btn")) return Move.ROCK;
	if (btn.classList.contains("user-paper-btn")) return Move.PAPER;
	if (btn.classList.contains("user-scissor-btn")) return Move.SCISSOR;

	console.assert(false, "failed to getUserMove");
}

/* 
	------------- Result 
*/
function getResult(userMove, computerMove) {
	const complement = {
		[Move.ROCK]: Move.PAPER,
		[Move.PAPER]: Move.SCISSOR,
		[Move.SCISSOR]: Move.ROCK,
	};

	if (userMove === computerMove) return State.TIE;
	if (complement[userMove] === computerMove) return State.COMPUTER;
	if (complement[computerMove] === userMove) return State.USER;

	console.assert(false, "Failed to getResult of the game");
}

function displayResult(result) {
	const resElm = document.getElementById("game-result");
	const pair = {
		[State.USER]: "You Won",
		[State.COMPUTER]: "Computer Won",
		[State.TIE]: "A Tie",
	};
	resElm.innerText = pair[result];

	const scoreElm = document.getElementById("score");
	scoreElm.classList.toggle("removed");
	resElm.classList.toggle("removed");
	colorResult(resElm, result);

	setTimeout(() => {
		scoreElm.classList.toggle("removed");
		resElm.classList.toggle("removed");
		colorResult(resElm, result);
	}, 1250);
}

function colorResult(resElm, result) {
	const pair = {
		[State.USER]: "user-won-result",
		[State.COMPUTER]: "user-lost-result",
		[State.TIE]: "tie-result",
	};
	resElm.classList.toggle(pair[result]);
}

function colorButtons(userMove, computerMove, result) {
	const computerBtnClass = ".computer-" + computerMove.toLowerCase() + "-btn";
	const userBtnClass = ".user-" + userMove.toLowerCase() + "-btn";
	const computerMoveBtn = document.querySelector(computerBtnClass);
	const userMoveBtn = document.querySelector(userBtnClass);

	const pair = {
		[State.USER]: "user-won-result",
		[State.COMPUTER]: "user-lost-result",
		[State.TIE]: "tie-result",
	};

	if (result === State.COMPUTER) {
		computerMoveBtn.classList.toggle("winner-move");
		userMoveBtn.classList.toggle("loser-move");
	} else if (result === State.USER) {
		computerMoveBtn.classList.toggle("loser-move");
		userMoveBtn.classList.toggle("winner-move");
	}
	setTimeout(() => {
		if (result === State.COMPUTER) {
			computerMoveBtn.classList.toggle("winner-move");
			userMoveBtn.classList.toggle("loser-move");
		} else if (result === State.USER) {
			computerMoveBtn.classList.toggle("loser-move");
			userMoveBtn.classList.toggle("winner-move");
		}
	}, 1250);
}
/* 
////////////////////////////////////////
	------------- Game Function 
////////////////////////////////////////
*/
const userBtns = document.getElementsByClassName("user-choice-btn");
for (let btn of userBtns) {
	btn.addEventListener("click", () => {
		const userMove = getUserMove(btn);
		const computerMove = getComputerMove();
		const result = getResult(userMove, computerMove);
		displayComputerMove(computerMove);
		displayResult(result);
		colorButtons(userMove, computerMove, result);
		updateScore(result);
		displayScore();
	});
}
