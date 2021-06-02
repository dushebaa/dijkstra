from copy import deepcopy
from node import Node
import arcade

NODE_SIZE = 20
INF = float('inf')

#the second one stores coordinates to visualise the graph
nodes = {}
Nodes = []
weights = {}

class MainWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True, update_rate=1/144)
        
        self.width = width
        self.height = height
        self.time = 0 
        self.mouse_x = None
        self.mouse_y = None
        self.selected = None
        self.typingWeight = False
        self.start = -1
        self.finish = -1
        self.weight = ''
        self.dragged = False
        self.shortPath = None
        self.table = None

        #nodes that we need to assign weight to
        self.ith_node = None
        self.jth_node = None
        
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        
        if (self.typingWeight):
            arcade.draw_text(f'Enter node weight: {self.weight}', 0, self.height-NODE_SIZE, arcade.color.BLUE, NODE_SIZE, anchor_x="left", anchor_y="top")

        arcade.draw_text(f'Start pos: {self.start}, end pos: {self.finish}', 0, self.height, arcade.color.BLUE, NODE_SIZE, anchor_x="left", anchor_y="top")

        #draw lines  
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if (j in nodes[i]):
                    node = Nodes[i]
                    c = Nodes[j]
                    arcade.draw_line(node.x, node.y, c.x, c.y, arcade.color.WHEAT, 2)
                    arcade.draw_text(str(nodes[i][j]), abs(node.x+c.x)//2, abs(node.y+c.y)//2, arcade.color.BLUE, NODE_SIZE)

        #draw green lines
        if self.shortPath != None:
            for i in range(1, len(self.shortPath)):
                node = Nodes[self.shortPath[i]] 
                c =    Nodes[self.shortPath[i-1]]  
                arcade.draw_line(node.x, node.y, c.x, c.y, arcade.color.GREEN, 2)

        #draw nodes
        for i in range(len(Nodes)):
            for j in range(len(Nodes)):
                node = Nodes[i]
                c = Nodes[j]
                arcade.draw_circle_filled(node.x, node.y, NODE_SIZE, node.color)
                arcade.draw_text(str(i), node.x, node.y, arcade.color.BLUE, NODE_SIZE, anchor_x="center", anchor_y="center")
        
        #draw table
        if (self.table != None):
            arcade.draw_text(self.table, 0, self.height-2*NODE_SIZE, arcade.color.BLUE_SAPPHIRE, NODE_SIZE, anchor_x="left", anchor_y="top")

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_update(self,  dt):
        self.time += dt           

    def on_mouse_press(self, x, y, button, modifiers):
        for i in range(len(Nodes)):
            #if clicked on node
            if ((x > Nodes[i].x - NODE_SIZE and x < Nodes[i].x + NODE_SIZE) and (y > Nodes[i].y - NODE_SIZE and y < Nodes[i].y + NODE_SIZE)):
                if (self.selected == None):
                    #set i-th node as selected
                    self.selected = i
                    Nodes[i].color = arcade.color.CAMEL
                else:
                    if (self.selected != i):
                        #if clicked on different node while selecting  
                        Nodes[self.selected].color = arcade.color.WHEAT

                        #get weight
                        self.typingWeight = True

                        self.ith_node = i
                        self.jth_node = self.selected
                    else:
                        Nodes[i].color = arcade.color.WHEAT
                        self.selected = None

        for i in range(len(Nodes)):
            if ((x > Nodes[i].x - NODE_SIZE and x < Nodes[i].x + NODE_SIZE) and (y > Nodes[i].y - NODE_SIZE and y < Nodes[i].y + NODE_SIZE)) or (self.selected != None):
                break
        else:
            #create new node 
            Nodes.append(Node(self.mouse_x, self.mouse_y, arcade.color.WHEAT))
            node_id = len(Nodes)-1
            nodes[node_id] = {}
    
    def on_mouse_drag(self, x, y, *modifiers):
        self.dragged = True
        if self.selected != None:
            Nodes[self.selected].x = x
            Nodes[self.selected].y = y
    
    def on_mouse_release(self, x, y, *modifiers):
        if self.dragged and self.selected != None:
            Nodes[self.selected].color = arcade.color.WHEAT
            self.selected = None
            self.dragged = False


    def on_key_press(self, key, *modifiers):        
        if (key == arcade.key.D):
            #dijkstra
            for i in range(len(nodes)):
                weights[i] = 0 if i == self.start else INF
            path = Node().search(self.start, self.finish, deepcopy(nodes), weights)
            self.shortPath = Node().backpedal(self.start, self.finish, path)

        if (key == arcade.key.T):
            #bouild the table
            s = '      '
            for i in range(len(nodes)):
                s += str(i) + '  ' 
            s += ' \n'
            for i in range(len(nodes)):
                s += str(i) + '    '
                for j in range(len(nodes)):
                    if (j in nodes[i]): s += str(nodes[i][j]) + '  '
                    else: s += '0  '
                s += '\n'
            self.table = s
        
        if (key == arcade.key.S):
            #start node selection 
            if (self.selected != None):
                self.start = self.selected
            else:
                print('No node selected')
        
        if (key == arcade.key.F):
            if (self.selected != None):
                self.finish = self.selected
            else:
                print('No node selected')

        if (key == arcade.key.R):
            self.shortPath = None
            self.table = None
        
        if (key >= 48 and key <= 57 and self.typingWeight):
            self.weight += str(key - 48)
        
        if (key == 65288):
            self.weight = self.weight[:-1]

        if (key == 65293):
            if (self.ith_node != None and self.jth_node != None):
                nodes[self.jth_node][self.ith_node] = int(self.weight) 
                nodes[self.ith_node][self.jth_node] = int(self.weight)
                self.weight = ''
                self.typingWeight = False
                self.selected = None
        
        if (key == arcade.key.DELETE):
            if self.selected != None:
                Nodes[self.selected].x = None