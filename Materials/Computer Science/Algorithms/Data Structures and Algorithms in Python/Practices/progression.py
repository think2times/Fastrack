class Progression:
    """ 创建数列基类 """
    def __init__(self, start=0) -> None:
        """ 初始化一个Progression对象 """
        self._current = start
    
    def _advance(self):
        """ 更新self._current为下一个数 """
        self._current += 1

    def __next__(self):
        """ 返回数列的下一个数 """
        if self._current is None:
            raise StopIteration()
        else:
            ans = self._current
            self._advance()
            return ans
    
    def __iter__(self):
        """ 根据规范，迭代器必须返回自身作为迭代器 """
        return self
    
    def print_progression(self, n):
        """ 返回接下来n个数 """
        print(' '.join(str(next(self)) for i in range(n)))


if __name__ == '__main__':
    seq = Progression(5)
    print(next(seq))
    seq.print_progression(8)