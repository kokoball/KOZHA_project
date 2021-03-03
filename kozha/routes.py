import secrets
import os
from PIL import Image
from flask import render_template, url_for, request, redirect, flash, abort
from kozha import app, db, bcrypt, mail
from kozha.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from kozha.models import User, Post, Hashtag, tags
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message

@app.route("/")

@app.route("/index", methods=['GET','POST'])
def home():
    posts = Post.query.all()
    posts = reversed(posts)
    # image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('index.html', tite='Home', posts=posts)

@app.route("/daily", methods=['GET','POST'])
def daily():
    if current_user.is_authenticated:
        posts = Post.query.filter_by(style=current_user.style).all()
        posts = reversed(posts)
    else:
        posts=Post.query.all()
        posts=reversed(posts)
    # image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('daily.html', title='Daily', posts=posts)

@app.route("/brand", methods=['GET'])
def brand():
    return render_template('brand.html')

@app.route("/search", methods=['GET'])
def search():
    q = request.args.get('q')
    if q:
        posts = Post.query.filter(Post.title.contains(q))
    else:
        posts = Post.query.all()
        posts= reversed(posts)
    return render_template('search.html', posts=posts)

@app.route("/qun", methods=['GET'])
def qna():
    return render_template('qna.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:   # current_user 객체의 is_authenticated 메소드는 db에 저장되어 있는 사용자의 정보를 반환했는지(인증,true) 안했는지(false)를 나타내준다.
        return redirect(url_for('home')) # 로그인이 되어있을 경우는 'index.html'로 이동
    form = RegistrationForm() # form 변수에 forms.py의 RegistrationForm() 객체를 저장
    if form.validate_on_submit(): # 양식이 다 채워진채로 서버에 post메세지가 발송되고 true를 반환받았으면
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # 입력한 패스워드를 해쉬화
        user = User(username = form.username.data, email = form.email.data, password= hashed_password, style= form.style.data) # 입력받은 모든 패스워드를 user변수에 저장
        db.session.add(user) # 데이터베이스 User테이블에 입력받은 새로운 user를 추가
        db.session.commit() # 데이터베이스 저장
        flash('계정 생성이 완료되었습니다!', 'success') # 계정이 성공적으로 등록되었다는 문구 출력
        return redirect(url_for('login'))   # 계정생성이 완료되면 로그인페이지로 이동
    return render_template('register.html', title='Register', form=form) # register.html 템플릿을 띄우고 타이틀은 'Register' 해당 템플릿에서 쓰이는 form은 위에서 forms.py에서 불러와 form에 저장해준 RegistrationFrom() 객체을 사용



@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): # 해쉬하된 암호와 유저가 입력한 암호가 같은지 확인 (by boolean)
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            flash('로그인 되었습니다!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
    
        else:
            flash('잘못된 정보입니다. 이메일과 패스워드를 확인해주세요', 'danger')
    return render_template('login.html', title='Login', form = form)
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size=(125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.profile = form.user_profile.data
        db.session.commit()
        flash('변경사항이 저장되었습니다.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.user_profile.data = current_user.profile
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

def save_update_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/update_pics', picture_fn)
    
    output_size=(350,350)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # post = Post(title=form.title.data, content=form.content.data, author=current_user)
        # db.session.add(post)
        if form.picture.data:
            picture_file = save_update_picture(form.picture.data)
            post = Post(title=form.title.data, content=form.content.data, content_img=picture_file, author=current_user, style=current_user.style)
            tag1 = Hashtag(tagname=form.tag1.data)
            tag2 = Hashtag(tagname=form.tag2.data)
            tag3 = Hashtag(tagname=form.tag3.data)
            tag4 = Hashtag(tagname=form.tag4.data)
            db.session.add(post)
            db.session.add(tag1)
            db.session.add(tag2)
            db.session.add(tag3)
            db.session.add(tag4)
            db.session.commit()
            post = Post.query.order_by(Post.id.desc()).first()
            tag1.tagging.append(post)
            tag2.tagging.append(post)
            tag3.tagging.append(post)
            tag4.tagging.append(post)
            db.session.commit()
            flash('게시물이 등록되었습니다!', 'success')
            return redirect(url_for('home'))
        else:
            post = Post(title=form.title.data, content=form.content.data, author=current_user, style=current_user.style )
            tag1 = Hashtag(tagname=form.tag1.data)
            tag2 = Hashtag(tagname=form.tag2.data)
            tag3 = Hashtag(tagname=form.tag3.data)
            tag4 = Hashtag(tagname=form.tag4.data)
            db.session.add(post)
            db.session.add(tag1)
            db.session.add(tag2)
            db.session.add(tag3)
            db.session.add(tag4)
            db.session.commit()
            post = Post.query.order_by(Post.id.desc()).first()
            tag1.tagging.append(post)
            tag2.tagging.append(post)
            tag3.tagging.append(post)
            tag4.tagging.append(post)
            db.session.commit()
            flash('게시물이 등록되었습니다!', 'success')
            return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='피드 등록(New Feed)')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) # 존재하지않으면 404에러 반환
    return render_template('post.html',title='post.title', post=post)

@app.route("/post/<int:post_id>/update" , methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) # 다른 유저가 생성한 게시물을 업데이트하려고 할 시 경고메시지 반환
    form=PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_update_picture(form.picture.data)
            post.content_img = picture_file
        post.title = form.title.data
        post.content = form.content.data
        post.tags[0].tagname = form.tag1.data
        post.tags[1].tagname = form.tag2.data
        post.tags[2].tagname = form.tag3.data
        post.tags[3].tagname = form.tag4.data
        # post.tags = [form.tag1.data, form.tag2.data, form.tag3.data, form.tag4.data]
        db.session.commit()
        flash('게시물이 수정되었습니다!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method =='GET':
        form.title.data = post.title
        form.content.data = post.content
        form.tag1.data = post.tags[0].tagname
        form.tag2.data = post.tags[1].tagname
        form.tag3.data = post.tags[2].tagname
        form.tag4.data = post.tags[3].tagname     
    image_file = url_for('static', filename='update_pics/'+post.content_img)
    return render_template('create_post.html', title='New Post', form=form, image_file=image_file, legend='피드 수정(Edit Feed)')

@app.route("/post/<int:post_id>/delete" , methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) # 다른 유저가 생성한 게시물을 업데이트하려고 할 시 경고메시지 반환
    db.session.delete(post)
    db.session.commit()
    flash('게시글이 삭제되었습니다', 'success')
    return redirect(url_for('home'))

@app.route("/my", methods=['GET', 'POST'])
@login_required
def my():
    posts = Post.query.all()
    posts = reversed(posts)
    my_posts = reversed(current_user.posts)
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('my.html', tite='My', posts=posts, my_posts = my_posts, image_file=image_file)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simpoly ignore this email and no change will be made.
'''
    mail.send(msg)
    
@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('비밀번호 변경을 위한 이메일이 전송되었습니다.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('존재하지 않거나 유효하지 않은 토큰입니다.', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit(): # 양식이 다 채워진채로 서버에 post메세지가 발송되고 true를 반환받았으면
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # 입력한 패스워드를 해쉬화
        user.password=hashed_password
        db.session.commit() # 데이터베이스 저장
        flash('비밀번호가 변경되었습니다!', 'success') # 계정이 성공적으로 등록되었다는 문구 출력
        return redirect(url_for('login')) 
    return render_template('reset_token.html', title='Reset Password', form=form)

@app.route("/like_worldcup")
def like_worldcup():
    return render_template('like_style.html')

@app.route("/style_basic")
def style_basic():
    return render_template('style_basic.html')

@app.route("/style_casual")
def style_casual():
    return render_template('style_casual.html')

@app.route("/style_lovely")
def style_lovely():
    return render_template('style_lovely.html')

@app.route("/style_modernchic")
def style_modernchic():
    return render_template('style_modernchic.html')

@app.route("/style_sexy")
def style_sexy():
    return render_template('style_sexy.html')

@app.route("/style_unique")
def style_unique():
    return render_template('style_unique.html')