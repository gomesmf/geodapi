from abc import ABC, abstractmethod

class AccountsServiceInterface(ABC):
    @abstractmethod
    def create_account(self):
        pass

    @abstractmethod
    def get_account_types(self):
        pass
