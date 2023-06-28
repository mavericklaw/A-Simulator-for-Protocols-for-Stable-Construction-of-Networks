import random
from matplotlib import animation
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import networkx as nx
import matplotlib.pyplot as plt
import globals
from copy import copy, deepcopy
from PyQt5 import QtCore
import math


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        FigureCanvas.__init__(self)
        self.setParent(parent)
        self.figure = plt.figure()


    def plot(self):
        self.figure.clf()
        globals.pos = nx.spring_layout(globals.G)
        nx.draw_networkx_nodes(globals.G, globals.pos, node_size=700)
        nx.draw_networkx_labels(globals.G, globals.pos, globals.labels, font_size=16, font_color="yellow")
        nx.draw_networkx_edges(globals.G, globals.pos)
        plt.axis("off")
        self.draw_idle()


    def random_scheduler(self):
        meeting = random.sample(range(0, globals.num), 2)
        meeting.sort()
        print(meeting[0] + 1, meeting[1] + 1)
        return meeting[0], meeting[1]

    def stack(self, name):
        if (name == "Global-Star"):
            if math.ceil(globals.num * math.log2(globals.num) * math.log2(globals.num * math.log2(globals.num))) < 1000:
                globals.additional = math.ceil(globals.num * math.log2(globals.num) * math.log2(globals.num * math.log2(globals.num)))
            else:
                globals.additional = 1000
            print(globals.additional)
        if (name == "Cycle-Cover"):
            if math.ceil(globals.num ** 2 * math.log2(globals.num ** 2)) < 1000:
                globals.additional = math.ceil(globals.num ** 2 * math.log2(globals.num ** 2))
            else:
                globals.additional = 1000
            print(globals.additional)
        if (name == "Simple-Global-Line"):
            if math.ceil(globals.num ** 4 * math.log2(globals.num ** 4)) < 1000:
                globals.additional = math.ceil(globals.num ** 4 * math.log2(globals.num ** 4))
            else:
                globals.additional = 1000
            print(globals.additional)
        if (name == "Custom"):
            globals.additional = 200
            print(globals.additional)
        globals.stack.insert(0, deepcopy(globals.edges))
        globals.state_stack.insert(0, deepcopy(globals.states))
        if (len(globals.stack) > globals.additional):
            globals.stack.pop(globals.additional)
        if (len(globals.state_stack) > globals.additional):
            globals.state_stack.pop(globals.additional)
        if ([globals.stack[0]] * len(globals.stack) == globals.stack) and \
                ([globals.state_stack[0]] * len(globals.state_stack) == globals.state_stack) and (len(globals.stack) == globals.additional):
            print("Stable")
            globals.ani.pause()
            print(globals.runningTime-globals.additional+1)
            globals.flag = True
            globals.running = False
        else:
            print("Unstable")
            globals.flag = False
            globals.running = True


    def Global_Star(self, frame):
        self.figure.clf()
        num1, num2 = self.random_scheduler()
        if globals.labels[num1] == 'c' and globals.labels[num2] == 'c':
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
            change = random.choice([num1, num2])
            globals.labels[change] = 'p'
            globals.states[change] = 'p'
        elif globals.labels[num1] == 'p' and globals.labels[num2] == 'p' and globals.G.has_edge(num1, num2) == True:
            globals.G.remove_edge(num1, num2)
            globals.edges[num1][num2] = 0
            globals.edges[num2][num1] = 0
        elif globals.labels[num1] == 'c' and globals.labels[num2] == 'p' and globals.G.has_edge(num1, num2) == False:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
        elif globals.labels[num1] == 'p' and globals.labels[num2] == 'c' and globals.G.has_edge(num1, num2) == False:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
        globals.runningTime = globals.runningTime + 1
        self.stack("Global-Star")
        print(globals.runningTime)
        print(globals.edges)
        print(globals.states)
        print(globals.stack)
        globals.form.runningTime.setText(str(globals.runningTime))
        if globals.flag == True:
            globals.form.stability.setText("Stable")
            globals.form.runningTime.setText(str(globals.runningTime - globals.additional + 1))
        if globals.flag == False:
            globals.form.stability.setText("Unstable")
        self.plot()


    def Cycle_Cover(self, frame):
        self.figure.clf()
        num1, num2 = self.random_scheduler()
        if globals.labels[num1] == 'q0' and globals.labels[num2] == 'q0' and globals.G.has_edge(num1, num2) == False:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
            globals.labels[num1] = 'q1'
            globals.labels[num2] = 'q1'
            globals.states[num1] = 'q1'
            globals.states[num1] = 'q2'
        elif globals.labels[num1] == 'q0' and globals.labels[num2] == 'q1' and globals.G.has_edge(num1, num2) == False:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
            globals.labels[num1] = 'q1'
            globals.labels[num2] = 'q2'
            globals.states[num1] = 'q1'
            globals.states[num1] = 'q2'
        elif globals.labels[num1] == 'q1' and globals.labels[num2] == 'q0' and globals.G.has_edge(num1, num2) == False:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
            globals.labels[num1] = 'q2'
            globals.labels[num2] = 'q1'
            globals.states[num1] = 'q2'
            globals.states[num1] = 'q1'
        elif globals.labels[num1] == 'q1' and globals.labels[num2] == 'q1' and globals.G.has_edge(num1, num2) == False:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
            globals.labels[num1] = 'q2'
            globals.labels[num2] = 'q2'
            globals.states[num1] = 'q2'
            globals.states[num1] = 'q2'
        globals.runningTime = globals.runningTime + 1
        self.stack("Cycle-Cover")
        print(globals.runningTime)
        print(globals.edges)
        print(globals.states)
        print(globals.stack)
        globals.form.runningTime.setText(str(globals.runningTime))
        if globals.flag == True:
            globals.form.stability.setText("Stable")
            globals.form.runningTime.setText(str(globals.runningTime - globals.additional + 1))
        if globals.flag == False:
            globals.form.stability.setText("Unstable")
        self.plot()


    def Simple_Global_Line(self, frame):
        self.figure.clf()
        num1, num2 = self.random_scheduler()
        if globals.labels[num1] == 'q0' and globals.labels[num2] == 'q0' and globals.G.has_edge(num1, num2) == False:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
            change = random.choice([0, 1])
            if change == 0:
                globals.labels[num1] = 'q1'
                globals.states[num1] = 'q1'
                globals.labels[num2] = 'l'
                globals.states[num2] = 'l'
            if change == 1:
                globals.labels[num2] = 'q1'
                globals.states[num2] = 'q1'
                globals.labels[num1] = 'l'
                globals.states[num1] = 'l'
        elif globals.labels[num1] == 'l' and globals.labels[num2] == 'q0' and globals.G.has_edge(num1, num2) == False:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
            globals.labels[num1] = 'q2'
            globals.states[num1] = 'q2'
            globals.labels[num2] = 'l'
            globals.states[num2] = 'l'
        elif globals.labels[num1] == 'q0' and globals.labels[num2] == 'l' and globals.G.has_edge(num1, num2) == False:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
            globals.labels[num2] = 'q2'
            globals.states[num2] = 'q2'
            globals.labels[num1] = 'l'
            globals.states[num1] = 'l'
        elif globals.labels[num1] == 'l' and globals.labels[num2] == 'l' and globals.G.has_edge(num1, num2) == False:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
            change = random.choice([0, 1])
            if change == 0:
                globals.labels[num1] = 'q2'
                globals.states[num1] = 'q2'
                globals.labels[num2] = 'w'
                globals.states[num2] = 'w'
            if change == 1:
                globals.labels[num2] = 'q2'
                globals.states[num2] = 'q2'
                globals.labels[num1] = 'w'
                globals.states[num1] = 'w'
        elif globals.labels[num1] == 'w' and globals.labels[num2] == 'q2' and globals.G.has_edge(num1, num2) == True:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
            globals.labels[num1] = 'q2'
            globals.states[num1] = 'q2'
            globals.labels[num2] = 'w'
            globals.states[num2] = 'w'
        elif globals.labels[num1] == 'q2' and globals.labels[num2] == 'w' and globals.G.has_edge(num1, num2) == True:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
            globals.labels[num2] = 'q2'
            globals.states[num2] = 'q2'
            globals.labels[num1] = 'w'
            globals.states[num1] = 'w'
        elif globals.labels[num1] == 'w' and globals.labels[num2] == 'q1' and globals.G.has_edge(num1, num2) == True:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
            globals.labels[num1] = 'q2'
            globals.states[num1] = 'q2'
            globals.labels[num2] = 'l'
            globals.states[num2] = 'l'
        elif globals.labels[num1] == 'q1' and globals.labels[num2] == 'w' and globals.G.has_edge(num1, num2) == True:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
            globals.labels[num2] = 'q2'
            globals.states[num2] = 'q2'
            globals.labels[num1] = 'l'
            globals.states[num1] = 'l'
        globals.runningTime = globals.runningTime + 1
        self.stack("Simple-Global-Line")
        print(globals.runningTime)
        print(globals.edges)
        print(globals.states)
        print(globals.stack)
        globals.form.runningTime.setText(str(globals.runningTime))
        if globals.flag == True:
            globals.form.stability.setText("Stable")
            globals.form.runningTime.setText(str(globals.runningTime - globals.additional + 1))
        if globals.flag == False:
            globals.form.stability.setText("Unstable")
        self.plot()


    def custom(self, frame):
        self.figure.clf()
        num1, num2 = self.random_scheduler()
        if globals.labels[num1] == 'c' and globals.labels[num2] == 'c' and globals.G.has_edge(num1, num2) == False:
            globals.G.add_edge(num1, num2)
            globals.edges[num1][num2] = 1
            globals.edges[num2][num1] = 1
        globals.runningTime = globals.runningTime + 1
        self.stack("Custom")
        print(globals.runningTime)
        print(globals.edges)
        print(globals.states)
        print(globals.stack)
        globals.form.runningTime.setText(str(globals.runningTime))
        if globals.flag == True:
            globals.form.stability.setText("Stable")
            globals.form.runningTime.setText(str(globals.runningTime - globals.additional + 1))
        if globals.flag == False:
            globals.form.stability.setText("Unstable")
        self.plot()
