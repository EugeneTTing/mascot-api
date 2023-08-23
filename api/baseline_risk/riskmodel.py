from abc import ABC, abstractmethod

class RiskModel(ABC):
    
    @abstractmethod
    def predict(self):
        pass 