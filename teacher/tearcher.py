from flask import render_template, request, flash, make_response, url_for, redirect, Blueprint, session
from io import BytesIO
from sqlalchemy import text
from models import Teacher, Course, Discussion

teacher = Blueprint('teacher', __name__, template_folder='template', static_folder='static')


def get_info():
    Tno = session.get('no')
    current_teacher = Teacher.query.filter_by(Tno=Tno).all()
    if current_teacher:
        courses = current_teacher[0].courses
    else:
        courses = []
    return current_teacher, courses


# @teacher.before_request
# def before_teacher():

@teacher.route("/", methods=['GET', 'POST'])
def teacher_main():
    current_teacher, courses = get_info()
    return render_template('teacherMain.html', teacher=current_teacher[0], courses=courses)


@teacher.route("/my_courses", methods=['GET', 'POST'])
def my_courses():
    current_teacher, courses = get_info()
    return render_template('teacherMyCourses.html', teacher=current_teacher[0], courses=courses)


@teacher.route("/teacher_course", methods=['GET', 'POST'])
def teacher_course():
    current_teacher, courses = get_info()
    Cno = request.args.get('Cno')
    current_course = Course.query.filter_by(Cno=Cno).all()
    return render_template('courseIntroduction.html', teacher=current_teacher[0], course=current_course[0])


@teacher.route("/new_course", methods=['GET', 'POST'])
def new_course():
    current_teacher, courses = get_info()
    return render_template('teacherNewCourse.html', teacher=current_teacher[0], courses=courses)


@teacher.route("/change_pwd", methods=['GET', 'POST'])
def change_pwd():
    current_teacher, courses = get_info()
    return render_template('changePwd.html', teacher=current_teacher[0], courses=courses)


@teacher.route("/my_info", methods=['GET', 'POST'])
def my_info():
    current_teacher, courses = get_info()
    return render_template('teacherMessage.html', teacher=current_teacher[0], courses=courses)


@teacher.route("/my_files", methods=['GET', 'POST'])
def my_files():
    current_teacher, courses = get_info()
    return render_template('teacherFile.html', teacher=current_teacher[0], courses=courses)


@teacher.route("/manage_courseware", methods=['GET', 'POST'])
def manage_courseware():
    current_teacher, courses = get_info()
    Cno = request.args.get('Cno')
    current_course = Course.query.filter_by(Cno=Cno).all()
    return render_template('courseFile.html', teacher=current_teacher[0], course=current_course[0])


@teacher.route("/release_homework", methods=['GET', 'POST'])
def release_homework():
    current_teacher, courses = get_info()
    Cno = request.args.get('Cno')
    current_course = Course.query.filter_by(Cno=Cno).all()
    return render_template('courseCreateHomework.html', teacher=current_teacher[0], course=current_course[0])


@teacher.route("/correct_homework", methods=['GET', 'POST'])
def correct_homework():
    current_teacher, courses = get_info()
    Cno = request.args.get('Cno')
    current_course = Course.query.filter_by(Cno=Cno).all()
    return render_template('courseCorrectHomework.html', teacher=current_teacher[0], course=current_course[0])


@teacher.route("/manage_students", methods=['GET', 'POST'])
def manage_students():
    current_teacher, courses = get_info()
    Cno = request.args.get('Cno')
    current_course = Course.query.filter_by(Cno=Cno).all()
    return render_template('courseStudents.html', teacher=current_teacher[0], course=current_course[0])


@teacher.route("/discussion", methods=['GET', 'POST'])
def discussion():
    current_teacher, courses = get_info()
    Cno = request.args.get('Cno')
    current_course = Course.query.filter_by(Cno=Cno).all()
    discussions = current_course[0].discussions
    print(discussions)
    return render_template('discussion.html', teacher=current_teacher[0], course=current_course[0], posts=discussions)


@teacher.route("/discussion_info", methods=['GET', 'POST'])
def discussion_info():
    current_teacher, courses = get_info()
    Cno = request.args.get('Cno')
    post_id = request.args.get('post_id')
    temp1 = Discussion.query.filter_by(Discuss_no=post_id)
    current_post = temp1[0]
    current_course = Course.query.filter_by(Cno=Cno)
    reply_posts = Discussion.query.filter_by(reply_which=post_id).order_by('Discuss_date')
    length = 0
    for item in reply_posts:
        length += 1
    return render_template('discussion_info.html', teacher=current_teacher[0], course=current_course[0],
                           replys=reply_posts, current_post=current_post, total_amount=length)
