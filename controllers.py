# from views import RentView
from models import RentModel

class RenterController:
    pass


class RentController:
    def __init__(self, model: RentModel, view):
        self._model = model
        self._view = view

    def show_rent(self):
        self._view.add_entry("Name", self._model.product_name)

    def add_entry(self, name: str):
        self._view.add_entry(name)

    def pack_field(self):
        self._view.pack_field()
