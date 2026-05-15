from abc import ABC, abstractmethod


class MathExpression(ABC):
    @abstractmethod
    def reduce(self):
        pass