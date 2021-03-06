from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    TextAreaField, IntegerField, FileField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User
from flask_wtf.file import FileRequired



class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class newsPostForm(FlaskForm):
    post_title = TextAreaField(_l('Post name'), validators=[DataRequired()])
    newscontent = TextAreaField(_l('Post content'), validators=[DataRequired()])
    fileName = FileField(_l('Cover image'), validators=[FileRequired()])
    submit = SubmitField(_l('Submit'))

class delnewsPostForm(FlaskForm):
    postid = IntegerField(_l('Delete Post id'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

