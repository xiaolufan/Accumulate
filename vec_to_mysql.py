#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Mr Fan
# @Time: 2020年05月14
import numpy as np
import pymysql as ml

x = np.load("./vec_data/000.npy")
temp = x[0]
# vector = temp.tostring()
eventid = "0"
# cameoid="0"


def insert_to_db(eventid, cameoid, vector):
    db = ml.connect(host="localhost", user="root", password="12341234", db="exercise", port=3306)
    cur = db.cursor()
    sql = "insert into event_vec_table(event_id,cameo,event_vec) values(%s,%s,%s)"

    try:
        cur.execute(sql, (eventid, cameoid, vector))
        # 执行sql语句
        db.commit()
        # 提交到数据库中
        print("提交成功！")
    except Exception as e:
        # 捕获异常
        raise e
    finally:
        db.close()  # 关闭连接


def get_answer_sentence(cursor, event_id_list):
    """
    到数据库中根据事件id列表检索所有的事件短句
    :param cursor:
    :param event_id_list:
    :return:
    """
    print(event_id_list)
    sql = 'select shorten_sentence from ebm_event_info where event_id in %s'
    
    # 从数据库中检索列表中的东西，必须转化为元组且必须再套一层
    cursor.execute(sql, (tuple(event_id_list),))

    all = cursor.fetchall()
    print(all)


    return [once[0] for once in all]
    

def readData():
    db = ml.connect(host="localhost", user="root", password="12341234", db="exercise", port=3306)
    # 连接数据库对象
    cur = db.cursor()
    # 游标对象
    sql = "select event_vec from event_vec_table"
    # 定义好sql语句，%s是字符串的占位符
    try:
        cur.execute(sql)
        # 执行sql语句
        results = cur.fetchall()
        # 获取所有结果集
        numArr = np.fromstring(string=results[0][0], dtype=np.float32)
        # 将读取到的字节流转化为ndarray数组
        print(numArr)
        db.commit()
        # 提交到数据库中
    except Exception as e:
        # 捕获异常
        raise e
    finally:
        db.close()  # 关闭连接

    return numArr

def del_vec(eventid):
    db = ml.connect(host="localhost", user="root", password="12341234", db="exercise", port=3306)
    # 连接数据库对象
    cur = db.cursor()
    # 游标对象
    sql = "delete from event_vec_table where event_id=(%s)"
    # 定义好sql语句，%s是字符串的占位符

    try:
        cur.execute(sql, (eventid))
        db.commit()
    except Exception as e:
        raise e
    finally:
        db.close()


if __name__=="__main__":
    numArr = readData()
    del_vec(eventid)

