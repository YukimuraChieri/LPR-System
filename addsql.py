import pymysql
import time


def db_open():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "password", "chepai")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    return db, cursor


def adddata(text, confidence, source, time1, color, db, cursor):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # print(type(time1))
    sql = "insert into carinfo(date,text,confidence,time,source, color) values ('"+date+"'"+","+"'"+text+"'"+","+"'"+confidence+"'"+","+"'"+time1+"'"+","+"'"+source+"'"+","+"'"+color+"')"
    if text == "":
        print("未检测到车牌")
        pass
    else:
        print(sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
            print("数据库写入数据成功")
        except:
            # 发生错误时回滚
            db.rollback()
            print("数据库写入数据失败")


def db_search(cursor, name, password):

    # SQL 查询语句
    sql = "select * from userinfo where name = "+"'"+name+"'"
    try:
        print(sql)
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results[0][1])
        if results[0][1] == password:
            return 1
        else:
            print("密码错误，请检查后重新输入")
            return 2
    except:
        print("Error: unable to fetch data")
        print("Error: 该用户未注册")
        return 3
        # 该用户未注册


def db_search_text(cursor, text):

    # SQL 查询语句
    sql = "select * from carinfo_register where text = "+"'"+text+"'"
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    if len(results) > 0:
        return True
    else:
        print("")
        return False


def db_search_path(cursor, source):

    # SQL 查询语句
    sql = "select * from carinfo where source = "+"'"+source+"'"
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    if len(results) > 0:
        return True
    else:
        print("不存在的来源")
        return False


def db_search_color(cursor, color):

    # SQL 查询语句
    sql = "select * from carinfo where color = "+"'"+color+"'"
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()

    return results


def db_close(db):
    # 关闭数据库连接
    db.close()


def adduser(name, password, db, cursor):
    num = db_search(cursor, name, password)
    if num == 3:
        sql = "insert into userinfo(name,password) values("+"'"+name+"'"+","+"'"+password+"')"
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        print("注册成功")
    else:
        print("注册失败")
        print("请勿重复注册")
    return num


def search_mh(a, b, c, d, e, f, g, cursor):
    if a == "":
        a = "_"
    if b == "":
        b = "_"
    if c == "":
        c = "_"
    if d == "":
        d = "_"
    if e == "":
        e = "_"
    if f == "":
        f = "_"
    if g == "":
        g = "_"
    # SQL 查询语句

    sql = "select * from carinfo where text like "+"'"+a+b+c+d+e+f+g+"'"

    results = ""
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for res in results:
            print(res)
    except:
        print("Error: unable to fetch data")
    return results


if __name__ == '__main__':

    db, cursor = db_open()
    # adduser("user2", "123456", db, cursor)
    # name = "user1"
    # password = "password"
    # db_search(cursor, name, password)
    #
    a = "浙"
    b = "A"
    c = ""
    d = ""
    e = ""
    f = ""
    g = ""
    # search_mh(a, b, c, d, e, f, g, cursor)
    # db_search_path(cursor, "D:/python/python_work/cnsoftbei_1/test-imgs-piliang/018.jpg")
    adddata("chepai", "confidence", "source", "time", "color", db, cursor)
    db_close(db)
