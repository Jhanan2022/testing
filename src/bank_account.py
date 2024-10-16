from datetime import datetime
from src.exceptions import InsufficientFundsError, WithdrawalTimeRestrictionError


class BankAccount:
    def __init__(self, balance=0, log_file=None):
        self.balance = balance
        self.log_file = log_file
        self._log_transaction('Cuenta creada')

    def _log_transaction(self, message):
        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(f"{message}\n")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._log_transaction(f"Deposited {amount}. New balance: {self.balance}")
        return self.balance

    def withdraw(self, amount):        
        now = datetime.now()
        if now.hour < 8 or now.hour > 17:
            raise  WithdrawalTimeRestrictionError("Withdrawal are not allowed before 8am or after 5 pm")
        elif now.weekday() in [5,6]:
            raise  WithdrawalTimeRestrictionError("Withdrawal are not allowed on weekends")

        if amount > 0:
            self.balance -= amount
            self._log_transaction(f"Withdrew {amount}. New balance: {self.balance}")
        return self.balance

    def get_balance(self):
        self._log_transaction(f"Checked balance. Current balance: {self.balance}")
        return self.balance
    
    def transfer(self, amount):
        account2 = BankAccount(balance=0, log_file=None)
        self._log_transaction("Transfer initiated")
        if self.get_balance()  >= amount:
            self.withdraw(amount)
            account2.deposit(amount)
            self._log_transaction("Transfer completed")
        elif  self.get_balance() < amount:
            self._log_transaction("Insufficient funds")
            raise  ValueError("Insufficient funds")