import os
import sys
import globals
from GUI import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QFileDialog, QAbstractItemView
from PyQt5.QtCore import QModelIndex, pyqtSignal
import csv


class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.setup_gui()

    def setup_gui(self):
        globals.form.setupUi(self)
        globals.form.exitButton.clicked.connect(self.quit_program)
        globals.form.spinBox.setRange(2, 10)
        globals.form.comboBox.currentTextChanged.connect(self.setRules)
        globals.form.startButton.clicked.connect(self.run)
        globals.form.stopButton.clicked.connect(self.reset)
        globals.form.pause_resume.clicked.connect(self.toggle)
        globals.form.rules.setReadOnly(True)
        globals.form.runningTime.setReadOnly(True)
        globals.form.stability.setReadOnly(True)
        globals.form.comboBox.currentTextChanged.connect(self.plot_init)
        globals.form.comboBox.currentTextChanged.connect(self.open_custom)
        globals.form.spinBox.textChanged.connect(self.plot_init)
        globals.form.runningTime.setText(str(globals.runningTime))
        globals.form.speed_slider.setRange(1, 10)


    def plot_init(self):
        globals.form.canvas.figure.clf()
        globals.G.clear()
        globals.labels.clear()
        globals.states.clear()
        globals.num = globals.form.spinBox.value()
        if (globals.form.comboBox.currentText() == "Global-Star"):
            for x in range(0, globals.num):
                globals.G.add_node(x)
                globals.labels[x] = 'c'
                globals.states.append('c')
            globals.form.canvas.plot()
        elif (globals.form.comboBox.currentText() == "Cycle-Cover" or globals.form.comboBox.currentText() == "Simple-Global-Line"):
            for x in range(0, globals.num):
                globals.G.add_node(x)
                globals.labels[x] = 'q0'
                globals.states.append('q0')
            globals.form.canvas.plot()
        elif (globals.form.comboBox.currentText() == "Custom"):
            if len(globals.custom_states) != 0:
                for x in range(0, globals.num):
                    globals.G.add_node(x)
                    globals.labels[x] = globals.custom_states[0]
                    globals.states.append(globals.custom_states[0])
                globals.form.canvas.plot()


    def run(self):
        globals.running = True
        globals.flag = False
        globals.form.canvas.figure.clf()
        globals.G.clear()
        globals.runningTime = 0
        globals.form.runningTime.setText(str(globals.runningTime))
        globals.labels = {}
        globals.edges = [[0 for _ in range(globals.num)] for _ in range(globals.num)]
        self.plot_init()
        globals.speed = globals.form.speed_slider.value()
        if (globals.form.comboBox.currentText() == "Global-Star"):
            globals.ani = animation.FuncAnimation(globals.form.canvas.figure, globals.form.canvas.Global_Star, frames=None, interval=1000/globals.speed, repeat=True)
        if (globals.form.comboBox.currentText() == "Cycle-Cover"):
            globals.ani = animation.FuncAnimation(globals.form.canvas.figure, globals.form.canvas.Cycle_Cover, frames=None, interval=1000/globals.speed, repeat=True)
        if (globals.form.comboBox.currentText() == "Simple-Global-Line"):
            globals.ani = animation.FuncAnimation(globals.form.canvas.figure, globals.form.canvas.Simple_Global_Line, frames=None, interval=1000/globals.speed, repeat=True)
        if (globals.form.comboBox.currentText() == "Custom"):
            globals.ani = animation.FuncAnimation(globals.form.canvas.figure, globals.form.canvas.custom, frames=None, interval=1000/globals.speed, repeat=True)


    def toggle(self):
        if (globals.form.stability.text() == "Unstable"):
            if globals.pause == False:
                globals.ani.pause()
                globals.pause = True
            else:
                globals.ani.resume()
                globals.pause = False


    def quit_program(self):
        self.reset()
        self.close()
        if not QApplication.topLevelWidgets():
            QApplication.quit()


    def reset(self):
        if (globals.running == True):
            globals.ani.pause()
        globals.form.canvas.figure.clf()
        globals.G.clear()
        globals.edges = []
        globals.states = []
        globals.runningTime = 0
        globals.stack = []
        globals.state_stack = []
        globals.form.runningTime.setText(str(globals.runningTime))
        globals.labels = {}
        globals.form.canvas.plot()
        globals.flag = False
        globals.form.comboBox.setCurrentIndex(0)
        globals.form.stability.setText("")
        globals.form.comboBox.setEnabled(True)
        globals.custom_states = []
        print("reset")


    def setRules(self):
        if (globals.form.comboBox.currentText() == "Global-Star"):
            globals.form.rules.setText(f"(c, c, 0) → (c, p, 1){os.linesep}(p, p, 1) → (p, p, 0){os.linesep}(c, p, 0) → (c, p, 1)")
        if (globals.form.comboBox.currentText() == "Cycle-Cover"):
            globals.form.rules.setText(f"(q0, q0, 0) → (q1, q1, 1){os.linesep}(q1, q0, 0) → (q2, q1, 1){os.linesep}(q1, q1, 0) → (q2, q2, 1)")
        if (globals.form.comboBox.currentText() == "Fast-Global-Line"):
            globals.form.rules.setText(f"(q0, q0, 0) → (q1, l, 1){os.linesep}(l, q0, 0) → (q2, l, 1){os.linesep}(l, l, 0) → (q2', l', 1){os.linesep}(l', q2, 1) → (l'', f1, 0){os.linesep}(l', q1, 1) → (l'', f0, 0){os.linesep}(l'', q2', 1) → (l, q2, 1){os.linesep}(l, f0, 0) → (q2, l, 1){os.linesep}(l, f1, 1) → (q2', l', 1)")
        if (globals.form.comboBox.currentText() == "Simple-Global-Line"):
            globals.form.rules.setText(f"(q0, q0, 0) → (q1, l, 1){os.linesep}(l, q0, 0) → (q2, l, 1){os.linesep}(l, l, 0) → (q2, w, 1){os.linesep}(w, q2, 1) → (q2, w, 1){os.linesep}(w, q1, 1) → (q2, l, 1)")
        if (globals.form.comboBox.currentText() == "Custom" or globals.form.comboBox.currentText() == ""):
            globals.form.rules.setText("")


    def open_custom(self):
        if (globals.form.comboBox.currentText() == "Custom"):
            self.window2 = FileManager()
            self.window2.show()



class FileManager(QMainWindow):
    fileSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Manager')
        self.setGeometry(200, 200, 1000, 800)
        self.model = QFileSystemModel()
        self.model.setRootPath('')
        self.model.setNameFilters(['*.csv'])
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(''))
        self.tree_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tree_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.setCentralWidget(self.tree_view)
        self.fileSelected.connect(self.on_file_selected)


    def on_file_selected(self, path):
        globals.file_path = path
        print('Selected file:', path)
        print(globals.file_path)


    def on_selection_changed(self, selected, deselected):
        indexes = selected.indexes()
        if not indexes:
            return
        index = indexes[0]
        path = self.model.filePath(index)
        if self.model.isDir(index):
            return
        self.fileSelected.emit(path)
        self.close()
        with open(globals.file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                # print(row)
                globals.custom_states = globals.custom_states + row
            print(globals.custom_states)
            text = ""
            if (len(globals.custom_states) % 7 == 0):
                for x in range(0, int(len(globals.custom_states) / 7)):
                    text = text + "(" + globals.custom_states[x * 7] + ", " + globals.custom_states[x * 7 + 1] + ", " + globals.custom_states[x * 7 + 2] + ") → (" + globals.custom_states[x * 7 + 4] + ", " + globals.custom_states[x * 7 + 5] + ", " + globals.custom_states[x * 7 + 6] + ")" + os.linesep
                globals.form.rules.setText(text)
                print(text)
            else:
                print("error")


    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'CSV Files (*.csv)', options=options)
        if file_name:
            self.fileSelected.emit(file_name)



mainloop = QtWidgets.QApplication([])
app = QApplication([])
run_app = GUI()
run_app.show()
sys.exit(mainloop.exec_())