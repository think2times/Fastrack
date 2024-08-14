from progression import Progression


class GeometicProgression(Progression):
    """ 创建一个等比数列 """
    def __init__(self, start=1, ratio=2) -> None:
        """ 初始化一个等比数列对象 """
        super().__init__(start)
        self._ratio = ratio
    
    def _advance(self):
        """ 更新当前数 """
        self._current *= self._ratio


if __name__ == '__main__':
    arith = GeometicProgression(5, 3)
    print(next(arith))
    arith.print_progression(8)