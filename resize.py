import cv2
import os

size = (84, 112)

suit = "Clubs"
filedir = os.listdir(f"original\\{suit}")
for file in filedir:
    print(f"original\\{suit}\\{file}")
    img = cv2.imread(f"original\\{suit}\\{file}")
    new_img = cv2.resize(img, size)
    cv2.imwrite(f"deck\\{suit}\\{file}", new_img)

suit = "Diamonds"
filedir = os.listdir(f"original\\{suit}")
for file in filedir:
    print(f"original\\{suit}\\{file}")
    img = cv2.imread(f"original\\{suit}\\{file}")
    new_img = cv2.resize(img, size)
    cv2.imwrite(f"deck\\{suit}\\{file}", new_img)

suit = "Hearts"
filedir = os.listdir(f"original\\{suit}")
for file in filedir:
    print(f"original\\{suit}\\{file}")
    img = cv2.imread(f"original\\{suit}\\{file}")
    new_img = cv2.resize(img, size)
    cv2.imwrite(f"deck\\{suit}\\{file}", new_img)

suit = "Spades"
filedir = os.listdir(f"original\\{suit}")
for file in filedir:
    print(f"original\\{suit}\\{file}")
    img = cv2.imread(f"original\\{suit}\\{file}")
    new_img = cv2.resize(img, size)
    cv2.imwrite(f"deck\\{suit}\\{file}", new_img)

img = cv2.imread(f"original\\Back.png")
new_img = cv2.resize(img, size)
cv2.imwrite(f"deck\\Back.png", new_img)