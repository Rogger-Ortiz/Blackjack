import random
import time
import os
import PySimpleGUI as sg


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
players = []
house = None
amt = 1
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

#####################################

layout = [
    [sg.Text("PvP or PvHouse?")],
    [sg.Button("PvP"),sg.Button("PvHouse")]
]
window = sg.Window(title="Initializing...", layout=layout, margins= (400,400))
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        exit()
    if event == "PvP" or event == "PvHouse":
        match event:
            case "PvP":
                mode = "PvP"
                break
            case "PvHouse":
                mode = "PvHouse"
                break
        print("ERROR")
        break
window.close()
print(f"playing {mode}")

if mode == "PvP":
    layout = [
        [sg.Text(f"Playing {mode}, How many players?")],
        [sg.Button("Two"),sg.Button("Three"),sg.Button("Four")]
    ]
    window = sg.Window(title="Initializing...", layout=layout, margins= (400,400))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit()
        else:
            match event:
                case "Two":
                    amt=2
                    break
                case "Three":
                    amt=3
                    break
                case "Four":
                    amt=4
                    break
    window.close()
    layoutArr = []
    layoutArr.append(sg.Text("Please enter your names!"))
    for i in range(amt):
        layoutArr.append([sg.Multiline(key=f'pvpname{i}')])
    layoutArr.append(sg.Button("Submit"))
    layout = [layoutArr]
    window = sg.Window(title="Initializing...", layout=layout, margins= (400,400))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit()
        if event == "Submit":
            print("Submitted")
            for i in range(amt):
                players.append(Player(values[f"pvpname{i}"], []))
                
            break

if mode == "PvHouse":
    layout = [
        [sg.Text(f"Welcome! What is your name?")],
        [sg.Multiline(key="pvhname"),sg.Button("Submit")]
    ]
    window = sg.Window(title="Initializing...", layout=layout, margins= (400,400))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit()
        if event == "Submit":
            p1 = Player(values["pvhname"], [])
            house = Player("House", [])
            players = [p1]
            break

window.close()
print(f"With {amt} players")

if mode != "PvP" and mode != "PvHouse":
    print("Error with gamemode")
    exit()

############ Core Code ################

for i in range(0, 2):
    for player in players:
        giveCard(player, deck)
        if mode != "PvP":
            giveCard(house, deck)

bj = False
fcc = False

for player in players:
    insta = total(player.hand)
    if insta == 21:
        winner.append(player)
        bj = True
if mode != "PvP":
    insta = total(house.hand)
    if insta == 21:
        winner.append(house)
        bj = True

#######################################

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

if mode != "PvP" and not bj:
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
