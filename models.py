from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# 多对多关系表
# 学生和课程关系表
tb_student_course = db.Table('tb_student_course',
                             db.Column('Sno', db.String(10), db.ForeignKey('student.Sno')),
                             db.Column('Cno', db.String(10), db.ForeignKey('course.Cno'))
                             )

# 教师和课程关系表
tb_teacher_course = db.Table('tb_teacher_course',
                             db.Column('Tno', db.String(10), db.ForeignKey('teacher.Tno')),
                             db.Column('Cno', db.String(10), db.ForeignKey('course.Cno'))
                             )

# 课程评价和课程关系表
tb_comment_course = db.Table('tb_comment_course',
                             db.Column('Comment_no', db.Integer, db.ForeignKey('comment.Comment_no')),
                             db.Column('Cno', db.String(10), db.ForeignKey('course.Cno'))
                             )

# 作业和课程关系表
tb_assignment_course = db.Table('tb_assignment_course',
                                db.Column('Assign_no', db.Integer, db.ForeignKey('assignment.Assign_no')),
                                db.Column('Cno', db.String(10), db.ForeignKey('course.Cno'))
                                )

# 帖子和课程关系表
tb_discussion_course = db.Table('tb_discussion_course',
                                db.Column('Discuss_no', db.Integer, db.ForeignKey('discussion.Discuss_no')),
                                db.Column('Cno', db.String(10), db.ForeignKey('course.Cno'))
                                )

# 课件和课程关系表
tb_document_course = db.Table('tb_document_course',
                              db.Column('Doc_no', db.Integer, db.ForeignKey('document.Doc_no')),
                              db.Column('Cno', db.String(10), db.ForeignKey('course.Cno'))
                              )

# 课程评价和学生关系表
tb_comment_student = db.Table('tb_comment_student',
                              db.Column('Comment_no', db.Integer, db.ForeignKey('comment.Comment_no')),
                              db.Column('Sno', db.String(10), db.ForeignKey('student.Sno'))
                              )

# 帖子和学生关系表
tb_discussion_student = db.Table('tb_discussion_student',
                                 db.Column('Discuss_no', db.Integer, db.ForeignKey('discussion.Discuss_no')),
                                 db.Column('Sno', db.String(10), db.ForeignKey('student.Sno'))
                                 )

# 作业和学生关系表
tb_assignment_student = db.Table('tb_assignment_student',
                                 db.Column('Assign_no', db.Integer, db.ForeignKey('assignment.Assign_no')),
                                 db.Column('Sno', db.String(10), db.ForeignKey('student.Sno'))
                                 )

# 帖子和教师关系表
tb_discussion_teacher = db.Table('tb_discussion_teacher',
                                 db.Column('Discuss_no', db.Integer, db.ForeignKey('discussion.Discuss_no')),
                                 db.Column('Tno', db.String(10), db.ForeignKey('teacher.Tno'))
                                 )


# 作业
class Assignment(db.Model):
    # 定义表名
    __tablename__ = 'assignment'
    # 定义字段
    Assign_no = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Assign_name = db.Column(db.String(20))
    type = db.Column(db.String(6))
    Begin_time = db.Column(db.DateTime)
    End_time = db.Column(db.DateTime)
    Description = db.Column(db.String(1000))
    Assign_path = db.Column(db.String(50))
    Assign_chapter = db.Column(db.Integer)
    Remaining_days = db.Column(db.Integer)
    percent = db.Column(db.Integer)
    score = db.Column(db.Integer)


# 讨论信息
class Discussion(db.Model):
    # 定义表名
    __tablename__ = 'discussion'
    # 定义字段
    Discuss_no = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Discuss_title = db.Column(db.String(30))
    Content = db.Column(db.String(200))
    Discuss_date = db.Column(db.DateTime)
    # 是否为置顶的帖子
    isTop = db.Column(db.Integer, default=0)
    # 是否为帖子（即第一条讨论信息）
    isNew = db.Column(db.Integer, default=0)
    # 回复哪个帖子
    reply_which = db.Column(db.Integer, default=-1)
    # 回帖数
    reply_amount = db.Column(db.Integer, default=0)
    poster_identity = db.Column(db.String(2), default='学生')


# 文件
class Document(db.Model):
    # 定义表名
    __tablename__ = 'document'
    # 定义字段
    Doc_no = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Doc_type = db.Column(db.String(10))
    Doc_name = db.Column(db.String(20))
    Doc_chapter = db.Column(db.Integer)
    Doc_description = db.Column(db.String(20))
    Doc_path = db.Column(db.String(100))
    Doc_authority = db.Column(db.String(10))
    Doc_preview_address = db.Column(db.String(200))


# 评价
class Comment(db.Model):
    # 定义表名
    __tablename__ = 'comment'
    # 定义字段
    Comment_no = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Course_score = db.Column(db.Integer)
    Content = db.Column(db.String(100))


# 学生
class Student(db.Model):
    # 定义表名
    __tablename__ = 'student'
    # 定义字段
    Sno = db.Column(db.String(10), primary_key=True)
    Sname = db.Column(db.String(8))
    Spw = db.Column(db.String(20))
    Ssex = db.Column(db.String(2))
    Class = db.Column(db.String(10))
    Sage = db.Column(db.Integer)
    Stel = db.Column(db.String(15))
    Saddr = db.Column(db.String(30))
    Syear = db.Column(db.String(4))
    Sprofessional = db.Column(db.String(20))
    avatar_path = db.Column(db.String(100), default="/student/static/avatar/default.jpg")
    comments = db.relationship('Comment',
                               secondary=tb_comment_student,
                               backref='students',
                               lazy='dynamic')
    assignments = db.relationship('Assignment',
                                  secondary=tb_assignment_student,
                                  backref='students',
                                  lazy='dynamic')
    discussions = db.relationship('Discussion',
                                  secondary=tb_discussion_student,
                                  backref='students',
                                  lazy='dynamic')


# 老师
class Teacher(db.Model):
    # 定义表名
    __tablename__ = 'teacher'
    # 定义字段
    Tno = db.Column(db.String(10), primary_key=True)
    Tname = db.Column(db.String(8))
    Tpw = db.Column(db.String(20))
    Tsex = db.Column(db.String(2))
    Tage = db.Column(db.Integer)
    Ttel = db.Column(db.String(15))
    Taddr = db.Column(db.String(30))
    profile = db.Column(db.String(1000))
    Tprofessional = db.Column(db.String(20))
    avatar_path = db.Column(db.String(100), default="/teacher/static/avatar/default.jpg")
    discussions = db.relationship('Discussion',
                                  secondary=tb_discussion_teacher,
                                  backref='teachers',
                                  lazy='dynamic')


# 管理员
class Admin(db.Model):
    # 定义表名
    __tablename__ = 'admin'
    # 定义字段
    Ano = db.Column(db.String(10), primary_key=True)
    Aname = db.Column(db.String(8))
    Apw = db.Column(db.String(20))
    Asex = db.Column(db.String(2))
    Aage = db.Column(db.Integer)
    Atel = db.Column(db.String(15))
    Aaddr = db.Column(db.String(30))
    Aemail = db.Column(db.String(20))
    Abirth = db.Column(db.Date)


# 助教
class Assistant(db.Model):
    # 定义表名
    __tablename__ = 'assistant'
    # 定义字段
    Asno = db.Column(db.String(10), primary_key=True)
    Asname = db.Column(db.String(8))
    Aspw = db.Column(db.String(20))
    Assex = db.Column(db.String(2))
    Asage = db.Column(db.Integer)
    Astel = db.Column(db.String(15))
    Asaddr = db.Column(db.String(30))


# 课程
class Course(db.Model):
    # 定义表名
    __tablename__ = 'course'
    # 定义字段
    Cno = db.Column(db.String(10), primary_key=True)
    Cname = db.Column(db.String(8))
    Cdate = db.Column(db.Date)
    Ctime = db.Column(db.String(20))
    Is_ongoing = db.Column(db.String(4))
    Cover_path = db.Column(db.String(40))
    introduction = db.Column(db.String(300))
    Ctype = db.Column(db.String(10))
    students = db.relationship('Student',
                               secondary=tb_student_course,
                               backref='courses',
                               lazy='dynamic')
    teachers = db.relationship('Teacher',
                               secondary=tb_teacher_course,
                               backref='courses',
                               lazy='dynamic')
    comments = db.relationship('Comment',
                               secondary=tb_comment_course,
                               backref='courses',
                               lazy='dynamic')
    assignments = db.relationship('Assignment',
                                  secondary=tb_assignment_course,
                                  backref='courses',
                                  lazy='dynamic')
    discussions = db.relationship('Discussion',
                                  secondary=tb_discussion_course,
                                  backref='courses',
                                  lazy='dynamic')
    documents = db.relationship('Document',
                                secondary=tb_document_course,
                                backref='courses',
                                lazy='dynamic')
