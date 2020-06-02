#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Mr Fan
# @Time: 2020年06月02
import re


def file_reader(file_path):
    """
    传入文件路径，读取文件内容，以字符串方式返回文件内容。
    :param file_path: (str)文件路径
    :return: (str) content 文件内容
    :raise:
    """

    try:
        with open(file_path, 'r', encoding="gbk") as file:
            content = file.read()
    except Exception as e:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

    return content


def save_file(content, file_path):
    """
    传入字符串内容，将内容保存到指定路径中。
    :param content: (str)文件内容
    :param file_path: (str)指定文件路径
    :return: None
    """
    assert isinstance(content, str)

    with open(file_path, "w", encoding="utf-8") as file:

        file.write(content)


def data_process(content):
    '''
    对传入的中文字符串进行清洗，去除邮箱、URL等无用信息。
    :param content: (str)待清洗的中文字符串
    :return: (str) content 清洗后的中文字符串
    '''
    assert isinstance(content, str)

    if content:
        content = re.sub('<.*?>', '', content)
        content = re.sub('【.*?】', '', content)
        # 剔除邮箱
        content = re.sub('^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$', '', content)
        content = re.sub('^[a-z\d]+(\.[a-z\d]+)*@([\da-z](-[\da-z])?)+(\.{1,2}[a-z]+)+$', '', content)
        # 剔除URL
        content = re.sub('^<([a-z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)$', '', content)
        content = re.sub('^[http]{4}\\:\\/\\/[a-z]*(\\.[a-zA-Z]*)*(\\/([a-zA-Z]|[0-9])*)*\\s?$','',content)
        # 剔除16进制值
        content = re.sub('^#?([a-f0-9]{6}|[a-f0-9]{3})$/', '', content)
        # 剔除IP地址
        content = re.sub('((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)', '', content)
        content = re.sub('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', '',
            content)
        # 剔除用户名密码名
        content = re.sub('^[a-z0-9_-]{3,16}$', '', content)
        content = re.sub('^[a-z0-9_-]{6,18}$', '', content)
        # 剔除HTML标签
        content = re.sub('^<([a-z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)$', '', content)
        # 剔除网络字符，剔除空白符
        content = content.strip().strip('\r\n\t').replace(u'\u3000', '').replace(u'\xa0', '')
        content = content.replace('\t', '').replace(' ', '').replace('\n', '').replace('\r', '')

    return content


def get_sentences(content):
    """
    传入一篇中文文章，获取文章中的每一个句子，返回句子列表。对中文、日文文本进行拆分。
    # todo 可以考虑说话部分的分句， 例如‘xxx：“xxx。”xx，xxxx。’
    :param content: (str) 一篇文章
    :return: sentences(list) 分句后的列表
    :raise: TypeError
    """
    if not isinstance(content, str):
        raise TypeError

    split_sign = '%%%%'  # 需要保证字符串内本身没有这个分隔符
    sign = '$PACK$'  # 替换的符号用: $PACK$
    search_pattern = re.compile('\$PACK\$')
    pack_pattern = re.compile('(“.+?”|（.+?）|《.+?》|〈.+?〉|[.+?]|【.+?】|‘.+?’|「.+?」|『.+?』|".+?"|\'.+?\')')
    pack_queue = re.findall(pack_pattern, content)
    content = re.sub(pack_pattern, sign, content)

    pattern = re.compile('(?<=[。？！])(?![。？！])')
    result = []
    while content != '':
        s = re.search(pattern, content)
        if s is None:
            result.append(content)
            break
        loc = s.span()[0]
        result.append(content[:loc])
        content = content[loc:]

    result_string = split_sign.join(result)
    while pack_queue:
        pack = pack_queue.pop(0)
        loc = re.search(search_pattern, result_string).span()
        result_string = f"{result_string[:loc[0]]}{pack}{result_string[loc[1]:]}"

    sentences = result_string.split(split_sign)

    return sentences


if __name__ == '__main__':
    content = ""
    sentence = data_process(content)

