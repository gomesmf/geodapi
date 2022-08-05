from unittest import main, TestCase

from accounts.GetAccountTypes.controller import get_account_types_controller
from accounts.GetAccountTypes.interactor import GetAccountTypesUCO, get_account_types_interactor
from accounts.GetAccountTypes.presenter import GetAccountTypesVM, get_account_types_presenter
from accounts.GetAccountTypes.view import GetAccountTypesResM, get_account_types_view

class TestController(TestCase):
    def test_success():
        pass

class TestInteractor(TestCase):
    def test_success(self):
        ucout = get_account_types_interactor()
        self.assertIsInstance(ucout, GetAccountTypesUCO)
        for at in ucout.account_types:
            self.assertIn("label", at)
            self.assertIn("value", at)

class TestPresenter(TestCase):
    def test_success(self):
        ucout = GetAccountTypesUCO(account_types=[
            {"label": "label", "value": "value"},
            {"label": "label", "value": "value"},
        ])
        vm = get_account_types_presenter(ucout)
        self.assertIsInstance(vm, GetAccountTypesVM)
        self.assertEqual(ucout.account_types, vm.account_types)

class TestView(TestCase):
    def test_success(self):
        vm = GetAccountTypesVM(account_types=[
            {"label": "label", "value": "value"},
            {"label": "label", "value": "value"},
        ])
        resm = get_account_types_view(vm)
        self.assertIsInstance(resm, GetAccountTypesResM)

if __name__ == "__main__":
    main()
