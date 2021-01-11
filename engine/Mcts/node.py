class Node(object):
    """
    Monte Carlo Tree Search Node
    """
    def __init__(self,env,turn):

        # Attrib
        self.win = 0 #reward
        self.visited = 0
        self.turn = turn
        self.value = float("inf")
        self.isTerminal = False # is terminal node
        self.isLeafNode = True
        self.winUpdated = False

        self.move = None
        self.parent = None # brackprop
        self.childNodes = [] 

        self.state = None # state
        self.env = env 

    def findChilds(self):
        # find all childs and add them

        if self.isTerminal:
            return self
        moves = self.env.getMoves(self.state, self.turn)

        for i in moves:
            temp_state = self.env.executeMove(self.state.copy(),i, self.turn)
            n =  Node(self.env,not self.turn)
            self.addChild(n,i,temp_state)


    def addChild(self,obj,move,temp_state = None):
        obj.parent = self
        obj.state = temp_state
        obj.move = move
        obj.isTerminal = self.env.isComplete(temp_state) != -1
        self.isExpanded = True 
        self.childNodes.append(obj)


    def print(self):
        self.env.printState(self.state)
