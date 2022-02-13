# 使用说明
暴力破解加密的zip文件,其实就是用不同密码不断尝试打开zip文件
```bash
breakzip.py -a <a|A|1> -c <Number of Chinese characters used in dictionary> -d <dictionary file> -f <zip file>
```
`-a a` 字典中添加小写字母
`-a A` 字典中添加大写字母
`-a 1` 字典中添加数字
`-a aA1` 字典中添加大小写字母和数字
`-d file` 指定中文字典文件`utf-8`编码
`-c number` 使用字典文件的前n个字符
`-f file` 要解密的zip文件
`-g number` 密码最大长度
`-l number` 密码长度等于