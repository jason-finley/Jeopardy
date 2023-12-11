import tkinter
from graphics import *
import json


# images must be png
# image name examples: 11Q.png, 42A.png, 94A.png
# window size: 1602x1002


def gameWindow(titles, round):
    # Create a game window with categories and questions
    win = GraphWin("Jeopardy", 1602, 1002)
    win.setBackground("light blue")

    boxes = []  # List to store question cards (Rectangles)
    labels = []  # List to store labels on question cards (Text)

    # Create title cards for each category
    for i in range(6):
        titlecard = Rectangle(Point((int(i))*267, 0), Point((int(i)+1)*267, 167))
        titlecard.setFill("Blue")
        titlecard.draw(win)
        title_label = Text(Point((int(i)+0.5)*267, (0.5)*167), titles[i])
        title_label.setStyle("bold")
        title_label.setSize(28)
        title_label.setFill("white")
        title_label.draw(win)

        # Create question cards for each question in the category
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

def question(question_data, column, row, title=""):
    # Display a question or answer window
    win2 = GraphWin("Jeopardy", 1602, 1002)
    win2.setBackground("light blue")

    # Display the title of the category
    title_label = Text(Point(801, 90), title)
    title_label.setStyle("bold italic")
    title_label.setSize(28)
    title_label.setFill("black")
    title_label.draw(win2)

    # Display the question or answer text
    question_label = Text(Point(801, 501), question_data[0][1])
    question_label.setStyle("bold")
    question_label.setSize(28)
    question_label.setFill("black")
    question_label.draw(win2)

    if question_data[0][0] == True: # If it's a quesition with an image
        # Load and display the image
        image = Image(Point(801, 420), "images\\" + str(column + 1) + str(row + 1) + "Q.png")
        image.draw(win2)
        imgHeight = image.getHeight()
        dy = (((1002 - (420 + imgHeight/2)) / 2) + 420 + imgHeight/2) - 501
        question_label.move(0, dy)

    # Wait for a click in the window
    while True:
        click = win2.checkMouse()
        if click:
            break

    # If there was an image for question
    if question_data[0][0] == True:
        # Delete image and return question label to center of window
        image.undraw()
        question_label.move(0, -1 * dy)

    # Display the answer text
    question_label.setText(question_data[1][1])

    if question_data[1][0] == True: # If it's an answer with an image
        # Load and display the imgae
        image = Image(Point(801, 420), "images\\" + str(column + 1) + str(row + 1) + "A.png")
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


def gameboard():
    # read questions from a JSON file
    file = open("questions.json", "r")
    data = json.load(file)
    keys = [list(data[0].keys()), list(data[1].keys()), list(data[2].keys())]  # Store category title names as dict keys

    # Loop throught the categories and display the game window
    for i in range(2):
        win, boxes, labels = gameWindow(keys[i], int(i)+1)
        questions_answered = []

        # Loop until all 30 questions in the round are answered
        while len(questions_answered) < 30:
            click = win.checkMouse()
            for j in range(len(boxes)):
                if clicked(click, boxes[j]):
                    boxes[j].undraw()
                    labels[j].undraw()
                    question(data[i][keys[i][int(j/5)]][j%5], int((i*6) + (j/5)), j%5)
                    if j not in questions_answered:
                        questions_answered.append(j)

        win.close() # Close round window

    # Display the final question
    question(data[2][keys[2][0]][0], 17, 1, title = keys[2][0])

# Run the gameboard function to start the Jeopardy game
gameboard()
