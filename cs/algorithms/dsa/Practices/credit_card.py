class CreditCard:
    def __init__(self, customer, bank, account, limit) -> None:
        """ 创建一个新的信用卡实例

        初始余额为0.
        customer 顾客的名字
        bank     银行的名称
        account  顾客的银行账号
        limit    这张信用卡的透支额度
        """
        self._customer = customer
        self._bank = bank
        self._account = account
        self._limit = limit
        self._balance = 0

    def get_customer(self) -> str:
        """ 返回顾客的姓名 """
        return self._customer
    
    def get_bank(self) -> str:
        """ 返回银行的名称 """
        return self._bank
    
    def get_account(self) -> str:
        """ 返回顾客的银行账号 """
        return self._account

    def get_limit(self) -> int:
        """ 返回信用卡的透支额度 """
        return self._limit

    def get_balance(self) -> int:
        """ 返回信用卡的当前使用额度 """
        return self._balance

    def charge(self, price) -> bool:
        """ 判断是否超过透支额度
        
        price   需要支付的费用
        如果足够进行透支，则进行透支，并返回 True，否则返回 False
        """
        if self._balance + price > self._limit:
            return False
        else:
            self._balance += price
            return True
    
    def make_payment(self, amount) -> None:
        """ 进行充值 """
        self._balance -= amount
