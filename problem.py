"""
problem.py
~~~~~~~~~~
A module to implement the code for thusaac.
"""
import math


class Problem(object):
    """
    问题集合.
    """

    def __init__(self) -> None:
        super().__init__()


class LuckNum(Problem):
    """
    小明发明了一种“幸运数”，一个正整数，其偶数位不变（个位为第1位，十位为第2位，以此类推），奇数位做如下变换：
    * 将数字乘以7，如果不大于9则作为变换结果，否则把结果的各位数相加，如果结果不大于9则作为变换结果，否则（结果仍大于9）继续
    把各位相加，直到结果不大于9，作为变换结果。变换结束后，把变换结果的各位数相加，如果得到的和是8的倍数，则称一个开始的正整数
    为幸运数。
    * 例如，16347:第1位为7，乘以7, 结果为49，大于9，各位数相加为13，仍大于9，继续各位数相加，最后结果为4；第3位位3， 变换结果
    为3；第5位位1，变换结果为7.最后变换结果为76344，对于结果76344其各位数之和为24，是8的倍数。因此16347是幸运数。
    """

    def resolve(self, num: int) -> tuple[str, int]:
        """
        计算方式为：
        1. 个位数字位置设置为1
        2. 幸运数初始化为0
        3. 计算输入数字的长度 N
        4. 从个位数开始循环(从 1 开始到 N)
           4.1 取出每一个位置的数字
           4.2 如果4.1取出来的是偶数位，则该位数字对应的变换结果为自己
           4.3 如果4.1取出来的是奇数位，则计算该数字的变换结果
           4.4 幸运数字的计算方式为：
              4.4.1 个十百千万位置的变换结果换算成对应的值,即:个位数字(第1位）乘以1， 十位数字(第2位）乘以10，百位数字(第3位）乘以10再乘以10，依次类推
              注意：乘以1等价于乘以10的0次方，乘以10等价于乘以10的1次方，依次类推。
        @param num: 待确认的输入整数。
        @return: 2元组，第一位表示T/F；第二位表示转换后的数。
        """
        # 个位数位置设置为1
        pos: int = 1
        # 幸运数初始化为0
        lucky_num: int = 0
        # 计算输入数字的长度
        num_len: int = self.get_num_len(num)
        # 从个位数开始循环
        while pos <= num_len:
            # 取出每一个位置的数字
            digit: int = self.get_digit_at_pos(num, pos)
            if pos % 2 == 0:
                # 如果是偶数位，变换结果即为其自身
                lucky_digit: int = digit
            else:
                # 如果是奇数位，计算其变换结果
                lucky_digit: int = self.translate_digit(digit)
            lucky_num = lucky_num + lucky_digit * self.int_power(10, pos - 1)
            pos = pos + 1

        return "T" if lucky_num % 8 == 0 else "F", lucky_num

    @staticmethod
    def int_power(base: int, n: int) -> int:
        """
        幂次方计算，如10的平方，10的立方等等。
        @param base: 求幂运算的基底，如10，即求10的幂次方。
        @param n: 幂次数，如1表示base的1次方，n=2表示求base的平方
        @return: 整数
        """
        result: int = 1
        while n > 0:
            result = result * base
            n = n - 1
        return result

    @staticmethod
    def get_digit_at_pos(num: int, pos: int) -> int:
        """
        获取整数对应位置的数字。
        @param num: 输入数。
        @param pos: 想要获取的位置，个位为1，十位位2，依次类推额。
        @return: 0-9之间的数字。
        """
        digit: int = 0
        while pos > 0:
            digit = num % 10
            num = num // 10
            pos = pos - 1

        return digit

     @staticmethod
    def translate_digit_2(digit: int) -> int:
        """
        该函数利用模运算法则对输入数字进行转换获得不大于9的转换值。核心思想为模运算的法则：
        1. (a+b)%p = (a%p + b%p)%p
        2. (a-b)%p = (a%p - b%p)%p
        3. (a*b)%p = (a%p * b%p)%p
        4. a^b%p = (a%p)^b %p
        同时，模运算满足结合律、交换律、分配律：
        A. 结合律
            A.1 ((a+b)%p+c)%p = (a+(b+c)%p)%p
            A.2 ((a*b)%p*c)%p = (a*(b*c)%p)%p
        B. 交换律
            B.1 (a+b)%p = (b+a)%p
            B.2 (a*b)%p = (b*a)%p
        C. 分配律
            C.1 (a+b)%p = (a%p + b%p)%p
            C.2 ((a+b)%p*c)%p = ((a*c)%p + (b*c)%p)%p
        例如：digit = 7,
            1.7乘以7 = 49，值大于9需要进行转换，转换规则如下：
            2.通过模9运算限制输出值小于9，但是由于题目要求是不大于9都有效，因此可以将49减去1，再进行模9运算，即48%9 = 3，由于运算前减去了1
            再将其加上，使输出值符合不超过9的要求。
            3. 为什么这种计算方式有效？可以通过如需模运算规则实现：
                3.1 48 = 40 + 8, 因此 48%9 = (40 + 8)%9，根据模运算分配律，48%9 = (40 + 8)%9 = (40%9 + 8%9)%9 =
                ((4*10)%9 + 8)%9，
                3.2 继续根据模运算四则运算法则3，将其继续拆解成((4%9*10%9)%9 + 8)%9 = ((4*1)%9 + 8)%9
                = (4 + 8)%9，此时可以发现 48%9 = (4+8)%9，即乘积值除以9的余数等于其个位数和十位数求和后再除以9取余数。所以转换算法就简化
                成了 (input*7 - 1) % 9 + 1
        这个转换函数与``translate_digit(digit: int) -> int``的结果相同，但是算法更优雅速度更快。缺点是需要首先理解模运算四则运算法则。
        @param digit: 输入数
        @return: 0-9之间的转换值
        """
        if digit == 0:
            return 0
        product: int = digit * 7
        return (product - 1) % 9 + 1

    @staticmethod
    def translate_digit(digit: int) -> int:
        """
        该函数将一个数字转换为对应的小于等于9的转换值。算法为：
        1. 转换值初始化为0
        2. 输入数字乘以7（结果不大于63，因为输入数字为0-9之间，乘以7在0 - 63之间）
        3. 如果输入数字乘以7的结果不大于9，则计算完成
        4. 如果输入数字乘以7的结果大于9则将该数字的个位与十位分离出来(乘积在0 - 63之间，不超过2位数):
            4.1 分离个位数：取余数，即模10
            4.2 分离十位数：整除运算，即整初10
        5. 对分离出来的个位数与十位数字求和
        6. 如果第5步计算结果大于9，则对求出来的和继续进行取余数和整除运算，分离个位数和十位数
            6.1 分离个位数：取余数，即模10
            6.2 分离十位数：整除运算，即整初10
        7. 重复第5步和第6步，直到求和结果不超过9
        8. 返回转换的结果
        """
        # 1. 转换值初始化为0
        translated_digit: int = 0
        # 2. 输入数字乘以7（结果不大于63，因为输入数字为0-9之间，乘以7在0 - 63之间）
        product: int = digit * 7
        if product <= 9:
            # 3. 如果输入数字乘以7的结果不大于9，则计算完成
            translated_digit = product
        else:
            # 4. 如果输入数字乘以7的结果大于9则将该数字的个位与十位分离出来(乘积在0 - 63之间，不超过2位数):
            # 4.1 分离个位数：取余数，即模10
            product_sub_1: int = product % 10
            # 4.2 分离十位数：整除运算，即整初10
            product_sub_2: int = product // 10
            # 5. 对分离出来的个位数与十位数字求和
            num_sum: int = product_sub_1 + product_sub_2
            # 6. 如果第5步计算结果大于9，则对求出来的和继续进行取余数和整除运算，分离个位数和十位数
            while num_sum > 9:
                # 6.1 分离个位数：取余数，即模10
                sum_sub_1: int = num_sum % 10
                # 6.2 分离十位数：整除运算，即整初10
                sum_sub_2: int = num_sum // 10
                # 7. 对分离出来的个位数与十位数字求和
                num_sum = sum_sub_1 + sum_sub_2
            translated_digit = num_sum
        return translated_digit

    @staticmethod
    def get_num_len(num: int) -> int:
        """
        通过循环整除10，计算一个整数的长度.
        @param num: 待求长度的整数
        @return: 整数的长度
        """
        num_len: int = 0
        while num > 0:
            num_len = num_len + 1
            # Python中//表示整除，/表示浮点除
            num = num // 10

        return num_len


if __name__ == "__main__":
    problem: LuckNum = LuckNum()

    input_num: int = 16347
    flag, lucky = problem.resolve(input_num)
    print(f"lucky of {input_num} is {lucky} result: {flag}")
