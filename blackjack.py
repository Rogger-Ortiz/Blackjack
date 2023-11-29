import json
import PySimpleGUI as sg
import random
import os
os.system("pip install pysimplegui")

theme = "DarkBrown1"
sg.theme(theme)

winner = []
players = []
house = None
amt = 1


class Player:
    def __init__(self, name, hand, cards):
        self.name = name
        self.hand = hand
        self.cards = cards


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


def RightSide(turn_player: Player):
    playerHand = [[]]
    otherHands = [[]]
    for card in turn_player.cards:
        playerHand[0].append(sg.Image(card, size=(167, 224)))
        pass
    for i in range(len(players)):
        if not players[i] == turn_player:
            otherHands[0].append(sg.Text(players[i].name+":"))
            for j in range(len(players[i].hand)):
                if j == 0:
                    otherHands[0].append(
                        sg.Image(players[i].cards[j], size=(167, 224), pad=(0, 0)))
                    continue
                otherHands[0].append(
                    sg.Image("deck\\Back.png", size=(167, 224)))
            if not turn_player == players[-1]:
                if not i == len(players)-1:
                    otherHands[0].append(sg.VSeparator())
            else:
                if not i == len(players)-2:
                    otherHands[0].append(sg.VSeparator())
    sgRightSide = [[sg.Column(playerHand, justification='center')], [sg.HSeparator()],
                   [sg.Column(otherHands)]]
    return sgRightSide


def giveCard(user, cards):
    card = random.sample(cards, 1)[0]
    loc = cards.index(card)
    cards.pop(loc)
    user.hand.append(card)
    suit = random.randint(1, 4)
    match suit:
        case 1:
            user.cards.append(f"deck\\Clubs\\{str(card)}Cl.png")
        case 2:
            user.cards.append(f"deck\\Diamonds\\{str(card)}Da.png")
        case 3:
            user.cards.append(f"deck\\Hearts\\{str(card)}He.png")
        case 4:
            user.cards.append(f"deck\\Spades\\{str(card)}Sp.png")


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
    [sg.Button("PvP"), sg.Button("PvHouse")]
]
window = sg.Window(title="Initializing...", layout=layout,
                   size=(1920, 1080), element_justification='c', finalize=True, resizable=True)
window.maximize()
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
        [sg.Button("Two"), sg.Button("Three"), sg.Button("Four")]
    ]
    window = sg.Window(title="Initializing...",
                       layout=layout, size=(1920, 1080), element_justification='c', finalize=True, resizable=True)
    window.maximize()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit()
        else:
            match event:
                case "Two":
                    amt = 2
                    break
                case "Three":
                    amt = 3
                    break
                case "Four":
                    amt = 4
                    break
    window.close()
    layoutArr = []
    layoutArr.append(sg.Text("Please enter your names!"))
    for i in range(amt):
        layoutArr.append([sg.Multiline(key=f'pvpname{i}')])
    layoutArr.append(sg.Button("Submit"))
    layout = [layoutArr]
    window = sg.Window(title="Initializing...",
                       layout=layout, size=(1920, 1080), element_justification='c', finalize=True, resizable=True)
    window.maximize()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit()
        if event == "Submit":
            print("Submitted")
            for i in range(amt):
                players.append(Player(values[f"pvpname{i}"], [], []))

            break

if mode == "PvHouse":
    layout = [
        [sg.Text(f"Welcome! What is your name?")],
        [sg.Multiline(key="pvhname"), sg.Button("Submit")]
    ]
    window = sg.Window(title="Initializing...",
                       layout=layout, size=(1920, 1080), element_justification='c', finalize=True, resizable=True)
    window.maximize()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit()
        if event == "Submit":
            p1 = Player(values["pvhname"], [], [])
            house = Player("House", [], [])
            players = [p1, house]
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
        # if mode != "PvP":
        #     giveCard(house, deck)

bj = False
fcc = False

response = ""
playerPass = 0
if not bj:
    for player in players:
        while True:
            if player == house:
                break
            leftCol = [
                [sg.Text(
                    f"({player.name}) You have {total(player.hand)}")],
                [sg.Text(f"({player.name}) Add another card?")],
                [sg.Button("Hit"), sg.Button("Pass")],
            ]

            rightCol = RightSide(player)

            layout = [
                [
                    sg.Column(leftCol),
                    sg.VSeparator(),
                    sg.Column(rightCol),
                ]
            ]
            window = sg.Window(title="Blackjack",
                               layout=layout, size=(1920, 1080), element_justification='c', finalize=True, resizable=True)
            window.maximize()
            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED:
                    exit()
                if event == "Hit" or event == "Pass":
                    match event:
                        case "Hit":
                            response = "yes"
                            window.close()
                            break
                        case "Pass":
                            response = "no"
                            window.close()
                            break
            if response == "no":
                break
            else:
                giveCard(player, deck)
                if total(player.hand) > 21:
                    leftCol = [
                        [sg.Text(
                            f"({player.name}) You have {total(player.hand)} (hand: {player.hand})")],
                        [sg.Text(
                            f"({player.name}) You busted with {total(player.hand)}! (Hand: {player.hand})")],
                        [sg.Button("Pass Turn")],
                    ]

                    rightCol = RightSide(player)

                    layout = [
                        [
                            sg.Column(leftCol),
                            sg.VSeparator(),
                            sg.Column(rightCol),
                        ]
                    ]
                    window = sg.Window(title="Blackjack",
                                       layout=layout, size=(1920, 1080), element_justification='c', finalize=True, resizable=True)
                    window.maximize()
                    while True:
                        event, values = window.read()
                        if event == "Pass Turn":
                            window.close()
                            playerPass = 1
                            break
                if playerPass:
                    playerPass = 0
                    break
        if len(winner) > 0:
            break

if mode != "PvP" and not bj:
    htotal = total(house.hand)
    housePass = 0
    while htotal < 21:
        leftCol = [
            [sg.Text(
                f"({house.name}) You have {total(house.hand)} (hand: {house.hand})")],
            [sg.Text(f"({house.name}) Add another card?")],
            [sg.Button("Continue")],
        ]

        rightCol = RightSide(house)

        layout = [
            [
                sg.Column(leftCol),
                sg.VSeparator(),
                sg.Column(rightCol),
            ]
        ]
        window = sg.Window(title="Blackjack", layout=layout,
                           size=(1920, 1080), element_justification='c', finalize=True, resizable=True)
        window.maximize()
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                exit()
            if event == "Continue":
                needed = 21 - htotal
                if needed > 4:
                    giveCard(house, deck)
                else:
                    housePass = 1
                    window.close()
                    break
                window.close()
                if total(house.hand) > 21:
                    leftCol = [
                        [sg.Text(
                            f"({house.name}) You have {total(house.hand)} (hand: {house.hand})")],
                        [sg.Text(
                            f"({house.name}) has busted with {total(house.hand)}! (Hand: {house.hand})")],
                        [sg.Button("Pass Turn")],
                    ]

                    rightCol = RightSide(house)

                    layout = [
                        [
                            sg.Column(leftCol),
                            sg.VSeparator(),
                            sg.Column(rightCol),
                        ]
                    ]
                    window = sg.Window(title="Blackjack",
                                       layout=layout, size=(1920, 1080), element_justification='c', finalize=True, resizable=True)
                    window.maximize()
                    while True:
                        event, values = window.read()
                        if event == "Pass Turn":
                            window.close()
                            playerPass = 1
                            break
                    housePass = 1
                    window.close()
                    break
                else:
                    htotal = total(house.hand)
                    window.close()
                    break
        if housePass:
            window.close()
            housePass = 0
            break

    # players.append(house)

if not fcc and not bj:
    for player in players:
        if total(player.hand) <= 21:
            if len(winner) > 0:
                if total(player.hand) > total(winner[0].hand):
                    winner.clear()
                    winner.append(player)
                    continue
                if total(player.hand) == total(winner[0].hand):
                    if len(player.hand) < len(winner[0].hand):
                        winner.clear()
                        winner.append(player)
                    elif len(player.hand) == len(winner[0].hand):
                        winner.append(player)

            else:
                winner.append(player)
            if len(player.hand) == 5:
                winner.clear()
                winner.append(player)
                break

for player in winner:
    file = open("leaderboard.json", "r+")
    data = json.load(file)
    try:
        amt = data[player.name]
        amt += 1
        entry = f"{{\"{player.name}\": {amt}}}"
        newEntry = json.loads(entry)
        data.update(newEntry)
        file.truncate(0)
        file.seek(0)
        json.dump(data, file)
        file.close()
    except KeyError:
        entry = f"{{\"{player.name}\": 1}}"
        newEntry = json.loads(entry)
        data.update(newEntry)
        file.truncate(0)
        file.seek(0)
        json.dump(data, file)
    file.close()

if len(winner) > 0:
    file = open("leaderboard.json", "r+")
    data = json.load(file)
    lbStr = ""
    for key in data:
        lbStr += f"{key} - {data[key]}\n"
    file.close()

    leftCol = []
    for player in winner:
        leftCol.append(
            [sg.Text(f"{player.name} wins with {total(player.hand)}!")])
    leftCol.append([sg.Text(f"Total = {total(player.hand)}")])
    leftCol.append([sg.Button("Continue")])

    rightCol = [
        [sg.Text(lbStr)]
    ]

    layout = [
        [
            sg.Column(leftCol),
            sg.VSeparator(),
            sg.Column(rightCol),
        ]
    ]
    window = sg.Window(title="Blackjack", layout=layout,
                       size=(1920, 1080), element_justification='c', finalize=True, resizable=True)
    window.maximize()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Continue":
            exit()

if len(winner) == 0:
    leftCol = [
        [sg.Text(f"Nobody wins!")],
        [sg.Button("Continue")],
    ]

    rightCol = [
        [sg.Text("...do you not know how to play???")]
    ]

    layout = [
        [
            sg.Column(leftCol),
            sg.VSeparator(),
            sg.Column(rightCol),
        ]
    ]
    window = sg.Window(title="Blackjack", layout=layout,
                       size=(1920, 1080), element_justification='c', finalize=True, resizable=True)
    window.maximize()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Continue":
            exit()
