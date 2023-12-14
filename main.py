import datetime
import tkinter as tk
from tkinter import Tk
import uuid
from rent_store import RentStore
# from controllers import RentController
from models import RentModel
import views
from observer import Observer, Observable


class ManagerMain(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1024x640")
        self.title("Rent Manager")

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=4)

        self.button_container = tk.Frame(master=self, highlightthickness=2)
        self.rent_list_container = tk.Frame(master=self, highlightthickness=2)
        self.working_container = tk.Frame(master=self, highlightthickness=2)

        self.button_container.grid(row=0, column=0)
        self.rent_list_container.grid(row=1, column=0)
        self.working_container.grid(row=0, column=1, rowspan=2)

        self.add_rent_btn = tk.Button(self.button_container, text='Add Rent', command=self.add_entry_window)
        self.add_rent_btn.pack()
        self.delete_rent_btn = tk.Button(self.button_container, text='Delete Rent', command=self.add_delete_window)
        self.delete_rent_btn.pack()
        self.rent_list = views.RentList(self.rent_list_container)
        self.rent_list.bind_list('<<ComboboxSelected>>', self.create_rent_view)

        RentStore.load()
        self.rent_list.load_list()

    def add_entry_window(self):
        self.clear_working_container()
        rent_add_window = views.RentAddView(self.working_container)
        rent_add_window.add_entry("Name", 'name')
        rent_add_window.add_entry("Category", 'category')
        rent_add_window.add_entry("Description", 'description')
        rent_add_window.add_entry("Daily price", 'daily_price', entry_type='number')
        rent_add_window.add_entry("Renter name", 'renter_name')
        rent_add_window.add_entry("Renter last name", 'renter_last_name')
        rent_add_window.add_entry("Renter personal code", 'renter_personal_code')
        rent_add_window.add_entry("Renter phone number", 'renter_phone_number')
        rent_add_window.add_entry("Rent start date", 'start_date', entry_type='date')
        rent_add_window.add_entry("Rent end date", 'end_date', entry_type='date')
        rent_add_window.pack_field()
        self.rent_list.subscribe(rent_add_window)

    def add_delete_window(self):
        self.clear_working_container()
        rent_remove_window = views.RentRemoveWindow(self.working_container)
        self.rent_list.subscribe(rent_remove_window)

    def clear_working_container(self):
        for widget in self.working_container.winfo_children():
            if isinstance(widget, Observable):
                widget.clear()
            widget.destroy()

    def create_rent_view(self, event):
        self.clear_working_container()
        model: RentModel = RentStore.get_dict()[self.rent_list.get()]
        test_msg = tk.Label(master=self.working_container, justify=tk.LEFT, text=f"{model.product_name}\n"
                                                                f"Category: {model.category}\n"
                                                                f"Description: {model.description}\n"
                                                                f"Daily price: {model.daily_price}€\n"
                                                                f"Accessible: {model.accessible}\n"
                                                                f"Renter:\n"
                                                                f"      First name: {model.renter.first_name}\n"
                                                                f"      Last name: {model.renter.last_name}\n"
                                                                f"      Personal code: {model.renter.personal_code}\n"
                                                                f"      Phone number: {model.renter.phone_number}\n"
                                                                f"Rent stats in: {datetime.datetime.strftime(model.start_date, '%d.%m.%Y')}\n"
                                                                f"Rent ends in: {datetime.datetime.strftime(model.end_date, '%d.%m.%Y')}")
        test_msg.pack()



def _run():
    app = ManagerMain()
    # rent_view = RentView(app)
    # rent_model = RentModel()
    # rent_controller = RentController(rent_model, rent_view)
    # rent_controller.show_rent()

    app.mainloop()


if __name__ == '__main__':
    _run()
