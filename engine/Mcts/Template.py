from abc import ABC, abstractmethod
class Template(ABC):
    @abstractmethod
    def isComplete(self, state):
        pass
    
    @abstractmethod
    def getMoves(self, state,turn):
        pass
    
    @abstractmethod
    def executeMove(self,state,move,turn):
        pass
    
    @abstractmethod
    def printState(self,state):
        pass
    
    @abstractmethod
    def moves_limit(self):
        pass
    
    @abstractmethod
    def tempIsComplete(self,state):
        pass
    
    @abstractmethod
    def getResource(self):
        pass