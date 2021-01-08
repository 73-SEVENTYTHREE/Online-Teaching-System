from flask import render_template, request, flash, Blueprint, session
from sqlalchemy import text
from models import Student, Course
import sys
from models import db
import os
from werkzeug.utils import secure_filename

student = Blueprint('student', __name__, template_folder='template', static_folder='static')


def get_info():
    Sno = session.get('no')
    current_student = Student.query.filter_by(Sno=Sno).all()
    if current_student:
        courses = current_student[0].courses
    else:
        courses = []
    return current_student, courses




@student.route("/", methods=['GET', 'POST'])
def index():
    current_student, courses = get_info()
    return render_template('studentMain.html', student=current_student[0], courses=courses)


@student.route("/change_pwd", methods=['GET', 'POST'])
def change_pwd():
    current_student, courses = get_info()
    if request.method == 'POST':
        oldPwd = request.form['oldPwd']
        first_pwd = request.form['newPwd1']
        second_pwd = request.form['newPwd2']
        if first_pwd != second_pwd:
            flash('前后密码不一致，请重新输入！', 'warning')
        else:
            if oldPwd != current_student[0].Spw:
                flash('原密码错误！', 'warning')
            else:
                current_student[0].Spw = first_pwd
                db.session.commit()
                flash('密码修改成功！', 'success')
    return render_template('SchangePwd.html', student=current_student[0])


@student.route('/personal_info', methods=['GET'])
def personal_info():
    current_student, courses = get_info()
    return render_template('studentMessage.html', student=current_student[0])


@student.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    current_student, courses = get_info()
    if request.method == 'POST':
        f = request.files['file']
        f.filename = current_student[0].Sno + os.path.splitext(f.filename)[1]
        base_path = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(base_path, 'static\\avatar', secure_filename(f.filename))
        f.save(upload_path)
        avatar_path = '/student/static/avatar/' + f.filename
        current_student[0].avatar_path = avatar_path
        db.session.commit()
        flash('头像上传成功！', 'success')
    return render_template('studentMessage.html', student=current_student[0])


@student.route('/my_courses', methods=['GET', 'POST'])
def my_courses():
    current_student, courses = get_info()
    course_info = []
    for course in courses:
        temp = Course.query.filter_by(Cno=course.Cno)
        course_info.append(temp[0])
    return render_template('studentMyCourses.html', student=current_student[0],
                           courses=course_info)


@student.route('/search_course', methods=['POST'])
def search_course():
    current_student, courses = get_info()
    if request.method == 'POST':
        key = request.form['search_key']
        result_course = Course.query.filter(
            Course.Cname.like("%" + key + "%") if key is not None else text('')
        ).all()
        return render_template('studentMyCourses.html', student=current_student[0],
                               courses=result_course)
