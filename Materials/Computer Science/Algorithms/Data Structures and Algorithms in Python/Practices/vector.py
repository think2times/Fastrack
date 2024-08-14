class Vector:
    """ 模拟数学中的向量 """
    def __init__(self, dimension) -> None:
        """ 创建一个维度为 dimension 的向量 
        
        向量的初始值为原点
        """
        self._coords = [0] * dimension
    
    def __len__(self):
        """ 返回向量的维度 """
        return len(self._coords)

    def __getitem__(self, i):
        """ 返回第i个位置的坐标 """
        return self._coords[i]
    
    def __setitem__(self, i, value):
        """ 修改第i个位置的坐标 """
        self._coords[i] = value
    
    def __add__(self, other):
        """ 返回两个向量的和 """
        if type(other) != Vector:
            raise TypeError
        if (len(self) != len(other)):
            raise ValueError

        # 以Vector类的对象存储向量和的结果
        ans = Vector(len(self))
        for i in range(len(other)):
            ans[i] = self[i] + other[i]
        return ans
    
    def __eq__(self, other):
        """ 判断两个向量的坐标是否相等 """
        return self._coords == other

    def __ne__(self, other):
        """ 判断两个向量是否不一样 """
        return not self == other    # 通过已定义的 __eq__ 方法直接判断两个向量是否一样
    
    def __str__(self) -> str:
        """ 产生向量的字符串表示 """
        return '<' + str(self._coords)[1: -1] + '>'     # 去除开头的'['和结尾的']'


if __name__ == '__main__':
    vector = Vector(5)
    vector[1] = 23
    vector[-1] = 45
    print(vector[4])
    u = vector + vector
    print(u)
    total = 0
    for v in vector:
        total += v
    print(total)
