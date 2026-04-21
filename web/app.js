// app.js — interface web do Termo Solver
// Usa as funções de solver.js (não duplica lógica)

const ATTEMPTS_LIMIT = 6;
const WORD_SIZE = 5;

const KEYBOARD_LAYOUT = [
  ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
  ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
  ["enter", "z", "x", "c", "v", "b", "n", "m", "backspace"]
];

const STATUS_PRIORITY = { wrong: 1, close: 2, correct: 3 };

// ── DOM refs ──────────────────────────────────────────────────────────────────
const screens = {
  mode:   document.getElementById("mode-screen"),
  game:   document.getElementById("game-screen"),
  solver: document.getElementById("solver-screen"),
};

const boardEl       = document.getElementById("board");
const keyboardEl    = document.getElementById("keyboard");
const statusEl      = document.getElementById("status");
const modeLabelEl   = document.getElementById("mode-label");
const hintPanelEl   = document.getElementById("hint-panel");
const hintCountEl   = document.getElementById("hint-count");
const hintListEl    = document.getElementById("hint-list");
const hintBtnEl     = document.getElementById("hint-btn");
const hintSuggEl    = document.getElementById("hint-suggestion");
const hintWordEl    = document.getElementById("hint-word");

const solverInputEl     = document.getElementById("solver-input");
const solverRowEl       = document.getElementById("solver-row");
const solverConfirmEl   = document.getElementById("solver-confirm-btn");
const solverAttemptsEl  = document.getElementById("solver-attempts-list");
const resultsListEl     = document.getElementById("results-list");
const resultsCountEl    = document.getElementById("results-count");
const bestSuggEl        = document.getElementById("best-suggestion");
const bestWordEl        = document.getElementById("best-word");

// ── State ─────────────────────────────────────────────────────────────────────
let currentMode   = null;
let answer        = "";
let attempts      = [];
let currentGuess  = "";
let gameOver      = false;
let keyStatuses   = {};

// Solver state
let solverAttempts     = [];
let solverTileStatuses = ["wrong", "wrong", "wrong", "wrong", "wrong"];

// ── Screen routing ────────────────────────────────────────────────────────────
function showScreen(name) {
  for (const [key, el] of Object.entries(screens)) {
    el.classList.toggle("active", key === name);
  }
  if (name === "game") {
    document.addEventListener("keydown", handleKeyboardEvent);
  } else {
    document.removeEventListener("keydown", handleKeyboardEvent);
  }
}

// ── Init ──────────────────────────────────────────────────────────────────────
async function init() {
  setStatus("Carregando dicionário...");
  try {
    VALID_INPUTS = await loadValidInputs();

    // Mode cards
    document.querySelectorAll(".mode-card").forEach(btn => {
      btn.addEventListener("click", () => selectMode(btn.dataset.mode));
    });

    document.getElementById("back-btn").addEventListener("click", goHome);
    document.getElementById("solver-back-btn").addEventListener("click", goHome);
    document.getElementById("new-game-btn").addEventListener("click", startNewGame);
    document.getElementById("solver-reset-btn").addEventListener("click", resetSolver);
    hintBtnEl.addEventListener("click", showHint);
    solverConfirmEl.addEventListener("click", confirmSolverAttempt);
    solverInputEl.addEventListener("input", onSolverInput);
    solverInputEl.addEventListener("keydown", e => {
      if (e.key === "Enter") confirmSolverAttempt();
    });

    setStatus("");
  } catch (err) {
    setStatus("Erro ao carregar dicionário. Use um servidor local.", "lose");
  }
}

function goHome() {
  showScreen("mode");
}

function selectMode(mode) {
  currentMode = mode;
  if (mode === "solver") {
    resetSolver();
    showScreen("solver");
  } else {
    modeLabelEl.textContent = mode === "assisted" ? "assistido" : "jogar";
    hintPanelEl.classList.toggle("hidden", mode !== "assisted");
    buildBoard();
    buildKeyboard();
    startNewGame();
    showScreen("game");
  }
}

// ── Game (play + assisted) ────────────────────────────────────────────────────
function startNewGame() {
  attempts      = [];
  currentGuess  = "";
  gameOver      = false;
  keyStatuses   = {};
  answer        = randomWord(VALID_INPUTS);
  updateBoard();
  updateKeyboard();
  if (currentMode === "assisted") {
    updateHintPanel([]);
    hintSuggEl.classList.add("hidden");
  }
  setStatus(`Tentativa 1 de ${ATTEMPTS_LIMIT}.`);
}

function setStatus(msg, tone = "") {
  if (!statusEl) return;
  statusEl.textContent = msg;
  statusEl.className   = "status" + (tone ? ` ${tone}` : "");
}

function buildBoard() {
  boardEl.innerHTML = "";
  for (let r = 0; r < ATTEMPTS_LIMIT; r++) {
    const row = document.createElement("div");
    row.className = "row";
    for (let c = 0; c < WORD_SIZE; c++) {
      const tile = document.createElement("div");
      tile.className = "tile";
      row.appendChild(tile);
    }
    boardEl.appendChild(row);
  }
}

function buildKeyboard() {
  keyboardEl.innerHTML = "";
  for (const rowKeys of KEYBOARD_LAYOUT) {
    const row = document.createElement("div");
    row.className = "key-row";
    for (const k of rowKeys) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "key";
      btn.dataset.key = k;
      if (k === "enter")     { btn.textContent = "↵"; btn.classList.add("special"); }
      else if (k === "backspace") { btn.textContent = "⌫"; btn.classList.add("special"); }
      else btn.textContent = k.toUpperCase();
      btn.addEventListener("click", () => handleInput(k));
      row.appendChild(btn);
    }
    keyboardEl.appendChild(row);
  }
}

function updateBoard() {
  const rows = boardEl.querySelectorAll(".row");
  for (let r = 0; r < ATTEMPTS_LIMIT; r++) {
    const tiles = rows[r].querySelectorAll(".tile");
    const attempt = attempts[r];
    for (let c = 0; c < WORD_SIZE; c++) {
      const tile = tiles[c];
      tile.className = "tile";
      tile.textContent = "";
      if (attempt) {
        tile.textContent = attempt[c].char.toUpperCase();
        tile.classList.add(attempt[c].status);
        tile.classList.add("revealed");
      } else if (r === attempts.length && currentGuess[c]) {
        tile.textContent = currentGuess[c].toUpperCase();
        tile.classList.add("filled");
      }
    }
  }
}

function updateKeyboard() {
  keyboardEl.querySelectorAll(".key[data-key]").forEach(btn => {
    const k = btn.dataset.key;
    btn.classList.remove("wrong", "close", "correct");
    if (keyStatuses[k]) btn.classList.add(keyStatuses[k]);
  });
}

function setKeyStatus(letter, status) {
  const cur = keyStatuses[letter];
  if ((STATUS_PRIORITY[status] || 0) >= (STATUS_PRIORITY[cur] || 0)) {
    keyStatuses[letter] = status;
  }
}

function updateHintPanel(currentAttempts) {
  const candidates = getRemainingPossibilities(currentAttempts);
  hintCountEl.textContent = `${candidates.length} palavras`;
  renderWordList(hintListEl, candidates.slice(0, 50));
  hintSuggEl.classList.add("hidden");
}

function showHint() {
  const candidates = getRemainingPossibilities(attempts);
  const best = bestWord(candidates);
  hintWordEl.textContent = best.toUpperCase();
  hintSuggEl.classList.remove("hidden");
}

function renderWordList(listEl, words) {
  listEl.innerHTML = "";
  for (const w of words) {
    const li = document.createElement("li");
    li.textContent = w.toUpperCase();
    listEl.appendChild(li);
  }
}

function handleEnter() {
  if (gameOver) return;
  if (currentGuess.length !== WORD_SIZE) {
    setStatus("Digite uma palavra de 5 letras.");
    return;
  }
  const guess = normalizeWord(currentGuess);
  if (!VALID_INPUTS.includes(guess)) {
    setStatus("Palavra não está no dicionário.");
    return;
  }

  // usa evaluateAttempt de solver.js
  const attempt = evaluateAttempt(guess, answer);
  attempts.push(attempt);
  for (const { char, status } of attempt) setKeyStatus(char, status);
  currentGuess = "";
  updateBoard();
  updateKeyboard();

  if (currentMode === "assisted") updateHintPanel(attempts);

  if (guess === answer) {
    gameOver = true;
    setStatus("Parabéns! Você acertou!", "win");
    return;
  }
  if (attempts.length >= ATTEMPTS_LIMIT) {
    gameOver = true;
    setStatus(`Fim de jogo. Era: ${answer.toUpperCase()}`, "lose");
    return;
  }
  setStatus(`Tentativa ${attempts.length + 1} de ${ATTEMPTS_LIMIT}.`);
}

function handleBackspace() {
  if (gameOver || !currentGuess.length) return;
  currentGuess = currentGuess.slice(0, -1);
  updateBoard();
}

function handleLetter(letter) {
  if (gameOver || currentGuess.length >= WORD_SIZE) return;
  currentGuess += letter;
  updateBoard();
}

function handleInput(input) {
  if (input === "enter")     return handleEnter();
  if (input === "backspace") return handleBackspace();
  if (/^[a-z]$/.test(input)) handleLetter(input);
}

function handleKeyboardEvent(e) {
  const key = normalizeWord(e.key);
  if (key === "enter")     { e.preventDefault(); handleInput("enter"); return; }
  if (key === "backspace") { e.preventDefault(); handleInput("backspace"); return; }
  if (/^[a-z]$/.test(key)) handleInput(key);
}

// ── Solver mode ───────────────────────────────────────────────────────────────
function resetSolver() {
  solverAttempts     = [];
  solverTileStatuses = ["wrong", "wrong", "wrong", "wrong", "wrong"];
  solverInputEl.value = "";
  solverAttemptsEl.innerHTML = "";
  buildSolverRow("", solverTileStatuses);
  updateSolverResults();
}

function buildSolverRow(word, statuses) {
  solverRowEl.innerHTML = "";
  for (let i = 0; i < 5; i++) {
    const tile = document.createElement("div");
    tile.className = `tile solver-tile ${statuses[i]}`;
    tile.dataset.index = i;
    tile.textContent = word[i] ? word[i].toUpperCase() : "";
    tile.addEventListener("click", () => cycleTileStatus(i));
    solverRowEl.appendChild(tile);
  }
}

function cycleTileStatus(index) {
  const order = ["wrong", "close", "correct"];
  const cur  = solverTileStatuses[index];
  const next = order[(order.indexOf(cur) + 1) % order.length];
  solverTileStatuses[index] = next;
  const word = normalizeWord(solverInputEl.value).padEnd(5, " ");
  buildSolverRow(word, solverTileStatuses);
}

function onSolverInput(e) {
  const raw  = normalizeWord(e.target.value).slice(0, 5);
  e.target.value = raw;
  buildSolverRow(raw, solverTileStatuses);
}

function confirmSolverAttempt() {
  const word = normalizeWord(solverInputEl.value);
  if (word.length !== 5) {
    solverInputEl.classList.add("shake");
    setTimeout(() => solverInputEl.classList.remove("shake"), 400);
    return;
  }
  if (!VALID_INPUTS.includes(word)) {
    solverInputEl.classList.add("shake");
    setTimeout(() => solverInputEl.classList.remove("shake"), 400);
    return;
  }

  const attempt = solverTileStatuses.map((status, i) => ({
    char: word[i],
    status,
  }));

  solverAttempts.push(attempt);
  renderSolverAttempt(attempt);

  // reset row
  solverInputEl.value    = "";
  solverTileStatuses     = ["wrong", "wrong", "wrong", "wrong", "wrong"];
  buildSolverRow("", solverTileStatuses);
  updateSolverResults();
}

function renderSolverAttempt(attempt) {
  const row = document.createElement("div");
  row.className = "solver-attempt-row";
  for (const { char, status } of attempt) {
    const tile = document.createElement("div");
    tile.className = `tile ${status} revealed`;
    tile.textContent = char.toUpperCase();
    row.appendChild(tile);
  }
  solverAttemptsEl.appendChild(row);
}

function updateSolverResults() {
  const candidates = getRemainingPossibilities(solverAttempts);
  resultsCountEl.textContent = `${candidates.length} palavras`;
  renderWordList(resultsListEl, candidates.slice(0, 100));
  if (candidates.length > 0 && solverAttempts.length > 0) {
    bestWordEl.textContent = bestWord(candidates).toUpperCase();
    bestSuggEl.classList.remove("hidden");
  } else {
    bestSuggEl.classList.add("hidden");
  }
}

init();