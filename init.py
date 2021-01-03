# encoding:utf-8
from teacher.tearcher import teacher
from index.index import index
from student.student import student
from course.course import course
from admin.admin import admin
from flask import Flask
from models import db
from config import Config, project_website
from models import Teacher, Admin, Student, Assistant, Course, Comment, Assignment, Document, Discussion
from flask_bootstrap import Bootstrap
import importlib
import sys
import pymysql
from flask_sqlalchemy import SQLAlchemy
from course.course import create_preview_address

pymysql.install_as_MySQLdb()
importlib.reload(sys)
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(index, url_prefix='/')
    app.register_blueprint(teacher, url_prefix='/teacher')
    app.register_blueprint(student, url_prefix='/student')
    app.register_blueprint(course, url_prefix='/course')
    app.register_blueprint(admin, url_prefix='/admin')
    app.app_context().push()
    bootstrap.init_app(app)
    t1 = Teacher(Tno="20201217", Tname="金波", Tpw="123456", Tsex="男", Tage=40, Ttel="13700000000", Taddr="浙江省杭州市西湖区浙大路38号",
                 profile="教授，博士生导师。1993年6月毕业于浙江大学流体传动及控制专业，获学士学位。1998年9"
                         "月于浙江大学流体传动及控制专业获得博士学位，同年留校任教。作为主要完成人获得国家技术发明奖二等奖一项，省部级科技进步一等奖两项。承担多项国家自然科学基金、863"
                         "计划重点项目及浙江省自然科学基金重点项目。承担多项横向科研项目，均圆满地完成了研发任务。共在国内外学术刊物与国际会议上发表论文七十余篇，其中SCI/EI"
                         "收录三十余篇。获得国家发明专利、软件著作权二十余项。", Tprofessional='计算机学院')
    t2 = Teacher(Tno="20201218", Tname="苏德矿", Tpw="123456", Tsex="男", Tage=40, Ttel="13700000000", Taddr="浙江省杭州市西湖区浙大路38号",
                 profile="浙江大学理学院数学系教授，浙江省精品课程《微积分》课程负责人、浙江大学公共数学基础课教学指导委员会副主任，浙江大学微积分课程负责人，浙江省高校高等数学教学研究会常务理事兼秘书长，清华大学萧树铁教授主持的前国家教委“面向21世纪教学内容和课程体系改革”研究课题组成员。", Tprofessional='数学学院')
    t3 = Teacher(Tno="20201219", Tname="邵健", Tpw="123456", Tsex="男", Tage=40, Ttel="13700000000", Taddr="浙江省杭州市西湖区浙大路38号",
                 profile="2003年7月从南京大学电子科学与工程系获得理学学士学位；2008年7月从中国科学院声学研究所获得信号与信息处理专业工学博士学位；2008年7"
                         "月博士毕业后直接进入浙江大学计算机学院计算机应用学科从事师资博后研究工作，并在2010年9"
                         "月留校，浙大工作期间研究方向拓展为视音频智能分析、跨媒体挖掘与检索、分布式计算，作为负责人承担了中国博士后基金面上与特别资助项目、教育部-微软重点实验室联合项目、省优先主题社会发展项目子课题等多个项目，并作为青年骨干参与承担了973项目子课题、NSFC重大研究计划、核高基重大专项子课题等多个项目。", Tprofessional='计算机学院')
    s1 = Student(Sno="3180100000", Sname="王小明", Spw="123456", Ssex="男", Sage=20, Stel="13700000000", Saddr="浙江省杭州市西湖区浙大路38号",
                 Class="软工1802", Syear="2018", avatar_path='/student/static/avatar/3180100000.jpg', Sprofessional='软件工程')
    s2 = Student(Sno="3180100001", Sname="韩梅梅", Spw="123456", Ssex="女", Sage=20, Stel="13700000000", Saddr="浙江省杭州市西湖区浙大路38号",
                 Class="计科1802", Syear="2018", Sprofessional='计算机科学与技术')
    s3 = Student(Sno="0000000000", Sname="匿名")
    a1 = Admin(Ano='admin', Aname='管理员', Atel='13700000000', Aaddr='玉泉', Aage=30, Asex='男', Apw='123456')
    Doc1 = Document(Doc_no=1, Doc_name="客户投诉处理.pptx", Doc_path="static/files/100001/chapter1/courseware", Doc_type="pptx",
                    Doc_chapter=7, Doc_description="客户投诉处理相关事务", Doc_authority='可下载')
    Ass1 = Assignment(Assign_no=1, Assign_path='static/files/100001/chapter1', Begin_time='2020-12-31 10:00:20',
                      End_time='2021-1-3 11:30:20', Description='平时作业1，请大家参照作业要求的ppt完成', Assign_chapter=7,
                      Assign_name='C1.3作业', type='docx', percent=15, score=90)
    Ass2 = Assignment(Assign_no=2, Assign_path='static/files/100001/chapter1', Begin_time='2020-12-31 10:00:45',
                      End_time='2020-12-25 11:11:45', Description='平时作业2，请大家参照模板完成', Assign_chapter=8,
                      Assign_name='C1.4作业', type='docx', percent=15)
    Doc1.Doc_preview_address = create_preview_address(Doc1)
    D1 = Discussion(Discuss_no=1, Discuss_date='2020-1-1 12:00:00', Discuss_title='请问大家需求优先级排序有些什么好方法呢？',
                    Content='rt，大家组里都是采用什么办法来排需求优先级呢，我觉得QFD比较完善...', isTop=1, isNew=1,
                    reply_amount=1)
    D2 = Discussion(Discuss_no=2, Discuss_date='2020-1-2 12:00:00', Content='我觉得我们这个项目三层优先级就够了', isTop=0, isNew=0,
                    reply_amount=0, reply_which=1)
    D3 = Discussion(Discuss_no=3, Discuss_date='2020-1-1 13:10:08', Discuss_title='关于期末答辩的安排', Content='各位同学：期末教学总体安排的'
                                                                                         '通知及4个附件已发布，请查阅，并遵照执'
                                                                                         '行。最后一周的那次上课就调整到16日的'
                                                                                         '答辩了', isTop=1, isNew=1,
                    reply_amount=0, poster_identity='教师')
    a1 = Admin(Ano="admin", Aname="张小红", Apw="123456", Asex="女", Aaddr="浙江省杭州市西湖区浙大路38号", Aage=23, Atel="13771011111",
               Aemail='zxh@163.com', Abirth='1995-5-20')
    assistant = Assistant(Asno="123", Asname="助教", Aspw="123456", Assex="男", Asage=23, Asaddr="浙江省杭州市西湖区浙大路38号")
    course1 = Course(Cno='100001', Ctype='计算机类', Cname='软件工程管理', Cdate='2020-9-27', Ctime="周三2、3、4节", Is_ongoing="正在进行",
                     Cover_path="/course/static/cover/100001.jpg", introduction="软件工程管理是为了使软件项目能够按照预定的成本、"
                                                                                "进度、质量顺利完成，而对人员（People）、产品（"
                                                                                "Product）、过程（Process）和项目(Project)"
                                                                                "进行分析和管理的活动。")
    course2 = Course(Cno='100002', Ctype='自然科学类', Cname='微积分甲', Cdate='2020-9-28', Ctime="周四1、2节", Is_ongoing="已结课",
                     Cover_path="/course/static/cover/100002.jpg", introduction="微积分学，数学中的基础分支。内容主要包括函数、极"
                                                                                "限、微分学、积分学及其应用。函数是微积分研究的基"
                                                                                "本对象，极限是微积分的基本概念，微分和积分是特定过程特定形式的极限。17"
                                                                                "世纪后半叶，英国数学家艾萨克·牛顿和德国数学家G.W"
                                                                                ".莱布尼兹，总结和发展了几百年间前人的工作，建立了"
                                                                                "微积分，但他们的出发点是直观的无穷小量，因此尚缺"
                                                                                "乏严密的理论基础。19世纪A.-L.柯西和K.魏尔斯特"
                                                                                "拉斯把微积分建立在极限理论的基础上；加之19世纪后"
                                                                                "半叶实数理论的建立，又使极限理论有了严格的理论基"
                                                                                "础，从而使微积分的基础和思想方法日臻完善。")
    course1.students = [s1]
    course1.assignments = [Ass1, Ass2]
    course1.discussions = [D1, D2, D3]
    D1.students = [s1]
    s2.discussions = [D2]
    course1.documents = [Doc1]
    course1.teachers = [t1, t3]
    course2.students = [s1]
    course2.teachers = [t2]
    t1.discussions = [D3]

    db.drop_all()
    db.create_all()
    db.session.add_all([course2, t2, t1, t3, s1, s3, s2, assistant, a1])
    db.session.commit()
    return app
