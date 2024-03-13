import abc

import telegram as tg

import weather


class BaseMessages(abc.ABC):
    @abc.abstractmethod
    def start(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def help(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def echo(self, text: str) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def weather(self, text: str) -> tuple:
        raise NotImplemented


class RegularUser(BaseMessages):
    def start(self) -> str:
        return 'Здравствуйте'

    def help(self) -> str:
        return 'Просто введите название города, чтобы узнать погоду'

    def echo(self, text: str) -> str:
        return f'{text}'

    def weather(self, text: str) -> tuple:
        return weather.get_weather(text)


class PremiumUser(RegularUser):
    def start(self) -> str:
        return 'Здравствуйте!'

    def help(self) -> str:
        return 'слишком богатый'


def get_message(user: tg.User) -> BaseMessages:
    if user.is_premium:
        return PremiumUser()
    else:
        return RegularUser()
