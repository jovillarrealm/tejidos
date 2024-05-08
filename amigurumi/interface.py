from abc import ABC, abstractmethod


class Reporte(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def reportar(self, data):
        pass
