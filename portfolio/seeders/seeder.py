import abc

from faker import Faker


class Seeder(metaclass=abc.ABCMeta):
    faker = Faker('en_GB')

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'seed') and
                callable(subclass.seed) or
                NotImplemented)

    @abc.abstractmethod
    def seed(self):
        raise NotImplementedError
