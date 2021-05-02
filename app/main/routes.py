from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import current_app, db
from app.main.forms import EditProfileForm, PostForm, newsPostForm, delnewsPostForm
from app.models import User, Post, newsPost, base_navigation, move_news_navigation, one_article_navigation\
           ,apple_daily_navigation ,movenewsPost, onearticlePost
from app.main import bp
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())




@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    base_configuration = base_navigation.query.all()
    apnews = newsPost.query.order_by(newsPost.timestamp.desc()).limit(5)
    mvnews = movenewsPost.query.order_by(movenewsPost.timestamp.desc()).limit(5)
    oanews = onearticlePost.query.order_by(onearticlePost.timestamp.desc()).limit(5)
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Home'), form=form, apnews=apnews,mvnews=mvnews,oanews=oanews,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url,base_configuration=base_configuration)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/addposts', methods=['GET', 'POST'])
@login_required
def addposts():
    newsform = newsPostForm()
    delform = delnewsPostForm()
    if newsform.validate_on_submit():
        f = newsform.fileName.data
        filename = secure_filename(f.filename)
        print(filename)
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        print(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        post = newsPost(body=newsform.newscontent.data, posttitle=newsform.post_title.data, cover_name=filename, author=current_user )
        db.session.add(post)
        db.session.commit()
        flash(_('Your apple daily post is now live!'))
        return redirect(url_for('main.apple_daily'))
    if delform.validate_on_submit():
        id = delform.postid.data
        print(newsPost.query.filter_by(id=id).first())
        delpost = newsPost.query.filter_by(id=id).first()
        if delpost is None:
            flash(_('Post id ' + str(id) + ' of apple daily is not exist'))
        else:
            db.session.delete(delpost)
            db.session.commit()
            flash(_('Post id ' + str(id) + 'of apple daily has been deleted'))
    return render_template('addposts.html', title=_('addnewspost'), form=newsform, delform=delform)


@bp.route('/add_move_news_posts', methods=['GET', 'POST'])
@login_required
def add_move_news_posts():
    newsform = newsPostForm()
    delform = delnewsPostForm()
    if newsform.validate_on_submit():
        f = newsform.fileName.data
        filename = secure_filename(f.filename)
        print(filename)
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        print(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        mvpost = movenewsPost(body=newsform.newscontent.data, posttitle=newsform.post_title.data, cover_name=filename, author=current_user)
        db.session.add(mvpost)
        db.session.commit()
        flash(_('Your move news post is now live!'))
        return redirect(url_for('main.move_news'))
    if delform.validate_on_submit():
        id = delform.postid.data
        delpost = movenewsPost.query.filter_by(id=id).first()
        if delpost is None:
            flash(_('Post id ' + str(id) + ' of move news is not exist'))
        else:
            db.session.delete(delpost)
            db.session.commit()
            flash(_('Post id ' + str(id) + ' of move news has been deleted'))
    return render_template('add_move_news_posts.html', title=_('addmovenewspost'), form=newsform, delform=delform)


@bp.route('/add_one_article_posts', methods=['GET', 'POST'])
@login_required
def add_one_article_posts():
    newsform = newsPostForm()
    delform = delnewsPostForm()
    if newsform.validate_on_submit():
        f = newsform.fileName.data
        filename = secure_filename(f.filename)
        print(filename)
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        print(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        oapost = onearticlePost(body=newsform.newscontent.data, posttitle=newsform.post_title.data, cover_name=filename, author=current_user)
        db.session.add(oapost)
        db.session.commit()
        flash(_('Your one article post is now live!'))
        return redirect(url_for('main.one_article'))
    if delform.validate_on_submit():
        id = delform.postid.data
        delpost = onearticlePost.query.filter_by(id=id).first()
        if delpost is None:
            flash(_('Post id ' + str(id) + '  of one article is not exist'))
        else:
            db.session.delete(delpost)
            db.session.commit()
            flash(_('Post id ' + str(id) + ' of one article has been deleted'))
    return render_template('add_one_article_posts.html', title=_('addmovenewspost'), form=newsform, delform=delform)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('explore.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/base.html', methods=['GET', 'POST'])
def base():
    base_configuration = base_navigation
    print(base_configuration)
    return render_template('base.html', base_configuration=base_configuration)


#@bp.route('/_page.html', methods=['GET', 'POST'])
#def base():
    #pages = base_navigation
    #return render_template('base.html', pages=pages)

@bp.route('/apple_daily')
def apple_daily():
    apple_daily_menu = apple_daily_navigation.query.all()
    news = newsPost.query.order_by(newsPost.timestamp.desc())
    for i in news:
        print(i)
    return render_template('apple_daily.html',apple_daily_menu=apple_daily_menu,news=news)


@bp.route('/apple_daily/<string:posttitle>', methods=['GET'])
def apple_daily_route(posttitle):
    new = newsPost.query.filter_by(posttitle=posttitle).first()
    image_url = os.path.join(current_app.config['UPLOAD_FOLDER'],new.cover_name)
    print(image_url)
    return render_template('apple_daily_post.html', new=new, image_url=image_url)

@bp.route('/move_news')
def move_news():
    move_news_menu = move_news_navigation.query.all()
    news = movenewsPost.query.order_by(movenewsPost.timestamp.desc())
    return render_template('move_news.html', move_news_menu=move_news_menu, news=news)

@bp.route('/move_news/<string:posttitle>', methods=['GET'])
def move_news_route(posttitle):
    mvnew = movenewsPost.query.filter_by(posttitle=posttitle).first()
    image_url = os.path.join(current_app.config['UPLOAD_FOLDER'],mvnew.cover_name)
    print(image_url)
    return render_template('move_news_post.html', new=mvnew, image_url=image_url)


@bp.route('/about_us')
def about_us():
    return render_template('about_us.html')


@bp.route('/one_article')
def one_article():
    one_article_menu = one_article_navigation.query.all()
    news = onearticlePost.query.order_by(onearticlePost.timestamp.desc())
    return render_template('one_article.html', one_article_menu=one_article_menu, news=news)

@bp.route('/one_article/<string:posttitle>', methods=['GET'])
def one_article_route(posttitle):
    oanew = onearticlePost.query.filter_by(posttitle=posttitle).first()
    image_url = os.path.join(current_app.config['UPLOAD_FOLDER'],oanew.cover_name)
    print(image_url)
    return render_template('one_article_post.html', new=oanew, image_url=image_url)


@bp.route('/apple_foundation')
@login_required
def apple_foundation():
    return render_template('apple_foundation.html')


@bp.route('/tomonews')
@login_required
def tomonews():
    return render_template('tomonews.html')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('main.user', username=username))
