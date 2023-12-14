from abc import ABC, abstractmethod


class Observable:
    _observers: list = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        if observer not in self._observers:
            print("ERROR: Observer not attached")
            return
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)


class Observer(ABC):

    @abstractmethod
    def update(self, subject: Observable):
        pass

    def subscribe(self, observable: Observable):
        observable.attach(self)

    def unsubscribe(self, observable: Observable):
        observable.detach(self)
