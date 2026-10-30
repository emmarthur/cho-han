"""
Cho-Han (even/odd dice) — Al Sweigart Project #15.

Two dice; player bets mon on CHO (even) or HAN (odd). Wins pay pot; house takes 10% fee.
"""

from __future__ import annotations

import random
from copy import deepcopy
from typing import Any, Literal

STARTING_PURSE = 5000
HOUSE_FEE_RATE = 10  # percent of pot on wins

Phase = Literal["bet", "guess", "reveal", "broke"]
Guess = Literal["CHO", "HAN"]

JAPANESE_NUMBERS: dict[int, str] = {
    1: "ICHI",
    2: "NI",
    3: "SAN",
    4: "SHI",
    5: "GO",
    6: "ROKU",
}


def initial_state() -> dict[str, Any]:
    return {
        "purse": STARTING_PURSE,
        "phase": "bet",
        "pot": 0,
        "dice1": None,
        "dice2": None,
        "player_guess": None,
        "correct_bet": None,
        "won": None,
        "fee": 0,
        "message": "Place your bet in mon.",
    }


def state_for_client(state: dict[str, Any]) -> dict[str, Any]:
    """Full state for API roundtrip; the web UI hides dice until reveal."""
    return deepcopy(state)


def _roll_dice(rng: random.Random) -> tuple[int, int]:
    return rng.randint(1, 6), rng.randint(1, 6)


def _correct_guess(dice1: int, dice2: int) -> Guess:
    return "CHO" if (dice1 + dice2) % 2 == 0 else "HAN"


def place_bet(state: dict[str, Any], amount: int, rng: random.Random | None = None) -> dict[str, Any]:
    if state["phase"] not in ("bet", "reveal"):
        raise ValueError("Place a bet only when a new round is ready.")
    if state["phase"] == "reveal":
        state = deepcopy(state)
        state["phase"] = "bet"
        state["won"] = None
        state["player_guess"] = None
        state["correct_bet"] = None
        state["dice1"] = None
        state["dice2"] = None
        state["fee"] = 0
    else:
        state = deepcopy(state)

    purse = int(state["purse"])
    if amount < 1:
        raise ValueError("Bet must be at least 1 mon.")
    if amount > purse:
        raise ValueError("You do not have enough to make that bet.")

    gen = rng or random.Random()
    d1, d2 = _roll_dice(gen)

    state["pot"] = amount
    state["dice1"] = d1
    state["dice2"] = d2
    state["phase"] = "guess"
    state["message"] = "The dealer covers the dice. Call CHO (even) or HAN (odd)."
    return state


def make_guess(state: dict[str, Any], guess: str) -> dict[str, Any]:
    if state["phase"] != "guess":
        raise ValueError("Choose CHO or HAN after placing a bet.")
    choice = guess.strip().upper()
    if choice not in ("CHO", "HAN"):
        raise ValueError('Please enter either "CHO" or "HAN".')

    state = deepcopy(state)
    d1 = int(state["dice1"])
    d2 = int(state["dice2"])
    pot = int(state["pot"])
    purse = int(state["purse"])
    correct = _correct_guess(d1, d2)
    won = choice == correct

    state["player_guess"] = choice
    state["correct_bet"] = correct
    state["won"] = won
    state["phase"] = "reveal"

    if won:
        fee = pot // HOUSE_FEE_RATE
        purse = purse + pot - fee
        state["fee"] = fee
        state["message"] = f"You won {pot} mon! House fee: {fee} mon."
    else:
        purse -= pot
        state["fee"] = 0
        state["message"] = "You lost!"

    state["purse"] = purse
    if purse <= 0:
        state["purse"] = 0
        state["phase"] = "broke"
        state["message"] = "You have run out of money!"
    return state


def reset_purse(state: dict[str, Any]) -> dict[str, Any]:
    fresh = initial_state()
    return fresh


def dice_labels(d1: int, d2: int) -> dict[str, str]:
    return {
        "dice1_label": JAPANESE_NUMBERS[d1],
        "dice2_label": JAPANESE_NUMBERS[d2],
        "total": str(d1 + d2),
        "parity": "even" if (d1 + d2) % 2 == 0 else "odd",
    }
