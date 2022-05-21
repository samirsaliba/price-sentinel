from abc import ABC, abstractmethod

class BaseNotifier(ABC):
    @abstractmethod
    def notify(self):
        pass
    
    @abstractmethod
    def check_setup(self) -> bool:
        pass

    @abstractmethod
    def close_connection(self):
        pass
