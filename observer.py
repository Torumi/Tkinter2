from abc import ABC, abstractmethod


class Observable:
    _observers: list = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer not in self._observers:
            print("ERROR: Observer not attached")
            return
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(self, message)

    def clear(self):
        self._observers = []


class Observer(ABC):

    @abstractmethod
    def update(self, subject: Observable, message: str):
        pass

    def subscribe(self, observable: Observable):
        observable.attach(self)

    def unsubscribe(self, observable: Observable):
        observable.detach(self)
