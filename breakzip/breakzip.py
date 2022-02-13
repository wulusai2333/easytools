import sys
import getopt
from itertools import chain
import time
from typing import List
from tqdm import tqdm
from zipfile import ZipFile
# chcp 65001 改变控制台编码编码为utf8


def main(argv):
    ascall = ''
    chinese = ''
    dir_file_name = ''  # 'D:/project/github/fuzzDicts/chinese/3500zi.txt'
    file_name = ''  # 'D:/project/MyWebProgect/bitburner/py/test.zip' # 你的文件路径
    lengths = [1, 2, 3, 4]    # 密码长度
    try:
        opts, args = getopt.getopt(argv, "ha:c:d:f:g:l:", ["ascaii=", "chinese="])
    except getopt.GetoptError:
        print('breakzip.py -a <a|A|1> -c <Number of Chinese characters used in dictionary> -d <dictionary file> -f <zip file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('breakzip.py -a <a|A|1> -c <Number of Chinese characters used in dictionary> -d <dictionary file> -f <zip file>')
            sys.exit()
        elif opt in ("-a", "--ascaii"):
            ascall = arg
        elif opt in ("-c", "--chinese"):
            chinese = arg
        elif opt in ("-d", "--dictionary"):
            dir_file_name = arg
        elif opt in ("-f", "--file"):
            file_name = arg
        elif opt in ("-g", "--great"):
            lengths = [(i+1) for i in range(0,int(arg))]
        elif opt in ("-l", "--length"):
            lengths = [int(arg)]
    #print('输入的文件为：', ascall)
    #print('输出的文件为：', chinese)
    dictionaries = []
    lower = [chr(i) for i in chain(range(97, 123))]
    upper = [chr(i) for i in chain(range(65, 91))]
    number = [chr(i) for i in chain(range(48, 58))]
    c3500 = []
    if dir_file_name != '':
        with open(dir_file_name, "r", encoding='utf-8') as f:
            data = f.read().replace("\r\n", "").replace("\n", "").replace(' ', "")
            # print(data)
            c3500 = list(data)
            # for ch in data:
            # 汉字字符转数字,转16进制字符串表示
            #    print(hex(ord(ch)).replace("0x", ""), end=",")
    for atype in ascall:
        if atype == 'a':
            dictionaries.extend(lower)
        if atype == 'A':
            dictionaries.extend(upper)
        if atype == '1':
            dictionaries.extend(number)
    if chinese != '' and int(chinese) <= len(c3500) and int(chinese) > 0:
        dictionaries.extend(c3500[0:int(chinese)])
    print("dictionaries: ", dictionaries, "length: ", len(dictionaries))
    start = time.time()

    # chr(97) -> 'a' 这个变量保存了密码包含的字符集
    # dictionaries = [chr(i) for i in
    #                 chain(range(97, 123),    # a - z
    #                       range(65, 91),    # A - Z
    #                       range(48, 58))]    # 0 - 9
    # print(dictionaries)
    # dictionaries.extend(['.com', 'www.'])    # 添加自定义的字符集

    def all_passwd(dictionaries: List[str], maxlen: int):
        # 返回由 dictionaries 中字符组成的所有长度为 maxlen 的字符串

        def helper(temp: list, start: int, n: int):
            # 辅助函数，是个生成器
            if start == n:    # 达到递归出口
                yield ''.join(temp)
                return
            for t in dictionaries:
                temp[start] = t    # 在每个位置
                yield from helper(temp, start + 1, n)

        yield from helper([0] * maxlen, 0, maxlen)

    zfile = ZipFile(file_name, 'r')    # 很像open

    def extract(zfile: ZipFile, pwd: str) -> bool:
        # zfile: 一个ZipFile类, pwd: 密码
        try:
            zfile.extractall(path='.', pwd=pwd.encode(
                'utf-8'))    # 密码输入错误的时候会报错
            now = time.time()                                      # 故使用 try - except 语句
            # 将正确的密码输出到控制台
            print(f"Password is: {pwd}")
            return True
        except:
            return False
    # 用 bool 类型的返回值告诉主程序是否破解成功 (意思就是返回 True 了以后就停止)

    
    total = sum(len(dictionaries) ** k for k in lengths)    # 密码总数

    for pwd in tqdm(chain.from_iterable(all_passwd(dictionaries, maxlen) for maxlen in lengths), total=total):
        if extract(zfile, pwd):    # 记得extract函数返回的是bool类型的哦
            break


if __name__ == "__main__":
    main(sys.argv[1:])
