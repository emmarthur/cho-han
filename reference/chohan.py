"""Cho-Han reference — Al Sweigart, Big Book Project #15 (upstream CLI)."""

import random
import sys

JAPANESE_NUMBERS = {1: "ICHI", 2: "NI", 3: "SAN", 4: "SHI", 5: "GO", 6: "ROKU"}

purse = 5000
while True:
    print("You have", purse, "mon. How much do you bet? (or QUIT)")
    while True:
        pot = input("> ")
        if pot.upper() == "QUIT":
            sys.exit()
        elif not pot.isdecimal():
            print("Please enter a number.")
        elif int(pot) > purse:
            print("You do not have enough to make that bet.")
        else:
            pot = int(pot)
            break

    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)

    print("    CHO (even) or HAN (odd)?")
    while True:
        bet = input("> ").upper()
        if bet in ("CHO", "HAN"):
            break

    roll_is_even = (dice1 + dice2) % 2 == 0
    correct_bet = "CHO" if roll_is_even else "HAN"
    if bet == correct_bet:
        purse = purse + pot - (pot // 10)
    else:
        purse -= pot

    if purse == 0:
        sys.exit()
