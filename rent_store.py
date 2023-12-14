import datetime
import os.path

from models import RentModel, RenterModel
import config as cfg
import json


class RentStore:
    _rent_dict: dict[RentModel] = {}

    @classmethod
    def get_dict(cls):
        return cls._rent_dict

    @classmethod
    def append(cls, model: RentModel):
        cls._rent_dict[model.product_name] = model

    @classmethod
    def remove(cls, model: RentModel):
        del cls._rent_dict[model.product_name]

    @classmethod
    def serialize(cls):
        serialized = {}
        for model in cls._rent_dict:
            model = cls._rent_dict[model]
            serialized[model.product_name] = {
                'name': model.product_name,
                'category': model.category,
                'description': model.description,
                'daily_price': model.daily_price,
                'accessible': model.accessible,
                'renter': {
                    'name': model.renter.first_name,
                    'last_name': model.renter.last_name,
                    'personal_code': model.renter.personal_code,
                    'phone_number': model.renter.phone_number
                },
                'start_date': str(model.start_date),
                'end_date': str(model.end_date)
            }
        return serialized

    @classmethod
    def save(cls):
        with open(cfg.RENT_FILE_PATH, 'w') as rents_file:
            json.dump(cls.serialize(), rents_file, indent=4)

    @classmethod
    def load(cls):
        if not os.path.isfile(cfg.RENT_FILE_PATH):
            cls._rent_dict = {}
            return
        with open(cfg.RENT_FILE_PATH, 'r') as rents_file:
            serialized = json.load(rents_file)
            for model in serialized:
                model = serialized[model]
                renter = RenterModel(model['renter']['name'],
                                     model['renter']['last_name'],
                                     model['renter']['personal_code'],
                                     model['renter']['phone_number'])
                rent = RentModel(model['category'],
                                 model['name'],
                                 model['description'],
                                 model['daily_price'],
                                 renter,
                                 datetime.datetime.strptime(model['start_date'], '%Y-%m-%d %H:%M:%S'),
                                 datetime.datetime.strptime(model['end_date'], '%Y-%m-%d %H:%M:%S'))
                cls.append(rent)
