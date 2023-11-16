import random
import time
import os


class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand


os.system("pip install pysimplegui")


def total(hand):
    num = 0
    aces = []
    for card in hand:
        if isinstance(card, str):
            match card:
                case "A":
                    aces.append("A")
                case "J":
                    num = num + 10
                case "Q":
                    num = num + 10
                case "K":
                    num = num + 10
            continue
        num = num + card

    for ace in range(0, len(aces)):
        if num + 11 > 21:
            num = num + 1
        else:
            num = num + 11
    return num


def giveCard(user, cards):
    card = random.sample(cards, 1)[0]
    loc = cards.index(card)
    cards.pop(loc)
    user.hand.append(card)


winner = []
deck = ["A", "A", "A", "A",
        2, 2, 2, 2,
        3, 3, 3, 3,
        4, 4, 4, 4,
        5, 5, 5, 5,
        6, 6, 6, 6,
        7, 7, 7, 7,
        8, 8, 8, 8,
        9, 9, 9, 9,
        10, 10, 10, 10,
        "J", "J", "J", "J",
        "Q", "Q", "Q", "Q",
        "K", "K", "K", "K"]

players = []
mode = input("Type 1 to play against others, type 2 to play against the House: ")
if mode == "1":
    amt = 0
    while amt < 1 or amt > 6:
        amt = input("How many players? ")
        amt = int(amt)
    for i in range(1, amt + 1):
        players.append(Player(input(f"Welcome Player {i}! Please enter your name: "), []))
else:
    p1 = Player(input("Welcome! Enter your name: "), [])
    house = Player("House", [])
    players = [p1]

for i in range(0, 2):
    for player in players:
        giveCard(player, deck)
        if mode != "1":
            giveCard(house, deck)

bj = False
fcc = False

for player in players:
    insta = total(player.hand)
    if insta == 21:
        winner.append(player)
        bj = True
if mode != "1":
    insta = total(house.hand)
    if insta == 21:
        winner.append(house)
        bj = True

if not bj:
    for player in players:
        while True:
            print(f"({player.name}) You have {total(player.hand)} (hand: {player.hand})")
            response = input(f"({player.name}) Add another card? (yes/no): ")
            if response == "no":
                break
            else:
                giveCard(player, deck)
                if total(player.hand) > 21:
                    print(f"({player.name}) You busted with {total(player.hand)}! (Hand: {player.hand})")
                    break
                else:
                    if len(player.hand) == 5:
                        winner.append(player)
                        fcc = True
                        break
        os.system("cls")
        # print("-------------------------------------------------------------------")
        if len(winner) > 0:
            break

if mode != "1" and not bj:
    htotal = total(house.hand)
    while htotal < 21:
        print(f"(House) You have {total(house.hand)} (hand: {house.hand})")
        needed = 21 - htotal
        if needed > 4:
            print(f"(House) Add another card? (yes/no): yes")
            giveCard(house, deck)
        else:
            print(f"(House) Add another card? (yes/no): no")
            break
        if total(house.hand) > 21:
            print(f"The House has busted! (Hand: {house.hand})")
            break
        else:
            htotal = total(house.hand)
        time.sleep(1)

    print("-------------------------------------------------------------------")
    players.append(house)

if len(winner) > 0 and fcc:
    print(f"FIVE CARD CHARLIE!!! {winner[0].name} WINS!!! (Hand: {winner[0].hand})")

if len(winner) > 0 and bj:
    for player in winner:
        print(f"BLACKJACK!!! {player.name} WINS!!! (Hand: {player.hand})")

if not fcc and not bj:
    for player in players:
        if total(player.hand) <= 21:
            if len(winner) > 0:
                if total(player.hand) > total(winner[0].hand):
                    winner.clear()
                    winner.append(player)
                    continue
                if total(player.hand) == total(winner[0].hand):
                    winner.append(player)
            else:
                winner.append(player)

if not fcc and not bj:
    for player in winner:
        print(f"{player.name} wins! (Hand: {player.hand})")
        if mode != "1":
            print(f"House hand: {house.hand}")

while True:
    close = input("Type \"Quit\" to quit: ")
    if close.lower() == "quit":
        break
