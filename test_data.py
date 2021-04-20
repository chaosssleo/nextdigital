from app import create_app, db, cli
from app.models import User, Post, newsPost, base_navigation

app = create_app()
app.app_context().push()

def add_user():
    with app.app_context():
        j = User(username='john1', email='john1@example.com')
        s = User(username='susan2', email='susan2@example.com')
        db.session.add(j)
        db.session.add(s)
        db.session.commit()

#add_user()

users = User.query.all()
for u in users:
    print(u.id, u.username)

u = User.query.get(1)
print(u)

def add_post():
    with app.app_context():
        p = Post(body='my first post!', author=u)
        db.session.add(p)
        db.session.commit()

#add_post()

# get all posts written by a user
posts = u.posts.all()
print(posts)
# same, but with a user that has no posts
u = User.query.get(2)
posts = u.posts.all()
print(posts)
# print post author and body for all posts
posts = Post.query.all()
for p in posts:
    print(p.id, p.author.username, p.body)

# get all users in reverse alphabetical order
User.query.order_by(User.username.desc()).all()

def add_page():
    with app.app_context():
        a = base_navigation(page_name='Home', page_link='main.index')
        b = base_navigation(page_name='Explore', page_link='main.explore')
        c = base_navigation(page_name='Apple Daily', page_link='main.apple_daily')
        d = base_navigation(page_name='動新聞', page_link='main.move_news')
        e = base_navigation(page_name='關於我們', page_link='main.about_us')
        f = base_navigation(page_name='addposts', page_link='main.addposts')
        db.session.add(a)
        db.session.add(b)
        db.session.add(c)
        db.session.add(d)
        db.session.add(e)
        db.session.add(f)
        db.session.commit()

add_page()