class Range:
    """ 实现一个自定义的简单range类 """

    def __init__(self, start, stop=None, step=1) -> None:
        """ 创建一个新的Range对象 """
        if step == 0:
            raise ValueError('step cannot be 0')

        # 处理Range(n)的情况，此时即Range(0, n)
        if stop == None:
            start, stop = 0, start
        
        # 计算Range对象的长度
        self._length = max(0, (stop - start + step - 1) // step)

        self._start = start
        self._step = step

    def __len__(self):
        """ 返回Range中的元素个数 """
        return self._length
        
    def __getitem__(self, i):
        """ 获取第i+1个位置的元素 """
        if i < 0:
            i += self._length
        if not 0 <= i < self._length:
            raise IndexError('index out of range')
        
        return self._start + i * self._step


if __name__ == '__main__':
    r = Range(8, 140, 5)
    print(len(r))
    print(r[0], r[15])