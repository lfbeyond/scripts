# -*- coding: utf-8 -*-

import traceback
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
import smtplib
import configparser

cf = configparser.ConfigParser()
cf.read("./conf.ini", encoding="utf-8")



class Email_li(object):
	def __init__(self,port=(cf.getint('email','port')),host=(cf.get('email','host')),sender=(cf.get('email','user')),password=(cf.get('email', 'pwd')),**kwargs):
		self.sender = sender
		try:
			print("开始登陆 {0}{1}".format(host,port))
			#腾讯企业邮箱,必须使用ssl
			self.server = smtplib.SMTP_SSL(host, port)
			print("开始登陆 {0}".format(sender))
			self.server.login(sender, password)
		except smtplib.SMTPException as e:
			print("connect smtp failed, {}".format(traceback.format_exc()))

	def send(self, to_user=(cf.get('email','to_user')), subject=(cf.get('email','subject')), content=(cf.get('email','content')), content_type="plain", reports_path=(cf.get('email','reports_path'))):
		"""
		:param to_user: 对方邮箱
		:param content: 邮件正文
		:param title: 邮件主题
		:param reports_path: {发送时测试报告名称:测试报告路径} or [测试报告路径] or 测试报告路径
		"""
		receivers = self._format_user(to_user)
		msg = self._attach_email_body(content, reports_path, content_type)
		#print("开始发送邮件 {},{},{},{}".format(self.sender,receivers,subject,msg))
		msg["From"] = self.sender
		msg["To"] = ','.join(receivers)
		msg["Subject"] = subject
		self.server.sendmail(self.sender, receivers, msg.as_string())
		self.server.quit()
		print("send email success")

	def _format_user(self, to_user):
		recvs = []
		if isinstance(to_user, str):
			if ',' in to_user:
				recvs = to_user.split(',')
			else:
				recvs.append(to_user)
		elif isinstance(to_user, list):
			recvs = to_user
		else:
			raise TypeError('Type error, receiver should be list or str')
		return recvs

	def _attach_email_body(self, content, reports_path, content_type):
		"""
		添加附件
		:param content:
		:param html_content:
		:param reports_path:
		:return:
		"""
		msg = MIMEMultipart()
		text_msg = MIMEText(content, content_type, "utf8")
		msg.attach(text_msg)
		if not reports_path:
			return msg
		if isinstance(reports_path, str):
			print(reports_path)
			filename = basename(reports_path)
			print(filename)
			tmp_file = self._create_application(reports_path, filename)
			msg.attach(tmp_file)
		elif isinstance(reports_path, list):
			for report_path in reports_path:
				filename = basename(report_path)
				tmp_file = self._create_application(report_path, filename)
				msg.attach(tmp_file)
		elif isinstance(reports_path, dict):
			for filename, report_path in reports_path.items():
				tmp_file = self._create_application(report_path, filename)
				msg.attach(tmp_file)
		else:
			raise TypeError('Type error, receiver should be list dict or str')
		return msg

	@staticmethod
	def _create_application(report_path, filename):
		tmp_file = MIMEApplication(open(report_path, 'rb').read())
		tmp_file.add_header('Content-Disposition', 'attachment', filename=filename)
		return tmp_file

#
# if __name__ == '__main__':
# 	title = "test title"
# 	content = "test content"
# 	reports_path = ["login.html", "1.jpg"]
# 	toaddrs = ["zh@163.com"]
# 	from_addr = "zh@163.com"
# 	m = Email('smtp.163.com', "zh@163.com", 'pwd')
# 	m.send(toaddrs, title, content, reports_path=reports_path)