# https://blog.csdn.net/qq_32903613/article/details/88693686
from math import ceil

import pandas as pd
from openpyxl import load_workbook
import pymysql


def getDataFromMysql():
    """
    连接数据库
    """
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='books', port=3306, charset='utf8')
    cur = conn.cursor()
    cur.execute("select * from Books_book")
    books = cur.fetchall()
    cur.close()
    conn.close()

    return books


def dataFrame2sheet(dataframe, excelWriter, countn):
    """
    pandas dataframe生成excel
    """
    # DataFrame转换成excel中的sheet表
    dataframe.to_excel(excel_writer=excelWriter, sheet_name="info_{0}".format(countn), index=None)

    excelWriter.save()
    excelWriter.close()


"""
excel中新增sheet表
"""


def excelAddSheet(dataframe, excelWriter, i):
    """
    在excel中新增sheet表
    """
    book = load_workbook(excelWriter.path)
    excelWriter.book = book

    dataframe.to_excel(excel_writer=excelWriter, sheet_name="info_{0}".format(i), index=None)

    excelWriter.close()


if __name__ == '__main__':

    books = getDataFromMysql()
    dataSet = []
    for i in books:
        dataSet.append(list(i))

    # excelPath
    excelPath = "./test.xlsx"

    # 生成DataFrame
    countn = ceil(len(dataSet) / 200)
    if countn <= 1:

        dataframe = pd.DataFrame(dataSet[:200])

        # 创建ExcelWriter 对象
        excelWriter = pd.ExcelWriter(excelPath, engine='openpyxl')

        # 生成excel

        dataFrame2sheet(dataframe, excelWriter, countn)

    # excel中增加sheet
    else:
        # 使用公共的excelWriter，数据不会被覆盖
        excelWriter = pd.ExcelWriter(excelPath, engine='openpyxl')
        for i in range(1, countn + 1):
            dataframe = pd.DataFrame(dataSet[(i - 1) * 200:i * 200])

            # 在excel里增加sheet，并写入数据。这个也可以实现
            # excelAddSheet(dataframe, excelWriter, i)

            # 生成excel
            dataFrame2sheet(dataframe, excelWriter, countn=i)