from flask import render_template, request, flash, make_response, url_for, redirect, Blueprint, session
from models import Assistant, Course, Discussion

assistant = Blueprint('assistant', __name__, template_folder='template', static_folder='static')


def get_info():
    Asno = session.get('no')
    current_assistant = Assistant.query.filter_by(Asno=Asno).all()
    if current_assistant:
        courses = current_assistant[0].courses
    else:
        courses = []
    return current_assistant, courses


@assistant.route("/", methods=['GET', 'POST'])
def assistant_main():
    current_assistant, courses = get_info()
    return render_template('assistantMain.html', assistant=current_assistant[0], courses=courses)


@assistant.route("/my_courses", methods=['GET', 'POST'])
def my_courses():
    current_assistant, courses = get_info()
    return render_template('assistantMyCourses.html', assistant=current_assistant[0], courses=courses)


@assistant.route("/assistant_course", methods=['GET', 'POST'])
def assistant_course():
    current_assistant, courses = get_info()
    Cno = request.args.get('Cno')
    current_course = Course.query.filter_by(Cno=Cno).all()
    return render_template('assistantcourseIntroduction.html', assistant=current_assistant[0], course=current_course[0])


@assistant.route("/change_pwd", methods=['GET', 'POST'])
def change_pwd():
    current_assistant, courses = get_info()
    return render_template('assistantchangePwd.html', assistant=current_assistant[0], courses=courses)


@assistant.route("/my_info", methods=['GET', 'POST'])
def my_info():
    current_assistant, courses = get_info()
    return render_template('assistantMessage.html', assistant=current_assistant[0], courses=courses)


@assistant.route("/my_files", methods=['GET', 'POST'])
def my_files():
    current_assistant, courses = get_info()
    return render_template('assistantFile.html', assistant=current_assistant[0], courses=courses)


@assistant.route("/manage_courseware", methods=['GET', 'POST'])
def manage_courseware():
    current_assistant, courses = get_info()
    Cno = request.args.get('Cno')
    current_course = Course.query.filter_by(Cno=Cno).all()
    return render_template('assistantcourseFile.html', assistant=current_assistant[0], course=current_course[0])


@assistant.route("/release_homework", methods=['GET', 'POST'])
def release_homework():
    current_assistant, courses = get_info()
    Cno = request.args.get('Cno')
    current_course = Course.query.filter_by(Cno=Cno).all()
    return render_template('assistantcourseCreateHomework.html', assistant=current_assistant[0], course=current_course[0])


@assistant.route("/correct_homework", methods=['GET', 'POST'])
def correct_homework():
    current_assistant, courses = get_info()
    Cno = request.args.get('Cno')
    current_course = Course.query.filter_by(Cno=Cno).all()
    return render_template('assistantcourseCorrectHomework.html', assistant=current_assistant[0], course=current_course[0])


@assistant.route("/manage_students", methods=['GET', 'POST'])
def manage_students():
    current_assistant, courses = get_info()
    Cno = request.args.get('Cno')
    current_course = Course.query.filter_by(Cno=Cno).all()
    return render_template('assistantcourseStudents.html', assistant=current_assistant[0], course=current_course[0])


@assistant.route("/discussion", methods=['GET', 'POST'])
def discussion():
    current_assistant, courses = get_info()
    Cno = request.args.get('Cno')
    current_course = Course.query.filter_by(Cno=Cno).all()
    discussions = current_course[0].discussions
    print(discussions)
    return render_template('assistantdiscussion.html', assistant=current_assistant[0], course=current_course[0], posts=discussions)


@assistant.route("/discussion_info", methods=['GET', 'POST'])
def discussion_info():
    current_assistant, courses = get_info()
    Cno = request.args.get('Cno')
    post_id = request.args.get('post_id')
    temp1 = Discussion.query.filter_by(Discuss_no=post_id)
    current_post = temp1[0]
    current_course = Course.query.filter_by(Cno=Cno)
    reply_posts = Discussion.query.filter_by(reply_which=post_id).order_by('Discuss_date')
    length = 0
    for item in reply_posts:
        length += 1
    return render_template('assistantdiscussion_info.html', assistant=current_assistant[0], course=current_course[0],
                           replys=reply_posts, current_post=current_post, total_amount=length)
