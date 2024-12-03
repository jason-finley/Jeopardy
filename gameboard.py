import tkinter
from graphics import *
import json
from random import randint
from time import sleep


# images must be png
# image name examples: 11Q.png, 11A.png, 94A.png
# window size: 1602x1002


def gameWindow(titles, round): # Create a game window with categories and questions
    win = GraphWin("Jasonpardy", 1602, 1002)
    win.setBackground("light blue")

    boxes = []  # List to store question card objects (Rectangles)
    labels = []  # List to store labels on question card text objects

    # Create category title cards
    for i in range(6):
        titlecard = Rectangle(Point((int(i))*267, 0), Point((int(i)+1)*267, 167))
        titlecard.setFill("Blue")
        titlecard.draw(win)
        title_label = Text(Point((int(i)+0.5)*267, (0.5)*167), titles[i])
        title_label.setStyle("bold")
        title_label.setSize(26)
        title_label.setFill("white")
        title_label.draw(win)

        # Create question card objects for each question in the category
        for j in range(5):
            quesiton_card = Rectangle(Point((int(i))*267, (int(j)+1)*167), Point((int(i)+1)*267, (int(j)+2)*167))
            quesiton_card.setFill("Blue")
            quesiton_card.draw(win)
            quesiton__label = Text(Point((int(i)+0.5)*267, (int(j)+1.5)*167), f"${int((float(j)+1)*200*round)}")
            quesiton__label.setStyle("bold")
            quesiton__label.setSize(28)
            quesiton__label.setFill("#FFFF00")
            quesiton__label.draw(win)

            boxes.append(quesiton_card)
            labels.append(quesiton__label)

            # Add dividers between questions
            divider = Rectangle(Point(0, (int(j)+1)*167 - 3), Point(1602, (int(j)+1)*167 + 3))
            divider.setFill("Black")
            divider.draw(win)
        

        # Add dividers between categories
        divider = Rectangle(Point((int(i) + 1)*267 - 3, 0), Point((int(i) + 1)*267 + 3, 1002))
        divider.setFill("Black")
        divider.draw(win)


    return win, boxes, labels


def clicked(click, rect): # Check if a point (click) is within a given rectangle
    if not click:
        return False
    mx, my = click.getX(), click.getY()
    x1, y1 = rect.getP1().getX(), rect.getP1().getY()
    x2, y2 = rect.getP2().getX(), rect.getP2().getY()

    return (x1 < mx < x2) and (y1 < my < y2)


def question(question_data, title, column = None, row = None, daydub = False, fj = False): # Display question/answer window
    win2 = GraphWin("Jeopardy", 1602, 1002)
    win2.setBackground("light blue")

    # Display the title of the category with point value
    if not fj:
        points_str = str(row*200 + 200)
        title = title + "\n" + points_str
    title_label = Text(Point(801, 90), title)
    title_label.setStyle("bold italic")
    title_label.setSize(28)
    title_label.setFill("black")
    title_label.draw(win2)

    if daydub: # Check if chosen question is the daily double
        daydub_label = Text(Point(801, 501), "! ! ! DAILY ! ! !\n! ! ! DOUBLE ! ! !")
        daydub_label.setStyle("bold")
        daydub_label.setSize(36)
        daydub_label.setFill("black")
        daydub_label.draw(win2)

        while True:
            click = win2.checkMouse()
            if click:
                break

        daydub_label.undraw()

    # Display the question text and image if provided
    question_label = Text(Point(801, 501), question_data[0][1])
    question_label.setStyle("bold")
    question_label.setSize(28)
    question_label.setFill("black")
    question_label.draw(win2)

    if question_data[0][0] == True: # Load and display the image
        if not fj:
            image_dir = "images\\" + str(column + 1) + str(row + 1) + "Q.png"
        else:
            image_dir = "images\\FJQ.png"
        image = Image(Point(801, 420), image_dir)
        image.draw(win2)
        imgHeight = image.getHeight()
        dy = (((1002 - (420 + imgHeight/2)) / 2) + 420 + imgHeight/2) - 501
        question_label.move(0, dy)

    # Display question countdown
    count = 11
    count_label = Text(Point(1200, 90), str(count))
    count_label.setStyle("bold italic")
    count_label.setSize(36)
    count_label.setFill("red")
    count_label.draw(win2)

    # Wait for a click in the window
    while True:
        click = win2.checkMouse()
        if click:
            break
        elif count != 0:
            count -= 1
            count_label.setText(str(count))
        sleep(1)

    # Remove countdown
    count_label.undraw()

    # Delete image and return question label to center of window
    if question_data[0][0] == True:
        image.undraw()
        question_label.move(0, -1 * dy)

    # Display the answer text
    question_label.setText(question_data[1][1])

    if question_data[1][0] == True: # Load and display the image
        if not fj:
            image_dir = "images\\" + str(column + 1) + str(row + 1) + "A.png"
        else:
            image_dir = "images\\FJA.png"
        image = Image(Point(801, 420), image_dir)
        image.draw(win2)
        imgHeight = image.getHeight()
        dy = (((1002 - (420 + imgHeight/2)) / 2) + 420 + imgHeight/2) - 501
        question_label.move(0, dy)

    # Wait for a click in the window
    while True:
        click = win2.checkMouse()
        if click:
            break

    # Close the window after the user clicks
    win2.close()


def gameboard_main(): # Read questions from a JSON file
    file = open("temp_questions.json", "r")
    data = json.load(file)
    keys = list(data.keys())  # Store category title names as dict keys

    # Create game window with given categories and round number (round number currently set to 1)
    win, boxes, labels = gameWindow(keys, 1)
    questions_answered = set()
    daily_double_int = randint(0, 30)

    # Loop until all 30 questions in the round are answered
    while len(questions_answered) > 30:
        click = win.checkMouse()

        for j in range(30): # Check all 30 question object boxes if they have been clicked on
            if clicked(click, boxes[j]):
                boxes[j].undraw()
                labels[j].undraw()

                daydub = (j == daily_double_int) # Boolean if daily double

                question(data[keys[int(j/5)]][j%5], title=keys[int(j/5)], column=int(j/5), row=int(j%5), daydub=daydub) # Open question window

                questions_answered.add(j) # Add question index to answered list

    # Display the final question
    question(data[keys[-1]], title = keys[-1], fj=True)

    win.close() # Close round window


if __name__ == "__main__":
    gameboard_main()
