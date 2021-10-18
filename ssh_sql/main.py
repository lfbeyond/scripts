from outexcell import exccell_li
from ssh_sql import ssh_mysql,mysql_conn
from sendemail import Email_li
import configparser
cf = configparser.ConfigParser()
cf.read("./conf.ini", encoding="utf-8")


if __name__ == '__main__':
     print("\n")
     print("请选择你需要使用的数据库连接方式，并确保conf.ini已修改正确")

     connects=cf.get('param','connect_way').split(',')
     l_num=0
     for i in connects:
          print("* * * * * * ")
          print("{}): {}".format(l_num,i))
          l_num=l_num+1
     print("\n")
     choice=input("请输入0~{} 的数字进行选择需要使用的数据库连接方式：".format(l_num-1))
     print(" 你需要使用的数据库连接方式为：{}".format(connects[int(choice)]))
     
     if connects[int(choice)] == 'mysql_conn':
          try:
               sql=mysql_conn()
          except:
               print("连接数据库失败")
     elif connects[int(choice)] == 'ssh_mysql':
          try:
               sql=ssh_mysql()
          except:
               print("连接数据库失败")
     #开始连接到数据库


     
     
     #链接远程数据库到处excell
     # a=mysql_conn()
     # sql='select * from firstblog.blog_article limit 1 '
     # print(a.query(sql))



#      sql='''select
# l.ordercode as 订单号,
# CASE l.applyway
#   WHEN 9 THEN '高位视频'
#   WHEN 6 THEN 'pos机'
#   WHEN 4 THEN '微信公众号'
#   when 1 THEN '手机app'
#   when 15 THEN '微信小程序'
#   when 5 THEN '支付宝服务窗'
#  END 申请方式,
# FROM_UNIXTIME(l.addtime/1000,'%Y-%m-%d %H:%i:%s') AS 订单生成时间,
# FROM_UNIXTIME(l.intime/1000,'%Y-%m-%d %H:%i:%s') AS 入场时间,FROM_UNIXTIME(l.outtime/1000,'%Y-%m-%d %H:%i:%s') AS 出场时间,
#  CONCAT(IF(FLOOR((l.outtime-l.intime)/3600000)=0,'',CONCAT(FLOOR((l.outtime-l.intime)/3600000),'时')),FLOOR((l.outtime-l.intime)/60000%60),"分钟") AS 停车时长,
# (select sectionname from parkcloud_ya.com_section where sectionid=id) as 路段名称,
# l.berthcode AS 地磁编号,l.carplate AS 车牌,
# l.shouldpay as 应付金额,
# l.discount as 优惠金额,
# sum(tpr.actualpay) AS 实付金额,
# FROM_UNIXTIME(tpr.paytime/1000,'%Y-%m-%d %H:%i:%s') as 付款时间,
#  CASE tpr.paymentway
#   WHEN 1 THEN 'APP'
#   WHEN 2 THEN '现金'
#   WHEN 3 THEN '微信'
#   WHEN 4 THEN '公众号'
#   WHEN 5 THEN '支付宝'
#   WHEN 6 THEN 'pos'
#  END 支付渠道
#  ,
#   CASE tpr.paytype
#   WHEN 1 THEN '余额付款'
#   WHEN 2 THEN '现金'
#   WHEN 3 THEN '微信'
#   WHEN 4 THEN '支付宝'
#  END 支付方式
#
# from tra_order as l  left JOIN  tra_pay_road as tpr on tpr.orderid = l.id  and  tpr.isvalid = 1   where  l.isvalid = 1
#   and l.actualpay!=0 and tpr.state=2 and tpr.type!=3 group by l.ordercode '''


     # sql='select * from c_h5_prop_copy1;'
     # all_data,e_count,fields_complex=a.query(sql)
     # del a
     # #将查询结果导出到excell
     # b=exccell_li(fields_complex=fields_complex,title=title)
     # b.write_to_excel_with_openpyxl(all_data)

     # b.send_email()



