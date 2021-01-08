import datetime
import os
import time

from flask import render_template, request, Blueprint, session, \
    send_from_directory, flash, redirect, url_for

from config import project_website
from models import Course, Document, Assignment, Discussion
from models import Student
from models import db
from werkzeug.utils import secure_filename

course = Blueprint('course', __name__, template_folder='template', static_folder='static')


def get_Anonymous():
    Sno = 0000000000
    targets = Student.query.filter_by(Sno=Sno)
    return targets[0]


def create_preview_address(Document):
    filename = Document.Doc_name
    filepath = Document.Doc_path
    office_api = "https://view.officeapps.live.com/op/view.aspx?src="
    preview_address = office_api + project_website + 'course/' + filepath + '/' + filename
    return preview_address


def Caltime(date1, date2):
    # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    date1 = time.strptime(date1, "%Y-%m-%d %H:%M:%S")
    date2 = time.strptime(date2, "%Y-%m-%d %H:%M:%S")
    # 根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
    date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])
    sub = str(date2 - date1)
    if '-' in sub:
        return -1
    return int((date2 - date1).days)


def get_info():
    Sno = session.get('no')
    current_student = Student.query.filter_by(Sno=Sno)
    courses = current_student[0].courses
    return current_student, courses


def generate_homework_path(Cno, Sno, Assignment):
    base_path = os.path.dirname(__file__)  # 当前文件所在路径
    base_path = base_path + "/static/files/" + Cno + "/chapter" + str(Assignment.Assign_chapter) + "/homework"
    if not os.path.exists(base_path):  # 如果路径不存在
        os.makedirs(base_path)
    names = []
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isfile(item_path):
            if Sno in item:
                names.append(item)
    annex_names = []
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isfile(item_path):
            if '作业附件' in item:
                annex_names.append(item)
    return names, base_path, annex_names


@course.route('/<Cno>', methods=['GET', 'POST'])
def index(Cno):
    current_student, courses = get_info()
    current_course = Course.query.filter_by(Cno=Cno)
    return render_template('courseMain.html', course=current_course[0], student=current_student[0])


@course.route('/course_ware/<Cno>', methods=['GET', 'POST'])
def course_ware(Cno):
    current_student, courses = get_info()
    current_course = Course.query.filter_by(Cno=Cno)
    return render_template('courseware.html', course=current_course[0], student=current_student[0])


@course.route('/download_courseware/<Doc_no>', methods=['GET', 'POST'])
def download_courseware(Doc_no):
    if request.method == 'POST':
        target_Doc = Document.query.filter_by(Doc_no=Doc_no)
        filename = target_Doc[0].Doc_name
        filepath = target_Doc[0].Doc_path
        basedir = os.path.abspath(os.path.dirname(__file__))
        dir_path = os.path.join(basedir, filepath)
        return send_from_directory(dir_path, filename, as_attachment=True)


@course.route('/my_assignments/<Cno>', methods=['GET', 'POST'])
def my_assignments(Cno):
    current_student, courses = get_info()
    current_course = Course.query.filter_by(Cno=Cno)
    if current_course[0].assignments:
        current_date = time.strftime("%Y-%m-%d %H:%M:%S")
        homeworks = current_course[0].assignments
        for homework in homeworks:
            homework.Remaining_days = Caltime(current_date, str(homework.End_time))
            db.session.commit()
    return render_template('courseHomework.html', course=current_course[0], student=current_student[0],
                           homeworks=homeworks)


@course.route('/homework_info', methods=['GET', 'POST'])
def homework_info():
    Cno = request.args.get('Cno')
    Assign_no = request.args.get('Assign_no')
    current_student, courses = get_info()
    current_course = Course.query.filter_by(Cno=Cno)
    results = Assignment.query.filter_by(Assign_no=Assign_no)
    current_assignment = results[0]
    homework_name, homework_path, annex_name = generate_homework_path(Cno, current_student[0].Sno, current_assignment)
    return render_template('courseHomeworkInfo.html', course=current_course[0], student=current_student[0],
                           current_assignment=current_assignment, homework_name=homework_name,
                           homework_path=homework_path, annex_name=annex_name)


@course.route('/upload_assignment', methods=['POST'])
def upload_assignment():
    current_student, courses = get_info()
    if request.method == 'POST':
        homework = request.files.get('homework')
        Cno = request.args['Cno']
        Assign_no = request.args['Assign_no']
        results = Assignment.query.filter_by(Assign_no=Assign_no)
        current_assignment = results[0]
        homework.filename = current_student[0].Sno + os.path.splitext(homework.filename)[1]
        base_path = os.path.dirname(__file__)  # 当前文件所在路径
        base_path = base_path + "/static/files/" + Cno + "/chapter" + str(
            current_assignment.Assign_chapter) + "/homework"
        if not os.path.exists(base_path):  # 如果路径不存在
            os.makedirs(base_path)
        upload_path = os.path.join(base_path, secure_filename(homework.filename))
        homework.save(upload_path)
        current_student[0].assignments.append(current_assignment)
        db.session.commit()
        flash('作业提交成功！', 'success')
        current_course = Course.query.filter_by(Cno=Cno)
        return redirect(url_for('.homework_info', Cno=Cno, Assign_no=Assign_no))


@course.route('/download_my_homework', methods=['POST'])
def download_my_homework():
    if request.method == 'POST':
        filepath = request.args.get('filepath')
        filename = request.args.get('filename')
        return send_from_directory(filepath, filename, as_attachment=True)


@course.route('/download_homework_annex', methods=['POST'])
def download_homework_annex():
    if request.method == 'POST':
        filepath = request.args.get('filepath')
        filename = request.args.get('filename')
        return send_from_directory(filepath, filename, as_attachment=True)


@course.route('/discussion', methods=['GET', 'POST'])
def discussion():
    Cno = request.args.get('Cno')
    current_student, courses = get_info()
    current_course = Course.query.filter_by(Cno=Cno)
    discussions = current_course[0].discussions
    return render_template('courseForum.html', course=current_course[0], student=current_student[0], posts=discussions)


@course.route('/post_info', methods=['GET', 'POST'])
def post_info():
    Cno = request.args.get('Cno')
    post_id = request.args.get('post_id')
    temp1 = Discussion.query.filter_by(Discuss_no=post_id)
    current_post = temp1[0]
    current_student, courses = get_info()
    current_course = Course.query.filter_by(Cno=Cno)
    reply_posts = Discussion.query.filter_by(reply_which=post_id).order_by('Discuss_date')
    length = 0
    for item in reply_posts:
        length += 1
    return render_template('courseForumThread.html', course=current_course[0], student=current_student[0],
                           replys=reply_posts, current_post=current_post, total_amount=length)


@course.route('/reply_post', methods=['POST'])
def reply_post():
    if request.method == 'POST':
        Cno = request.args.get('Cno')
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        post_id = request.args.get('post_id')
        temp = Discussion.query.filter_by(Discuss_no=post_id)
        this_post = temp[0]
        current_student, courses = get_info()
        content = request.form.get('content')
        isAnonymousReply = request.form.get('isAnonymousReply')
        if isAnonymousReply == "1":
            new_reply = Discussion(Content=content, Discuss_date=current_time, reply_which=post_id)
            new_reply.students.append(get_Anonymous())
            this_post.reply_amount += 1
            db.session.add(new_reply)
            db.session.commit()
            return redirect(url_for('course.post_info', Cno=Cno, post_id=post_id))
        else:
            new_reply = Discussion(Content=content, Discuss_date=current_time, reply_which=post_id)
            print(current_student[0])
            current_student[0].discussions.append(new_reply)
            this_post.reply_amount += 1
            db.session.add(new_reply)
            db.session.commit()
            return redirect(url_for('course.post_info', Cno=Cno, post_id=post_id))


@course.route('/new_post', methods=['GET', 'POST'])
def new_post():
    Cno = request.args.get('Cno')
    current_course = Course.query.filter_by(Cno=Cno)
    current_student, courses = get_info()
    if request.method == 'GET':
        return render_template('courseNewThread.html', course=current_course[0], student=current_student[0])
    else:
        Cno = request.args.get('Cno')
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        current_student, courses = get_info()
        content = request.form.get('content')
        isAnonymousThread = request.form.get('isAnonymousThread')
        title = request.form.get('title')
        new_post = Discussion(Content=content, Discuss_date=current_time, Discuss_title=title, isNew=1)
        if isAnonymousThread == "1":
            new_post.students.append(get_Anonymous())
        else:
            new_post.students.append(current_student[0])
        current_course[0].discussions.append(new_post)
        db.session.add(new_post)
        db.session.commit()
        flash('发帖成功！', 'success')
        return redirect(url_for('course.discussion', Cno=Cno))

