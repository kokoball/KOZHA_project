from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from kozha.models import User


class RegistrationForm(FlaskForm):
    username = StringField('성명(name)', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('비밀번호(Password)', validators=[DataRequired()])
    confirm_password=PasswordField('비밀번호확인(Confirm Password)', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('다음')
    # 주소는 필수로 추가해야함
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(username.data+'님은 이미 등록되어 있습니다.')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(email.data+'은 이미 등록되어있는 이메일입니다.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me') # 로그인 정보 쿠키에 저장
    submit = SubmitField('로그인')


class UpdateAccountForm(FlaskForm):
    username = StringField('성명(name)', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    user_profile = TextAreaField('내 소개', validators=[DataRequired()])
    picture = FileField('이미지 등록', validators=[FileAllowed(['png','jpg'])])
    submit = SubmitField('Update')
    # 주소는 필수로 추가해야함
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(username.data+'님은 이미 등록되어 있습니다.')
            
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(email.data+'은 이미 등록되어있는 이메일입니다.')

class PostForm(FlaskForm):
    title = StringField('스타일명', validators=[DataRequired()])
    content = TextAreaField('내용', validators=[DataRequired()])
    tag1 = StringField('태그', validators=[DataRequired()])
    tag2 = StringField('태그', validators=[DataRequired()])
    tag3 = StringField('태그', validators=[DataRequired()])
    tag4 = StringField('태그', validators=[DataRequired()])
    picture = FileField('이미지 등록', validators=[FileAllowed(['png','jpg'])])
    submit = SubmitField('업로드')

    a = ['~','!','@','#','$','%','^','&','*','(',')','_','+','₩','-','=','[',']','<\>','{','}','|',';',':',',','.','/','<','>','?']
    
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('비밀번호 재설정')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(email.data+'은 존재하지 않는 계징입니다. 회원가입 해주시기 바랍니다')   
  

class ResetPasswordForm(FlaskForm):
    password = PasswordField('비밀번호(Password)', validators=[DataRequired()])
    confirm_password=PasswordField('비밀번호확인(Confirm Password)', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('비밀번호 재설정')    
    # def validate_tag1(self, tag1):
    #     for i in range(len(list(tag1.data))):
    #         if list(tag1.data)[i] in a:
    #             raise ValidationError('태그에 특수문자가 포함되어 있습니다.')
    # def validate_tag2(self, tag2):    
    #     for i in range(len(list(tag2.data))):
    #         if list(tag2.data)[i] in a:
    #             raise ValidationError('태그에 특수문자가 포함되어 있습니다.')
    # def validate_tag3(self, tag3):    
    #     for i in range(len(list(tag3.data))):
    #         if list(tag3.data)[i] in a:
    #             raise ValidationError('태그에 특수문자가 포함되어 있습니다.')
    # def validate_tag4(self, tag4):    
    #     for i in range(len(list(tag4.data))):
    #         if list(tag4.data)[i] in a:
    #             raise ValidationError('태그에 특수문자가 포함되어 있습니다.')