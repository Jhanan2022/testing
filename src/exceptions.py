class InsufficientFundsError(Exception):
    """Raised when the user does not have sufficient funds to make a transaction."""
    pass

class WithdrawalTimeRestrictionError(Exception):
    """Raised when the user attempts to withdraw funds at a restricted time."""
    pass