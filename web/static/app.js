const purseEl = document.getElementById("purse");
const messageEl = document.getElementById("message");
const betPanel = document.getElementById("bet-panel");
const guessPanel = document.getElementById("guess-panel");
const revealPanel = document.getElementById("reveal-panel");
const brokePanel = document.getElementById("broke-panel");
const betInput = document.getElementById("bet-amount");
const errorEl = document.getElementById("error-text");
const die1 = document.getElementById("die1");
const die2 = document.getElementById("die2");
const die1Jp = document.getElementById("die1-jp");
const die2Jp = document.getElementById("die2-jp");
const resultLine = document.getElementById("result-line");

const SESSION_KEY = "cho-han-v2";
let gameState = null;

function setError(msg) {
  errorEl.hidden = !msg;
  errorEl.textContent = msg || "";
}

function persist() {
  AppSession.save(SESSION_KEY, { state: gameState, bet: betInput.value });
}

function restore() {
  const saved = AppSession.load(SESSION_KEY);
  if (!saved) return;
  if (saved.bet) betInput.value = saved.bet;
  if (saved.state) {
    const s = saved.state;
    if (s.phase === "guess" && (s.dice1 == null || s.dice2 == null)) {
      return;
    }
    applyState(s);
  }
}

AppSession.wireHelpSave(SESSION_KEY, () => ({ state: gameState, bet: betInput.value }));

function show(el, on) {
  el.classList.toggle("hidden", !on);
}

function applyState(data) {
  gameState = data;
  purseEl.textContent = String(data.purse);
  messageEl.textContent = data.message || "";

  const phase = data.phase;
  show(betPanel, phase === "bet" || phase === "reveal");
  show(guessPanel, phase === "guess");
  show(revealPanel, phase === "reveal");
  show(brokePanel, phase === "broke");

  if (phase === "reveal" && data.dice1 != null) {
    die1.textContent = String(data.dice1);
    die2.textContent = String(data.dice2);
    die1Jp.textContent = data.dice1_label || "";
    die2Jp.textContent = data.dice2_label || "";
    const parity = data.parity === "even" ? "Cho" : "Han";
    resultLine.textContent = `Total ${data.total} (${parity}) — you picked ${data.player_guess}, answer was ${data.correct_bet}.`;
    resultLine.className = "result-line " + (data.won ? "win" : "lose");
  }

  document.getElementById("btn-bet").disabled = phase === "guess";
  persist();
}

async function post(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Request failed.");
  return data;
}

async function placeBet() {
  setError("");
  try {
    const amount = Number(betInput.value);
    const data = await post("/api/bet", { state: gameState || { phase: "bet", purse: 5000 }, amount });
    applyState(data);
  } catch (e) {
    setError(e.message);
  }
}

async function guess(choice) {
  setError("");
  try {
    const data = await post("/api/guess", { state: gameState, guess: choice });
    applyState(data);
  } catch (e) {
    setError(e.message);
  }
}

async function resetGame() {
  const data = await post("/api/reset", { state: {} });
  applyState(data);
}

document.getElementById("btn-bet").addEventListener("click", placeBet);
document.getElementById("btn-cho").addEventListener("click", () => guess("CHO"));
document.getElementById("btn-han").addEventListener("click", () => guess("HAN"));
document.getElementById("btn-next").addEventListener("click", placeBet);
document.getElementById("btn-reset").addEventListener("click", resetGame);

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    betInput.value = chip.dataset.bet;
    persist();
  });
});

betInput.addEventListener("input", persist);

applyState({ phase: "bet", purse: 5000, message: "Place your bet in mon." });
restore();
