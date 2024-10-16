import unittest, os
from unittest.mock import patch
import unittest.mock
from src.bank_account import BankAccount
from src.exceptions import WithdrawalTimeRestrictionError

SERVER = "b"

class BankAccountTests(unittest.TestCase):

    def setUp(self) -> None: #aqui creamos la instancia de cuenta account que se llamará en todos los métodos antes de ejecutarse con self
        self.account = BankAccount(balance=1000, log_file="transaction_log.txt")

    def tearDown(self) -> None:
        if os.path.exists(self.account.log_file):
            os.remove(self.account.log_file)

    def _count_lines(self, filename):
        with open(filename, "r") as f:
            return len(f.readlines())

    def test_deposit(self):
        new_balance = self.account.deposit(500)
        self.assertEqual(new_balance, 1500, "El  Balance no es igual")

    @patch("src.bank_account.datetime")
    def test_withdraw_raises_during_business_hours(self, mock_datetime):
        mock_datetime.now.return_value.hour = 10
        new_balance = self.account.withdraw(100)
        self.assertEqual(new_balance, 900, "El balance no es igual")

    @patch("src.bank_account.datetime")
    def test_withdraw_disallow_before_business_hours(self, mock_datetime):
        mock_datetime.now.return_value.hour = 7
        with self.assertRaises(WithdrawalTimeRestrictionError):
            self.account.withdraw(100)

    @patch("src.bank_account.datetime")
    def test_withdraw_disallow_after_business_hours(self, mock_datetime):
        mock_datetime.now.return_value.hour = 18
        with self.assertRaises(WithdrawalTimeRestrictionError):
            self.account.withdraw(100)

    @patch("src.bank_account.datetime")
    def test_withdraw_disallow_on_weekends(self, mock_datetime):
        mock_now = unittest.mock.Mock()
        mock_now.hour = 8
        mock_now.weekday.return_value = 5
        mock_datetime.now.return_value = mock_now
        with self.assertRaises(WithdrawalTimeRestrictionError):
            self.account.withdraw(100)

    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 1000,  "El  Balance no es igual")

    def test_transaction_log(self):
        self.account.deposit(500)
        self.assertTrue(os.path.exists("transaction_log.txt"))

    def test_count_transactions(self):
        assert self._count_lines(self.account.log_file) == 1
        self.account.deposit(500)
        assert self._count_lines(self.account.log_file) == 2

    def test_transfer_insufficient(self):
        with self.assertRaises(ValueError):
            self.account.transfer(1001)

    @patch("src.bank_account.datetime")
    def test_transfer(self, mock_datetime):
        mock_datetime.now.return_value.hour = 10
        self.account.transfer(1000)
        self.assertEqual(self.account.get_balance(),0)

    @unittest.skip("Trabajo en progreso")
    def test_skip(self):
        self.assertEqual(1, 1)

    @unittest.skipIf(SERVER=="b","Saltado porque no estamos en el servidor B.")
    def test_skip_if(self):
        self.assertEqual(100,100)

    def test_deposit_multiple_ammounts(self):
        test_cases = [
            {"ammount" : 100, "expected": 1100},
            {"ammount" : 5000, "expected": 6000},
            {"ammount" : 3000, "expected": 4000},
        ]
        for test_case in test_cases:
            self.account = BankAccount(balance=1000, log_file="transaction_log.txt")
            self.subTest(ammount=test_case["ammount"], expected=test_case["expected"])
            self.account.deposit(test_case["ammount"])

            """Explicación:
            test_cases: Es una lista de diccionarios, donde cada diccionario tiene la cantidad a depositar y el saldo esperado.
            Bucle for: Itera sobre los casos de prueba. En cada iteración, crea una nueva cuenta bancaria con un saldo inicial de 1000.
            self.subTest: Agrupa los casos de prueba dentro de un único test, pero los separa en sub-pruebas. Esto hace más fácil saber cuál falló sin detener todo el proceso.
            Depósito: Realiza el depósito con la cantidad especificada en cada caso de prueba."""
