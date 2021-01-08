from flask import render_template, request, flash, url_for, redirect, Blueprint, session
from models import Student, Teacher, Admin, Assistant
from models import db

index = Blueprint('index', __name__, template_folder='template', static_url_path='static')


@index.route('/', methods=['GET'])
def all_index():
    no = session.get('no')
    if no is not None:
        if session.get('identity') == 'student':
            students = Student.query.filter_by(Sno=no).all()
            return render_template('index.html', student=students[0])
        if session.get('identity') == 'teacher':
            teachers = Teacher.query.filter_by(Tno=no).all()
            return render_template('index.html', teacher=teachers[0])
    return render_template('index.html')


@index.route('/courses', methods=['GET'])
def courses():
    no = session.get('no')
    if no is not None:
        if session.get('identity') == 'student':
            students = Student.query.filter_by(Sno=no).all()
            return render_template('course.html', student=students[0])
        if session.get('identity') == 'teacher':
            teachers = Teacher.query.filter_by(Tno=no).all()
            return render_template('course.html', teacher=teachers[0])
    return render_template('course.html')


@index.route('/teachers', methods=['GET'])
def teachers():
    no = session.get('no')
    if no is not None:
        if session.get('identity') == 'student':
            students = Student.query.filter_by(Sno=no).all()
            return render_template('teacher.html', student=students[0])
        if session.get('identity') == 'teacher':
            teachers = Teacher.query.filter_by(Tno=no).all()
            return render_template('teacher.html', teacher=teachers[0])
    return render_template('teacher.html')


@index.route('/help', methods=['GET'])
def help():
    no = session.get('no')
    if no is not None:
        if session.get('identity') == 'student':
            students = Student.query.filter_by(Sno=no).all()
            return render_template('help.html', student=students[0])
        if session.get('identity') == 'teacher':
            teachers = Teacher.query.filter_by(Tno=no).all()
            return render_template('help.html', teacher=teachers[0])
    return render_template('help.html')


@index.route('/contact', methods=['GET'])
def contact():
    no = session.get('no')
    if no is not None:
        if session.get('identity') == 'student':
            students = Student.query.filter_by(Sno=no).all()
            return render_template('contact.html', student=students[0])
        if session.get('identity') == 'teacher':
            teachers = Teacher.query.filter_by(Tno=no).all()
            return render_template('contact.html', teacher=teachers[0])
    return render_template('contact.html')


@index.route("/login", methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        identity = request.form['identityType']
        username = request.form['username']
        pwd = request.form['pwd']
        if identity == "option1":
            student = Student.query.filter_by(Sno=username).all()
            if student:
                if pwd == student[0].Spw:
                    session['identity'] = 'student'
                    session['no'] = student[0].Sno
                    return redirect(url_for('student.index'))
                else:
                    flash("用户名或密码输入错误！", 'warning')
            else:
                flash('您还不是学生，请先注册！', 'warning')
        if identity == "option2":
            teacher = Teacher.query.filter_by(Tno=username).all()
            if teacher:
                if pwd == teacher[0].Tpw:
                    session['identity'] = 'teacher'
                    session['no'] = teacher[0].Tno
                    return redirect(url_for('teacher.teacher_main'))
                else:
                    flash("用户吗或密码输入错误！", 'warning')
            else:
                flash('您还不是教师，请先注册！', 'warning')
        if identity == "option3":
            assistant = Assistant.query.filter_by(Asno=username).all()
            if assistant:
                if pwd == assistant[0].Aspw:
                    session['identity'] = 'assistant'
                    session['no'] = assistant[0].Asno
                    return redirect(url_for('assistant.assistant_main'))
                else:
                    flash("用户名或密码输入错误！", 'warning')
            else:
                flash('您还不是管理员，请先注册！', 'warning')
        if identity == "option4":
            admin = Admin.query.filter_by(Ano=username).all()
            if admin:
                if pwd == admin[0].Apw:
                    session['identity'] = 'admin'
                    session['no'] = admin[0].Ano
                    return redirect(url_for('admin.admin_index'))
                else:
                    flash("用户名或密码输入错误！", 'warning')
            else:
                flash('您还不是管理员，请先注册！', 'warning')
    return render_template('login.html')


@index.route('/forget1', methods=['GET', 'POST'])
def forget1():
    if request.method == 'POST':
        no = request.form.get('userid')
        tel = request.form.get('tel')
        students = Student.query.filter_by(Sno=no).all()
        if students:
            if tel == students[0].Stel:
                session['change_no'] = no
                return redirect(url_for('index.forget2', no=no))
            else:
                flash('您输入的手机号有误！', 'warning')
        else:
            flash('您输入的学号有误！', 'warning')
    return render_template('forget-1.html')


@index.route('/forget2', methods=['GET', 'POST'])
def forget2():
    if request.method == 'POST':
        no = session.get('change_no')
        new_pwd = request.form.get('newpwd')
        resure_new_pwd = request.form.get('resurepwd')
        students = Student.query.filter_by(Sno=no).all()
        print(students)
        if new_pwd != resure_new_pwd:
            flash('您两次输入的密码不一致！请重新输入', 'warning')
            return redirect(url_for('index.forget2', no=no))
        else:
            if len(new_pwd) < 8 or len(resure_new_pwd) > 16:
                flash('密码长度应为8-16， 请重新输入！', 'warning')
            else:
                students[0].Spw = new_pwd
                db.session.commit()
                flash('密码修改成功！', 'success')
                return render_template('login.html')
    return render_template('forget-2.html')


@index.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('userid')
        true_name= request.form.get('name')
        phone_number = request.form.get('usertel')
        pwd = request.form.get('inputpassword')
        students = Student.query.filter_by(Sno=name).all()
        if len(students) != 0:
            flash('该学号已注册！', 'warning')
        else:
            if len(pwd) < 8 or len(pwd) >16:
                flash('密码长度应为8-16字符，请重新输入！', 'warning')
            else:
                new_student = Student(Sno=name, Stel=phone_number, Spw=pwd, Sname=true_name)
                db.session.add(new_student)
                db.session.commit()
                flash('创建成功！', 'success')
                return render_template('login.html')
    return render_template('signup.html')

