import pymysql
import xlwt
from datetime import datetime
from math import ceil


def getData(sql):
    # 创建数据库连接.
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='books', port=3306, charset='utf8')
    # 创建游标
    cur = conn.cursor()
    # 执行查询，
    cur.execute(sql)
    # fetchall()来获取所有内容。
    result = cur.fetchall()

    # 查询数据库表格字段
    col_result = cur.description  # 获取查询结果的字段描述，做为表格的头

    db_field = []
    for i in range(len(col_result)):
        db_field.append(col_result[i][0])
    # 关闭游标
    cur.close()
    # 关闭数据库连接
    conn.close()

    # 返给结果给函数调用者。
    return result, db_field


"""
使用xlwt中的Alignment来设置单元格的对齐方式，其中horz代表水平对齐方式，vert代表垂直对齐方式。
VERT_TOP          = 0x00    上端对齐
VERT_CENTER    = 0x01    居中对齐（垂直方向上）
VERT_BOTTOM  = 0x02    低端对齐
HORZ_LEFT        = 0x01    左端对齐
HORZ_CENTER   = 0x02    居中对齐（水平方向上）
HORZ_RIGHT     = 0x03    右端对齐
"""


def writeData2excel(name, sql):
    result, db_field = getData(sql)

    # 实例化一个Workbook()对象(即excel文件)
    wbk = xlwt.Workbook()
    # 设置对齐方式
    style = xlwt.XFStyle()
    al = xlwt.Alignment()
    al.horz = 0x01  # 左端对齐
    style.alignment = al

    # 基于每页xlrd每页最大纪录条数的考虑，分sheet存储。以200条每页为例
    countn = ceil(len(result) / 200)
    # 获取当前日期
    today = datetime.today()
    today_date = datetime.date(today)
    for m in range(1, countn + 1):
        sheet = wbk.add_sheet('Sheet_{0}'.format(m), cell_overwrite_ok=True)

        # 生成第一行，相当于表头
        for i in range(0, len(db_field)):
            # sheet1.write(0, i, db_field[i], set_style('Times New Roman', 220, True))
            # 0:表示从sheet的行数的下标，实际是第一行写入
            # i：表示从第几列开始
            # db_field[i]：表示把db_field重的数据从第0行写入
            sheet.write(0, i, db_field[i], style)

        # result为嵌套元祖
        for i in range(len(result[(m - 1) * 100:m * 100])):
            # 对result的每个子元素作遍历，
            for j in range(len(result[i])):
                # 将每一行的每个元素按行号i,列号j,写入到excel中。
                # 这里切片取得数据
                sheet.write(i + 1, j, (result[(m - 1) * 200:m * 200])[i][j], style)
        # excel名称保存。
        wbk.save(name + str(today_date) + '.xls')


if __name__ == '__main__':

    db_dict = {'Report_': 'select * from Books_book'}

    # 遍历字典每个元素的key和value。
    for k, v in db_dict.items():
        # 用字典的每个key和value调用writeData2excel函数。
        writeData2excel(k, v)