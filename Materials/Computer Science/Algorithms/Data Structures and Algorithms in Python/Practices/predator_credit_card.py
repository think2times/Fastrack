from credit_card import CreditCard

class PredatorCreditCard(CreditCard):
    
    def __init__(self, customer, bank, account, limit, apr) -> None:
        """ 创建一个新的掠夺性信用卡 """
        super().__init__(customer, bank, account, limit)
        self._apr = apr     # 年利率
    
    def charge(self, price) -> bool:
        """ 如果超过透支额度，则收取 $5 手续费 """
        success = super().charge(price)
        if not success:
            self._balance += 5
        return success
    
    def process_month(self):
        """ 根据年利率计算每月利息 """
        if self._balance > 0:
            monthly_factor = pow(1 + self._apr, 1/12)
        self._balance *= monthly_factor


if __name__ == '__main__':
    pc = PredatorCreditCard("pwDing", "ABC", "5816376", 100000000, 0.3)
