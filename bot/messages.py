import abc

import telegram as tg


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


class RegularUser(BaseMessages):
    def start(self) -> str:
        return 'Привет'

    def help(self) -> str:
        return 'Вам нужно приобрести подписку'

    def echo(self, text: str) -> str:
        return f'{text}'


class PremiumUser(RegularUser):
    def start(self) -> str:
        return 'Здравствуйте!'

    def help(self) -> str:
        return 'Наш менеджер скоро свяжется с Вами'


def get_message(user: tg.User) -> BaseMessages:
    if not user.is_premium:
        return PremiumUser()
    else:
        return RegularUser()
