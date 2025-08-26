import random
import tkinter as tk
import heapq
from collections import deque
import time


# initializes a pyraminx in a solved state
def initialize():
    colors = ['red', 'green', 'blue', 'yellow']
    faces = ['a', 'b', 'c', 'd']
    pyraminx = {}
    for i in range(4):
        for j in range(16):
            pyraminx[faces[i] + str(j)] = colors[i]
    return pyraminx


# handles all GUI elements for the program
def display(pyraminx):
    root = tk.Tk()
    root.title("Pyraminx Visualizer")
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack()

    def drawTriangle(x, y, size, color, orientation):
        if orientation == "u":
            canvas.create_polygon(x, y, x + size, y, x + size / 2, y - size * 0.866, fill=color, outline='black')
        else:
            canvas.create_polygon(x, y - size * 0.866, x + size, y - size * 0.866, x + size / 2, y, fill=color,
                                  outline='black')

    def drawFace(start_x, start_y, face, inverted=False):
        size = 50
        nodes = [
            (3, 0, "u", 0),
            (2, 1, "u", 1), (3, 1, "d", 2), (4, 1, "u", 3),
            (1, 2, "u", 4), (2, 2, "d", 5), (3, 2, "u", 6), (4, 2, "d", 7), (5, 2, "u", 8),
            (0, 3, "u", 9), (1, 3, "d", 10), (2, 3, "u", 11), (3, 3, "d", 12), (4, 3, "u", 13), (5, 3, "d", 14),
            (6, 3, "u", 15)
        ]
        for col, row, orientation, index in nodes:
            color = pyraminx[face + str(index)]
            if inverted:
                x = start_x + (6 - col) * size * 0.5
                y = start_y - row * size * 0.866
                orientation = "d" if orientation == "u" else "u"
            else:
                x = start_x + col * size * 0.5
                y = start_y + row * size * 0.866
            drawTriangle(x, y, size, color, orientation)

    def updateDisplay():
        canvas.delete("all")
        drawFace(300, 500, 'a', inverted=True)
        drawFace(300, 194, 'b')
        drawFace(198, 372, 'c')
        drawFace(402, 372, 'd')

    def randomizeGUI():
        nonlocal pyraminx
        try:
            numRotations = int(rotationEntry.get())
        except ValueError:
            numRotations = 0
        randomize(pyraminx, numRotations)
        updateDisplay()

    def reset():
        nonlocal pyraminx
        pyraminx = initialize()
        updateDisplay()

    def solveGUI():
        nonlocal pyraminx
        start = time.time()
        solution = aStar(pyraminx)
        end = time.time()
        length = end - start
        timeLabel.config(text=f"Solved in {length:.2f} seconds")
        if solution:
            animateSolution(solution)

    def animateSolution(solution):
        def animateStep(moves):
            if not moves:
                return
            move = moves.popleft()
            globals()[move](pyraminx)
            updateDisplay()
            root.after(1000, animateStep, moves)

        moves = deque(solution)
        root.after(1000, animateStep, moves)

    updateDisplay()

    rotationEntry = tk.Entry(root, width=4, font=("Arial", 14))
    rotationEntry.place(x=270, y=150)
    rotationEntry.insert(0, "5")
    randomizeButton = tk.Button(root, text="Perform n Rotations:", command=randomizeGUI, bg="orange")
    randomizeButton.place(x=150, y=150)
    solveButton = tk.Button(root, text="Solve", command=solveGUI, bg="orange")
    solveButton.place(x=150, y=185)
    resetButton = tk.Button(root, text="Reset", command=reset, bg="orange")
    resetButton.place(x=200, y=185)
    timeLabel = tk.Label(root, text="", font=("Arial", 12))
    timeLabel.place(x=150, y=220)

    root.mainloop()


# original rotation functions: all rotations are clockwise when vertex is pointing toward user, number indicates level
def abc1(pyraminx):
    temp = pyraminx["a15"]
    pyraminx["a15"] = pyraminx["b9"]
    pyraminx["b9"] = pyraminx["c0"]
    pyraminx["c0"] = temp
    return pyraminx


def abc2(pyraminx):
    temp1 = pyraminx["a8"]
    temp2 = pyraminx["a14"]
    temp3 = pyraminx["a13"]
    pyraminx["a8"] = pyraminx["b11"]
    pyraminx["a14"] = pyraminx["b10"]
    pyraminx["a13"] = pyraminx["b4"]
    pyraminx["b11"] = pyraminx["c1"]
    pyraminx["b10"] = pyraminx["c2"]
    pyraminx["b4"] = pyraminx["c13"]
    pyraminx["c1"] = temp1
    pyraminx["c2"] = temp2
    pyraminx["c3"] = temp3
    return pyraminx


def abc3(pyraminx):
    temp1 = pyraminx["a3"]
    temp2 = pyraminx["a7"]
    temp3 = pyraminx["a6"]
    temp4 = pyraminx["a12"]
    temp5 = pyraminx["a11"]
    pyraminx["a3"] = pyraminx["b13"]
    pyraminx["a7"] = pyraminx["b12"]
    pyraminx["a6"] = pyraminx["b6"]
    pyraminx["a12"] = pyraminx["b5"]
    pyraminx["a11"] = pyraminx["b1"]
    pyraminx["b13"] = pyraminx["c4"]
    pyraminx["b12"] = pyraminx["c5"]
    pyraminx["b6"] = pyraminx["c6"]
    pyraminx["b5"] = pyraminx["c7"]
    pyraminx["b1"] = pyraminx["c8"]
    pyraminx["c4"] = temp1
    pyraminx["c5"] = temp2
    pyraminx["c6"] = temp3
    pyraminx["c7"] = temp4
    pyraminx["c8"] = temp5
    return pyraminx


def abd1(pyraminx):
    temp = pyraminx["a9"]
    pyraminx["a9"] = pyraminx["d0"]
    pyraminx["d0"] = pyraminx["b15"]
    pyraminx["b15"] = temp
    return pyraminx


def abd2(pyraminx):
    temp1 = pyraminx["a11"]
    temp2 = pyraminx["a10"]
    temp3 = pyraminx["a4"]
    pyraminx["a11"] = pyraminx["d1"]
    pyraminx["a10"] = pyraminx["d2"]
    pyraminx["a4"] = pyraminx["d3"]
    pyraminx["d1"] = pyraminx["b8"]
    pyraminx["d2"] = pyraminx["b14"]
    pyraminx["d3"] = pyraminx["b13"]
    pyraminx["b8"] = temp1
    pyraminx["b14"] = temp2
    pyraminx["b13"] = temp3
    return pyraminx


def abd3(pyraminx):
    temp1 = pyraminx["a13"]
    temp2 = pyraminx["a12"]
    temp3 = pyraminx["a6"]
    temp4 = pyraminx["a5"]
    temp5 = pyraminx["a1"]
    pyraminx["a13"] = pyraminx["d4"]
    pyraminx["a12"] = pyraminx["d5"]
    pyraminx["a6"] = pyraminx["d6"]
    pyraminx["a5"] = pyraminx["d7"]
    pyraminx["a1"] = pyraminx["d8"]
    pyraminx["d4"] = pyraminx["b3"]
    pyraminx["d5"] = pyraminx["b7"]
    pyraminx["d6"] = pyraminx["b6"]
    pyraminx["d7"] = pyraminx["b12"]
    pyraminx["d8"] = pyraminx["b11"]
    pyraminx["b3"] = temp1
    pyraminx["b7"] = temp2
    pyraminx["b6"] = temp3
    pyraminx["b12"] = temp4
    pyraminx["b11"] = temp5
    return pyraminx


def acd1(pyraminx):
    temp = pyraminx["a0"]
    pyraminx["a0"] = pyraminx["c15"]
    pyraminx["c15"] = pyraminx["d9"]
    pyraminx["d9"] = temp
    return pyraminx


def acd2(pyraminx):
    temp1 = pyraminx["a1"]
    temp2 = pyraminx["a2"]
    temp3 = pyraminx["a3"]
    pyraminx["a1"] = pyraminx["c8"]
    pyraminx["a2"] = pyraminx["c14"]
    pyraminx["a3"] = pyraminx["c13"]
    pyraminx["c8"] = pyraminx["d11"]
    pyraminx["c14"] = pyraminx["d10"]
    pyraminx["c13"] = pyraminx["d4"]
    pyraminx["d11"] = temp1
    pyraminx["d10"] = temp2
    pyraminx["d4"] = temp3
    return pyraminx


def acd3(pyraminx):
    temp1 = pyraminx["a4"]
    temp2 = pyraminx["a5"]
    temp3 = pyraminx["a6"]
    temp4 = pyraminx["a7"]
    temp5 = pyraminx["a8"]
    pyraminx["a4"] = pyraminx["c3"]
    pyraminx["a5"] = pyraminx["c7"]
    pyraminx["a6"] = pyraminx["c6"]
    pyraminx["a7"] = pyraminx["c12"]
    pyraminx["a8"] = pyraminx["c11"]
    pyraminx["c3"] = pyraminx["d13"]
    pyraminx["c7"] = pyraminx["d12"]
    pyraminx["c6"] = pyraminx["d6"]
    pyraminx["c12"] = pyraminx["d5"]
    pyraminx["c11"] = pyraminx["d1"]
    pyraminx["d13"] = temp1
    pyraminx["d12"] = temp2
    pyraminx["d6"] = temp3
    pyraminx["d5"] = temp4
    pyraminx["d1"] = temp5
    return pyraminx


def bcd1(pyraminx):
    temp = pyraminx["b0"]
    pyraminx["b0"] = pyraminx["d15"]
    pyraminx["d15"] = pyraminx["c9"]
    pyraminx["c9"] = temp
    return pyraminx


def bcd2(pyraminx):
    temp1 = pyraminx["b1"]
    temp2 = pyraminx["b2"]
    temp3 = pyraminx["b3"]
    pyraminx["b1"] = pyraminx["d8"]
    pyraminx["b2"] = pyraminx["d14"]
    pyraminx["b3"] = pyraminx["d13"]
    pyraminx["d8"] = pyraminx["c11"]
    pyraminx["d14"] = pyraminx["c10"]
    pyraminx["d13"] = pyraminx["c4"]
    pyraminx["c11"] = temp1
    pyraminx["c10"] = temp2
    pyraminx["c4"] = temp3
    return pyraminx


def bcd3(pyraminx):
    temp1 = pyraminx["b4"]
    temp2 = pyraminx["b5"]
    temp3 = pyraminx["b6"]
    temp4 = pyraminx["b7"]
    temp5 = pyraminx["b8"]
    pyraminx["b4"] = pyraminx["d3"]
    pyraminx["b5"] = pyraminx["d7"]
    pyraminx["b6"] = pyraminx["d6"]
    pyraminx["b7"] = pyraminx["d12"]
    pyraminx["b8"] = pyraminx["d11"]
    pyraminx["d3"] = pyraminx["c13"]
    pyraminx["d7"] = pyraminx["c12"]
    pyraminx["d6"] = pyraminx["c6"]
    pyraminx["d12"] = pyraminx["c5"]
    pyraminx["d11"] = pyraminx["c1"]
    pyraminx["c13"] = temp1
    pyraminx["c12"] = temp2
    pyraminx["c6"] = temp3
    pyraminx["c5"] = temp4
    pyraminx["c1"] = temp5
    return pyraminx


# reverse rotation functions: all rotations are counterclockwise when vertex is pointing toward user
def abc1r(pyraminx):
    temp = pyraminx["a15"]
    pyraminx["a15"] = pyraminx["c0"]
    pyraminx["c0"] = pyraminx["b9"]
    pyraminx["b9"] = temp
    return pyraminx


def abc2r(pyraminx):
    temp1 = pyraminx["a8"]
    temp2 = pyraminx["a14"]
    temp3 = pyraminx["a13"]
    pyraminx["a8"] = pyraminx["c1"]
    pyraminx["a14"] = pyraminx["c2"]
    pyraminx["a13"] = pyraminx["c3"]
    pyraminx["c1"] = pyraminx["b11"]
    pyraminx["c2"] = pyraminx["b10"]
    pyraminx["c3"] = pyraminx["b4"]
    pyraminx["b11"] = temp1
    pyraminx["b10"] = temp2
    pyraminx["b4"] = temp3
    return pyraminx


def abc3r(pyraminx):
    temp1 = pyraminx["a3"]
    temp2 = pyraminx["a7"]
    temp3 = pyraminx["a6"]
    temp4 = pyraminx["a12"]
    temp5 = pyraminx["a11"]
    pyraminx["a3"] = pyraminx["c4"]
    pyraminx["a7"] = pyraminx["c5"]
    pyraminx["a6"] = pyraminx["c6"]
    pyraminx["a12"] = pyraminx["c7"]
    pyraminx["a11"] = pyraminx["c8"]
    pyraminx["c4"] = pyraminx["b13"]
    pyraminx["c5"] = pyraminx["b12"]
    pyraminx["c6"] = pyraminx["b6"]
    pyraminx["c7"] = pyraminx["b5"]
    pyraminx["c8"] = pyraminx["b1"]
    pyraminx["b13"] = temp1
    pyraminx["b12"] = temp2
    pyraminx["b6"] = temp3
    pyraminx["b5"] = temp4
    pyraminx["b1"] = temp5
    return pyraminx


def abd1r(pyraminx):
    temp = pyraminx["a9"]
    pyraminx["a9"] = pyraminx["b15"]
    pyraminx["b15"] = pyraminx["d0"]
    pyraminx["d0"] = temp
    return pyraminx


def abd2r(pyraminx):
    temp1 = pyraminx["a11"]
    temp2 = pyraminx["a10"]
    temp3 = pyraminx["a4"]
    pyraminx["a11"] = pyraminx["b8"]
    pyraminx["a10"] = pyraminx["b14"]
    pyraminx["a4"] = pyraminx["b13"]
    pyraminx["b8"] = pyraminx["d1"]
    pyraminx["b14"] = pyraminx["d2"]
    pyraminx["b13"] = pyraminx["d3"]
    pyraminx["d1"] = temp1
    pyraminx["d2"] = temp2
    pyraminx["d3"] = temp3
    return pyraminx


def abd3r(pyraminx):
    temp1 = pyraminx["a13"]
    temp2 = pyraminx["a12"]
    temp3 = pyraminx["a6"]
    temp4 = pyraminx["a5"]
    temp5 = pyraminx["a1"]
    pyraminx["a13"] = pyraminx["b3"]
    pyraminx["a12"] = pyraminx["b7"]
    pyraminx["a6"] = pyraminx["b6"]
    pyraminx["a5"] = pyraminx["b12"]
    pyraminx["a1"] = pyraminx["b11"]
    pyraminx["b3"] = pyraminx["d4"]
    pyraminx["b7"] = pyraminx["d5"]
    pyraminx["b6"] = pyraminx["d6"]
    pyraminx["b12"] = pyraminx["d7"]
    pyraminx["b11"] = pyraminx["d8"]
    pyraminx["d4"] = temp1
    pyraminx["d5"] = temp2
    pyraminx["d6"] = temp3
    pyraminx["d7"] = temp4
    pyraminx["d8"] = temp5
    return pyraminx


def acd1r(pyraminx):
    temp = pyraminx["a0"]
    pyraminx["a0"] = pyraminx["d9"]
    pyraminx["d9"] = pyraminx["c15"]
    pyraminx["c15"] = temp
    return pyraminx


def acd2r(pyraminx):
    temp1 = pyraminx["a1"]
    temp2 = pyraminx["a2"]
    temp3 = pyraminx["a3"]
    pyraminx["a1"] = pyraminx["d11"]
    pyraminx["a2"] = pyraminx["d10"]
    pyraminx["a3"] = pyraminx["d4"]
    pyraminx["d11"] = pyraminx["c8"]
    pyraminx["d10"] = pyraminx["c14"]
    pyraminx["d4"] = pyraminx["c13"]
    pyraminx["c8"] = temp1
    pyraminx["c14"] = temp2
    pyraminx["c13"] = temp3
    return pyraminx


def acd3r(pyraminx):
    temp1 = pyraminx["a4"]
    temp2 = pyraminx["a5"]
    temp3 = pyraminx["a6"]
    temp4 = pyraminx["a7"]
    temp5 = pyraminx["a8"]
    pyraminx["a4"] = pyraminx["d13"]
    pyraminx["a5"] = pyraminx["d12"]
    pyraminx["a6"] = pyraminx["d6"]
    pyraminx["a7"] = pyraminx["d5"]
    pyraminx["a8"] = pyraminx["d1"]
    pyraminx["d13"] = pyraminx["c3"]
    pyraminx["d12"] = pyraminx["c7"]
    pyraminx["d6"] = pyraminx["c6"]
    pyraminx["d5"] = pyraminx["c12"]
    pyraminx["d1"] = pyraminx["c11"]
    pyraminx["c3"] = temp1
    pyraminx["c7"] = temp2
    pyraminx["c6"] = temp3
    pyraminx["c12"] = temp4
    pyraminx["c11"] = temp5
    return pyraminx


def bcd1r(pyraminx):
    temp = pyraminx["b0"]
    pyraminx["b0"] = pyraminx["c9"]
    pyraminx["c9"] = pyraminx["d15"]
    pyraminx["d15"] = temp
    return pyraminx


def bcd2r(pyraminx):
    temp1 = pyraminx["b1"]
    temp2 = pyraminx["b2"]
    temp3 = pyraminx["b3"]
    pyraminx["b1"] = pyraminx["c11"]
    pyraminx["b2"] = pyraminx["c10"]
    pyraminx["b3"] = pyraminx["c4"]
    pyraminx["c11"] = pyraminx["d8"]
    pyraminx["c10"] = pyraminx["d14"]
    pyraminx["c4"] = pyraminx["d13"]
    pyraminx["d8"] = temp1
    pyraminx["d14"] = temp2
    pyraminx["d13"] = temp3
    return pyraminx


def bcd3r(pyraminx):
    temp1 = pyraminx["b4"]
    temp2 = pyraminx["b5"]
    temp3 = pyraminx["b6"]
    temp4 = pyraminx["b7"]
    temp5 = pyraminx["b8"]
    pyraminx["b4"] = pyraminx["c13"]
    pyraminx["b5"] = pyraminx["c12"]
    pyraminx["b6"] = pyraminx["c6"]
    pyraminx["b7"] = pyraminx["c5"]
    pyraminx["b8"] = pyraminx["c1"]
    pyraminx["c13"] = pyraminx["d3"]
    pyraminx["c12"] = pyraminx["d7"]
    pyraminx["c6"] = pyraminx["d6"]
    pyraminx["c5"] = pyraminx["d12"]
    pyraminx["c1"] = pyraminx["d11"]
    pyraminx["d3"] = temp1
    pyraminx["d7"] = temp2
    pyraminx["d6"] = temp3
    pyraminx["d12"] = temp4
    pyraminx["d11"] = temp5
    return pyraminx


# performs num random clockwise rotations on the pyraminx
def randomize(pyraminx, num):
    rotations = [abc1, abc2, abc3, abd1, abd2, abd3, acd1, acd2, acd3, bcd1, bcd2, bcd3]
    for i in range(num):
        random.choice(rotations)(pyraminx)


# returns heuristic value: maximum number of colors on any single face - 1
def heuristic(pyraminx):
    faces = {face: set() for face in 'abcd'}
    for piece, color in pyraminx.items():
        faces[piece[0]].add(color)
    return max(len(colors) for colors in faces.values()) - 1


# returns a new pyraminx after a move has been applied without altering original
def applyMove(pyraminx, move):
    newPyraminx = pyraminx.copy()
    move(newPyraminx)
    return newPyraminx


# attempts to find the best path to solve the pyraminx
def aStar(initialPyraminx):
    openNodes = []
    closedNodes = set()
    initialState = (0, 0, tuple(initialPyraminx.items()), [])
    heapq.heappush(openNodes, initialState)
    moveCount = 0
    nodesExpanded = 0


    while openNodes:
        f, depth, currentTuple, moves = heapq.heappop(openNodes)
        current = dict(currentTuple)
        # check if solved
        if heuristic(current) == 0:
            print(f"Total nodes expanded: {nodesExpanded}")
            return moves
        if currentTuple in closedNodes:
            continue
        closedNodes.add(currentTuple)
        nodesExpanded += 1
        reversedRotations = [abc1r, abc2r, abc3r, abd1r, abd2r, abd3r, acd1r, acd2r, acd3r, bcd1r, bcd2r, bcd3r]
        for move in reversedRotations:
            neighbor = applyMove(current, move)
            neighborTuple = tuple(neighbor.items())
            if neighborTuple not in closedNodes:
                newMoves = moves + [move.__name__]
                h = heuristic(neighbor)
                g = len(newMoves)
                f = g + h
                moveCount += 1
                newState = (f, g, neighborTuple, newMoves)
                heapq.heappush(openNodes, newState)
    return None


def main():
    pyraminx = initialize()
    display(pyraminx)


if __name__ == "__main__":
    main()
