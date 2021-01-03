from flask import render_template, request, flash, make_response, url_for, redirect, Blueprint, session
from sqlalchemy import text
from models import Student, Course, Teacher, Admin
import sys
from models import db
import os
from werkzeug.utils import secure_filename
from io import BytesIO
import xlsxwriter

admin = Blueprint('admin', __name__, template_folder='template', static_folder='static')


def create_courses_flie(courses):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('courses')
    title = ["课程编号", "课程名称", '课程类型', "开课教师", "开课时间", "上课时间", "开课状态", "课程简介"]
    worksheet.write_row('A1', title)
    for i in range(len(courses)):
        row = [courses[i].Cno, courses[i].Cname, courses[i].Ctype, courses[i].teachers[0].Tname,
               courses[i].Cdate.strftime("%Y-%m-%d"), courses[i].Ctime, courses[i].Is_ongoing, courses[i].introduction]
        worksheet.write_row('A' + str(i + 2), row)
    workbook.close()
    response = make_response(output.getvalue())
    output.close()
    return response


@admin.before_request
def before_admin():
    if 'identity' in session and session['identity'] == 'admin':  # 如果身份是学生就通过
        pass
    else:  # 否则返回登录界面
        flash('您还未用管理员账号登录！', 'danger')
        return redirect(url_for('index.all_index'))


@admin.route('/', methods=['GET', 'POST'])
def admin_index():
    students = Student.query.all()
    teachers = Teacher.query.all()
    courses = Course.query.all()
    admins = Admin.query.all()
    total_number = (len(students) + len(teachers) + len(courses) + len(admins)) / 100
    p1 = len(students) / total_number
    p2 = len(teachers) / total_number
    p3 = len(courses) / total_number
    p4 = len(admins) / total_number
    return render_template('adm_index.html', usr_number=len(students), teacher_number=len(teachers),
                           course_number=len(courses),
                           admin_number=len(admins), total_number=total_number, p1=p1, p2=p2, p3=p3, p4=p4)


@admin.route('/admin_info', methods=['GET'])
def admin_info():
    Ano = session.get('no')
    current_admin = Admin.query.filter_by(Ano=Ano)
    return render_template('adm-profile.html', current_admin=current_admin[0])


@admin.route('/manage_course', methods=['GET', 'POST'])
def manage_course():
    courses = Course.query.all()
    return render_template('class-list.html', courses=courses)


@admin.route('/print_courses', methods=['GET'])
def print_courses():
    courses = Course.query.all()
    response = create_courses_flie(courses)
    response.headers['Content-Type'] = 'utf=8'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Content-Disposition'] = 'attachment;filename=courses.xlsx'
    return response


@admin.route('/manage_students', methods=['GET'])
def manage_students():
    students = Student.query.all()
    for i in range(len(students) - 1):
        if students[i].Sname == '匿名':
            del students[i]
    return render_template('student-list.html', students=students)


@admin.route('/manage_teachers', methods=['GET'])
def manage_teachers():
    teachers = Teacher.query.all()
    return render_template('teacher-list.html', teachers=teachers)


@admin.route('/manage_admins', methods=['GET'])
def manage_admins():
    admins = Admin.query.all()
    return render_template('adm-list.html', admins=admins)
