from progression import Progression


class FibonacciProgression(Progression):
    """ 创建一个Fibonacci数列 """
    def __init__(self, first=0, second=1) -> None:
        """ 初始化一个Fibonacci数列对象 """
        super().__init__(first)
        self._prev = second - first
    
    def _advance(self):
        """ 更新self._prev和self._current """
        self._prev, self._current = self._current, self._prev + self._current


if __name__ == '__main__':
    arith = FibonacciProgression(5, 3)
    arith.print_progression(8)