import tkinter
from graphics import *
import json


def gameWindow(titles, round):
    win = GraphWin("Jeopardy", 1602, 1002)
    win.setBackground("light blue")
    
    boxes = []
    labels = []

    for i in range(6):
        titlecard = Rectangle(Point((int(i))*267, 0), Point((int(i)+1)*267, 167))
        titlecard.setFill("Blue")
        titlecard.draw(win)
        title_label = Text(Point((int(i)+0.5)*267, (0.5)*167), titles[i])
        title_label.setStyle("bold")
        title_label.setSize(32)
        title_label.setFill("white")
        title_label.draw(win)


        for j in range(5):
            quesiton_card = Rectangle(Point((int(i))*267, (int(j)+1)*167), Point((int(i)+1)*267, (int(j)+2)*167))
            quesiton_card.setFill("Blue")
            quesiton_card.draw(win)
            quesiton__label = Text(Point((int(i)+0.5)*267, (int(j)+1.5)*167), f"${(float(j)+1)*200*round}")
            quesiton__label.setStyle("bold")
            quesiton__label.setSize(32)
            quesiton__label.setFill("#FFFF00")
            quesiton__label.draw(win)

            boxes.append(quesiton_card)
            labels.append(quesiton__label)

            divider = Rectangle(Point(0, (int(j)+1)*167 - 3), Point(1602, (int(j)+1)*167 + 3))
            divider.setFill("Black")
            divider.draw(win)

        divider = Rectangle(Point((int(i) + 1)*267 - 3, 0), Point((int(i) + 1)*267 + 3, 1002))
        divider.setFill("Black")
        divider.draw(win)


    return win, boxes, labels


def clicked(click, rect):
    if not click:
        return False
    mx, my = click.getX(), click.getY()
    x1, y1 = rect.getP1().getX(), rect.getP1().getY()
    x2, y2 = rect.getP2().getX(), rect.getP2().getY()

    return (x1 < mx < x2) and (y1 < my < y2)

def question(question_data, title=""):
    win2 = GraphWin("Jeopardy", 1602, 1002)
    win2.setBackground("light blue")

    title_label = Text(Point(801, 90), title)
    title_label.setStyle("bold italic")
    title_label.setSize(32)
    title_label.setFill("black")
    title_label.draw(win2)

    question_label = Text(Point(801, 501), question_data[0])
    question_label.setStyle("bold")
    question_label.setSize(32)
    question_label.setFill("black")
    question_label.draw(win2)

    while True:
        click = win2.checkMouse()
        if click:
            break

    question_label.setText(question_data[1])

    while True:
        click = win2.checkMouse()
        if click:
            break

    win2.close()

def gameboard():
    file = open("questions.json", "r")
    data = json.load(file)
    keys = [list(data[0].keys()), list(data[1].keys())]

    questions_answered = []

    for i in range(2):
        win, boxes, labels = gameWindow(keys[i], int(i)+1)
        cond = True

        while cond:
            click = win.checkMouse()
            for j in range(len(boxes)):
                if clicked(click, boxes[j]):
                    boxes[j].undraw()
                    labels[j].undraw()
                    question(data[i][keys[i][int(j/5)]][j%5])
                    if j not in questions_answered:
                        questions_answered.append(j)
                    print(questions_answered)

            if len(questions_answered) >= 30:
                questions_answered = []
                cond = False
                win.close()

    print(data[2])
    question(data[2][1], title = data[2][0])

gameboard()
