from progression import Progression


class ArithmeticProgression(Progression):
    """ 创建一个等差数列 """
    def __init__(self, start=0, increment=1) -> None:
        """ 创建一个新的等差数列对象 """
        super().__init__(start)
        self._increment = increment
    
    def _advance(self):
        """ 更新当前的数为前一个数加上增量 """
        self._current += self._increment
    

if __name__ == '__main__':
    arith = ArithmeticProgression(5, 3)
    print(next(arith))
    arith.print_progression(8)