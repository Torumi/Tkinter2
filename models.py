import datetime as dt


class RenterModel:
    def __init__(self, first_name: str, last_name: str, personal_code: str, phone_number: str):
        self._first_name = first_name
        self._last_name = last_name
        self._personal_code = personal_code
        self._phone_number = str(phone_number)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, new_value: str):
        self._first_name = new_value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_value: str):
        self._last_name = new_value

    @property
    def personal_code(self):
        return self._personal_code

    @personal_code.setter
    def personal_code(self, new_value: str):
        self._personal_code = new_value

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, new_value: str):
        self._phone_number = new_value

    @property
    def info(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'personal_code': self.personal_code,
            'phone_number': self.phone_number
        }

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.personal_code}) Tel.: {self.phone_number}"


class RentModel:
    def __init__(self,
                 category: str | None = None,
                 product_name: str | None = None,
                 description: str | None = None,
                 daily_price: float | int | None = None,
                 renter: RenterModel | None = None,
                 start_date: dt.datetime | None = None,
                 end_date: dt.datetime | None = None):
        self._category = category
        self._product_name = product_name
        self._description = description
        self._daily_price = daily_price
        self._accessible = True
        self._renter = renter
        self._start_date = start_date
        self._end_date = end_date

    @property
    def category(self):
        return self._category

    @property
    def product_name(self):
        return self._product_name

    @property
    def description(self):
        return self._description

    @property
    def daily_price(self):
        return self._daily_price

    @property
    def accessible(self):
        return self._accessible

    @property
    def renter(self):
        return self._renter

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    def remain(self):
        return self.end_date - dt.datetime.now()

    def total_price(self):
        return self.daily_price * (self.end_date - self.start_date).days

    def product_info(self):
        return {
            'category': self.category,
            'product_name': self.product_name,
            'description': self.description,
            'daily_price': self.daily_price,
            'accessible': self.accessible,
            'renter': self.renter.info,
            'start_date': self.start_date,
            'end_date': self.end_date
        }

    def renter_info(self):
        return self.renter.info

    def __str__(self):
        return f"{self.product_name} (Category: {self.category}, Description: {self.description}\n" \
               f"Daily price: {self.daily_price}€, Renter: {self.renter}\n" \
               f"From {self.start_date.strftime('%d.%m.%Y %H:%M')} to {self.end_date.strftime('%d.%m.%Y %H:%M')})"
