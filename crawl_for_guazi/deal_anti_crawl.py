import html
import re

font_str = ['\\ue9ce', '\\ue76e', '\\ue1d0', '\\ueaf2', '\\ue891', '\\ue325', '\\ue41d', '\\ue52e', '\\ue630', '\\uec4c']
font_int = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
font_dict = dict(zip(font_str, font_int))

pattern = re.compile(r'\\u.{4}')

def repl(matched):
    '''
    正则表达替换函数
    '''
    value = str(matched.group('value'))
    if font_str.count(value):
        return font_dict[value]

def deal_str(str):
    '''
    处理字符串
    '''
    if str.find("&#") > -1:
        # 字符串包含HTML编码元素，且该编码只用于数字
        newstr = bytes.decode(html.unescape(str).encode('unicode_escape'))
        newstr = pattern.sub(lambda x: font_dict.get(x.group(), x.group()), newstr)
        str = newstr.split('\\', maxsplit=1)[0] + ('\\' + newstr.split('\\', maxsplit=1)[1]).encode('utf8').decode('unicode_escape')
    return str
