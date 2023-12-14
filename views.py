import datetime
import tkinter as tk
import uuid
from typing import Callable
from tkinter import ttk
import tkcalendar
from observer import *
from rent_store import RentStore
from models import RentModel, RenterModel


class RentAddView(tk.Frame, Observable):

    def __init__(self, master):
        super().__init__(master)
        self._fields_counter = 0
        self._entry_field = tk.Frame(master=self)
        self._input_vars = {}

    @property
    def fields_counter(self):
        return self._fields_counter

    @fields_counter.setter
    def fields_counter(self, new_value: int):
        self._fields_counter = new_value

    @property
    def entry_field(self):
        return self._entry_field

    def add_entry(self, label: str, name: str, entry_type=None):
        self._input_vars[name] = tk.Variable(name=name)
        entry_label = tk.Label(master=self, text=label)
        if entry_type == 'date':
            entry = tkcalendar.DateEntry(master=self, selectmode='day', date_pattern='dd.mm.y', textvariable=self._input_vars[name])
        elif entry_type == 'number':
            # TODO: Make mask to write only numbers
            ...
        else:
            entry = tk.Entry(master=self, textvariable=self._input_vars[name])

        entry_label.grid(row=self.fields_counter, column=0, padx=10, pady=5, sticky=tk.W)
        entry.grid(row=self.fields_counter, column=1, padx=10, pady=5)
        self.fields_counter += 1

    def _add_submit_button(self):
        submit_btn = tk.Button(master=self, text='Submit', command=self.submit)
        submit_btn.grid(row=self.fields_counter, column=0, columnspan=2)
        self.fields_counter += 1

    def pack_field(self):
        self._add_submit_button()
        self.pack()

    def submit(self):
        # TODO: Forbid to create rent with non-unique product name
        new_renter = RenterModel(self._input_vars['renter_name'].get(),
                                 self._input_vars['renter_last_name'].get(),
                                 self._input_vars['renter_personal_code'].get(),
                                 self._input_vars['renter_phone_number'].get())
        new_rent = RentModel(self._input_vars['category'].get(),
                             self._input_vars['name'].get(),
                             self._input_vars['description'].get(),
                             int(self._input_vars['daily_price'].get()) if self._input_vars['daily_price'].get() else 0,
                             new_renter,
                             datetime.datetime.strptime(self._input_vars['start_date'].get(), '%d.%m.%Y'),
                             datetime.datetime.strptime(self._input_vars['end_date'].get(), '%d.%m.%Y'))
        RentStore.append(new_rent)
        RentStore.save()
        submit_msg = tk.Label(self, text='Successfully added rent!', fg='green')
        submit_msg.grid(row=self.fields_counter, column=0, columnspan=2, sticky=tk.E)
        self.notify()


class RentList(Observer, tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._rent_list = ttk.Combobox(self)
        self._rent_list['values'] = ()
        self._rent_list.pack()
        self.pack()

    def append_rent(self, name: str):
        self._rent_list['values'] = (*self._rent_list['values'], name)

    def load_list(self):
        for model in RentStore.get_dict():
            self.append_rent(model)
    
    def update(self, subject: Observable):
        self.append_rent(subject.children['!entry'].get())

    def bind_list(self, sequence: str, callback: Callable):
        self._rent_list.bind(sequence, callback)

    def get(self):
        return self._rent_list.get()


