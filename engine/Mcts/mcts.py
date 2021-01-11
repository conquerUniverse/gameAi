import numpy as np
import time

class Mcts:
    def __init__(self,env,turn,root,debug =False):
        """
        General Mcts is implemented with required functions
        Player 1 - False
        Player 2 - True
        """

        self.MaxTime = env.getResource()

        self.iniTime = time.time()
        self.env = env
        self.turn = turn
        self.root = root
        self.maxVal = float('inf')
        self.debug = debug

        # iteration resouce
        self.maxIter = 1000
        self.iter = 0

    
    def resourceAvailable(self,UseTimeResource = True):
        # within the time limit

        # Use iterations For Calculations
        if  not UseTimeResource:
            if self.iter < self.maxIter:
                self.iter += 1
                return True
            return False


        if time.time() - self.iniTime  <= self.MaxTime:
            return True
        return False

    def best(self,node):
        """ UCB selection """
        if node.isTerminal:
            return node

        past = -self.maxVal
        obj = node
        
        for i in node.childNodes: 
            val = self.nodeValue(i)
            if val > past: # maximize
                obj = i
                past = val
        return obj


    def selection(self,node):
        """Return the leaf node To be expanded """

        while not node.isTerminal and not node.isLeafNode :
            node = self.best(node) # higher UCT value

        if node.isLeafNode:  
            node.findChilds()
            node.isLeafNode = False

        return self.best(node)



    def rollout(self,node):
        # simulate the game with env

        temp_turn = node.turn
        temp_state = node.state.copy()
        moves_count = 0

        while self.env.isComplete(temp_state) == -1 and moves_count < self.env.moves_limit(): # unless the Game is complete
            moves_count+=1
            moves = self.env.getMoves(temp_state,temp_turn) # gives random moves
            temp_state = self.env.executeMove(temp_state.copy(), moves[0], temp_turn)
            temp_turn = not temp_turn
            # invert_reward = not invert_reward

        if moves_count < self.env.moves_limit():
            winner = self.env.isComplete(temp_state) # 0, 1,2
        else:
            winner = self.env.tempIsComplete(temp_state)

        if node.turn == True:
            wint = 2
        else:
            wint = 1

        if winner == 0:
            return 1 #draw
        elif wint == winner:
            return 2  # favourable condition
        return 0
    

    def nodeValue(self,node):
        # UCB funciton

        win = node.win
        nodeVisit = node.visited
        rootVisit = self.root.visited

        if nodeVisit==0:
            return self.maxVal
        return win/nodeVisit +  np.sqrt(2*np.log(rootVisit)/nodeVisit)

    def backpropagate(self,node,result):
        # update the values to the root node
        assert node!=self.root

        while node != None :
            result =1-result
            node.win += result
            node.visited += 1
            # node.winUpdated = True
            node = node.parent

            # for simulation
            
            
        

    def bestMove(self,node):
        # find the best move with UCT
        # assert node.childNodesExtracted == True

        past = -self.maxVal
        obj = None
        assert node.isLeafNode == False

        for i in node.childNodes:
            if i.win >= past: # max
                obj = i
                past = i.win
            
        return obj.move


    def execute(self,UseTimeResource = True):
        """ the core of Mcts """

        self.iniTime = time.time() # restart time 

        while self.resourceAvailable(UseTimeResource):
            node = self.selection(self.root) # find the leaf nodes to be expanded
            simulation_result = self.rollout(node)
            self.backpropagate(node,simulation_result)

            # simulation display root node
            if self.debug == True:
                time.sleep(0.5)
                clear_output(True)
                for j in self.root.childNodes:
                    j.print()
                    print(j.win,j.visited)
                    if j.winUpdated == True:
                        prGreen(self.nodeValue(j))
                        j.winUpdated = False
                    else:
                        print(self.nodeValue(j))


        return self.bestMove(self.root)