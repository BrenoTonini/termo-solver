const CORRECT = "correct";
const CLOSE   = "close";
const WRONG   = "wrong";

// carregado em init()
let VALID_INPUTS = [];

async function loadValidInputs() {
  const response = await fetch("../src/dictionary/valid-inputs.txt");
  if (!response.ok) throw new Error("Falha ao carregar dicionário.");
  const text = await response.text();
  return [...new Set(
    text.split(/\r?\n/)
      .map(w => normalizeWord(w))
      .filter(w => w.length === 5)
  )];
}

function normalizeWord(word) {
  return word
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function randomWord(wordList = VALID_INPUTS) {
  return wordList[Math.floor(Math.random() * wordList.length)];
}

// equivalente de new_attempt()
function evaluateAttempt(guess, correctAnswer) {
  const result = Array(5).fill(null);
  const remaining = correctAnswer.split("");

  for (let i = 0; i < 5; i++) {
    if (guess[i] === correctAnswer[i]) {
      result[i] = { char: guess[i], status: CORRECT };
      remaining[i] = null;
    }
  }

  for (let i = 0; i < 5; i++) {
    if (result[i] !== null) continue;
    const pos = remaining.indexOf(guess[i]);
    if (pos !== -1) {
      result[i] = { char: guess[i], status: CLOSE };
      remaining[pos] = null;
    } else {
      result[i] = { char: guess[i], status: WRONG };
    }
  }

  return result;
}

// equivalente de filter_correct_characters()
function filterCorrectChars(attempt, word) {
  for (let i = 0; i < attempt.length; i++) {
    if (attempt[i].status === CORRECT && word[i] !== attempt[i].char) return false;
  }
  return true;
}

// equivalente de filter_close_characters()
function filterCloseChars(attempt, word) {
  for (let i = 0; i < attempt.length; i++) {
    if (attempt[i].status === CLOSE) {
      if (!word.includes(attempt[i].char) || word[i] === attempt[i].char) return false;
    }
  }
  return true;
}

// equivalente de filter_wrong_characters()
function filterWrongChars(attempt, word) {
  const charInfo = {};

  for (const { char, status } of attempt) {
    if (!charInfo[char]) charInfo[char] = { min: 0, hasWrong: false };
    if (status === CORRECT || status === CLOSE) {
      charInfo[char].min++;
    } else if (status === WRONG) {
      charInfo[char].hasWrong = true;
    }
  }

  for (const [char, info] of Object.entries(charInfo)) {
    const count = word.split("").filter(c => c === char).length;
    if (count < info.min) return false;
    if (info.hasWrong && count > info.min) return false;
  }

  return true;
}

// equivalente de filter_attempted_word()
function filterAttemptedWord(attempt, word) {
  const attemptedWord = attempt.map(a => a.char).join("");
  return attemptedWord !== word;
}

// equivalente de get_remaining_possibilities()
function getRemainingPossibilities(attempts, wordList = VALID_INPUTS) {
  let candidates = [...wordList];
  for (const attempt of attempts) {
    candidates = candidates.filter(w => filterCorrectChars(attempt, w));
    candidates = candidates.filter(w => filterCloseChars(attempt, w));
    candidates = candidates.filter(w => filterWrongChars(attempt, w));
    candidates = candidates.filter(w => filterAttemptedWord(attempt, w));
  }
  return candidates;
}

// equivalente de build_frequency() + score_word() + best_word()
function buildFrequency(candidates) {
  const freq = {};
  for (const word of candidates) {
    for (const c of new Set(word)) {
      freq[c] = (freq[c] || 0) + 1;
    }
  }
  return freq;
}

function scoreWord(word, freq) {
  let score = 0;
  const used = new Set();
  for (const c of word) {
    if (used.has(c)) continue;
    score += freq[c] || 0;
    used.add(c);
  }
  return score;
}

function bestWord(candidates) {
  if (!candidates.length) return randomWord();
  const freq = buildFrequency(candidates);
  let best = null, bestScore = -1;
  for (const word of candidates) {
    const score = scoreWord(word, freq);
    if (score > bestScore) { bestScore = score; best = word; }
  }
  return best;
}