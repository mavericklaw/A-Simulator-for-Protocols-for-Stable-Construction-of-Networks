from GUI import *
import networkx as nx
global num
global pos
global ani
global additional
global speed
global file_path
global loops
pause = False
G = nx.Graph()
labels = {}
edges = []
states = []
runningTime = 0
custom_states = []
stack = []
state_stack = []
form = Ui_MainWindow()
running = False