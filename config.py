# encoding:utf-8
from datetime import timedelta

project_website = 'http://0b31f3bf1c13.ngrok.io/'


class Config:
    SECRET_KEY = '1223343245235'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:2569535507Lw@127.0.0.1:3306/x_z_z_d'  # 数据库配置
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)  # session有效期为30天
    SQLALCHEMY_TRACK_MODIFICATIONS = False
