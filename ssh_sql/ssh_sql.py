# _*_ coding:utf-8 _*_
import pymysql
from sshtunnel import SSHTunnelForwarder
import configparser
cf = configparser.ConfigParser()
cf.read("./conf.ini", encoding="utf-8")

class ssh_mysql:
    def __init__(self):
        self.dbname = (cf.get('ssh_sql','dbname'))
        self.server = SSHTunnelForwarder(
            ((cf.get('ssh_sql','IP_B')), (cf.getint('ssh_sql','Port_B'))),
            ssh_username=(cf.get('ssh_sql','username_B')),
            ssh_password=(cf.get('ssh_sql','password_B')),
            remote_bind_address=((cf.get('ssh_sql','IP_C')), (cf.getint('ssh_sql','Port_C')))) # 数据库存放服务器C配置
        self.server.start()
        self.conn = pymysql.connect(host='127.0.0.1', # 本机主机A的IP（必须是这个）
                                    port=self.server.local_bind_port,
                                    user=(cf.get('ssh_sql','username_sql')),
                                    password=(cf.get('ssh_sql','password_sql')),
                                    db=self.dbname,
                                    charset='utf8')
        print('数据库连接成功！')
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cur = self.conn.cursor()
        print('游标设置成功！')

    def __del__(self):  # 析构函数，实例删除时触发
        self.cur.close()
        self.conn.close()
        self.server.stop()
        print('关闭')

    def query(self, sql):
        print('开始执行查询语句{}'.format(sql))
        # 使用 execute()  方法执行 SQL 查询
        count=self.cur.execute(sql)
        print('sql{}执行成功！'.format(sql))
        print(count)
        return self.cur.fetchall(),count,self.cur.description

    def exec(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            print('sql{}执行成功！'.format(sql))
        except Exception as e:
            print(str(e))
            self.conn.rollback()


# 直连的mysql
class mysql_conn:
    def __init__(self):
        print(cf.get('mysql_conn','port'))
        self.dbname = (cf.get('mysql_conn','dbname'))
        self.conn = pymysql.connect(host=(cf.get('mysql_conn','ip')), # 本机主机A的IP（必须是这个）
                                    port=(cf.getint('mysql_conn','port')),
                                    user=(cf.get('mysql_conn','username')),
                                    password=(cf.get('mysql_conn','password')),
                                    db=self.dbname,
                                    charset='utf8')
        print('数据库连接成功！')
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cur = self.conn.cursor()
        print('游标设置成功！')

    def __del__(self):  # 析构函数，实例删除时触发
        self.cur.close()
        self.conn.close()
        print('关闭')

    def query(self, sql):
        print('开始执行查询语句{}'.format(sql))
        # 使用 execute()  方法执行 SQL 查询
        count=self.cur.execute(sql)
        print('sql{}执行成功！'.format(sql))
        print(count)
        return self.cur.fetchall(),count,self.cur.description

    def exec(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            print('sql{}执行成功！'.format(sql))
        except Exception as e:
            print(str(e))
            self.conn.rollback()




