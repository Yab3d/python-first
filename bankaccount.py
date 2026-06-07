class BankAccount:
    def __init__(self,account_number,owner,balance=0):
        self.account_number = account_number
        self.owner = owner
        self.balance = balance


    @property
    def balance(self):
        return self._balance
    


    @balance.setter
    def balance(self,value):
        if value < 0:
           raise ValueError("Balance cannot be negative")
        self._balance = value

    def deposite(self,amount):
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self.balance += amount

    def withdraw(self,amount):
        if amount > self.balance:
            raise ValueError("withdrwal cannot be greater than the balance")
        
        if amount < 0:
            raise ValueError("amount cannot be negative")
        
        self.balance -= amount


    def _str_(self):
        return f"{self.owner} ({self.account_number}) - Balance: ${self.balance}"
    

    def __repr__(self):
         return (
            f"BankAccount("
            f"account_number='{self.account_number}', "
            f"owner='{self.owner}', "
            f"balance={self.balance})"
        )
    
    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return False

        return self.account_number == other.account_number
    


acc1 = BankAccount("1001","Alice",500)
print(acc1)
