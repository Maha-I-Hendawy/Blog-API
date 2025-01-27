from flask import Flask, request, jsonify  
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import json




app = Flask(__name__)
app.config['SECRET_KEY'] = '3532ea0bf5f21ad3ad26d2c21d04'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_DATABASE_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

app.app_context().push()


# Database Models

# User Model

class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), nullable=False, unique=True)
	email = db.Column(db.String(100), nullable=False, unique=True)
	password = db.Column(db.String(100), nullable=False)
	date_joined = db.Column(db.Date, default=datetime.utcnow)
	posts = db.relationship('Post', backref='user', lazy=True)
	comments = db.relationship('Comment', backref='user')

	def __repr__(self):
		return f"'user_id': {self.user_id}, 'username': {self.username}, 'email': {self.email}, 'password': {self.password}, 'date_joined': {self.date_joined}, 'posts': {self.posts}, 'comments': {self.comments}"



# Post Model

class Post(db.Model):
	post_id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200))
	content = db.Column(db.Text)
	date_created = db.Column(db.Date, default=datetime.utcnow)
	userid = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	comments = db.relationship('Comment', backref='post', lazy=True)


	def __str__(self):
		return f"{self.title}"


# Comment Model

class Comment(db.Model):
	comment_id = db.Column(db.Integer, primary_key=True)
	comment = db.Column(db.Text)
	userid = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	postid = db.Column(db.Integer, db.ForeignKey('post.post_id'))


	def __str__(self):
		return f"{self.comment}"




# Users API

# Get all Users API


@app.route('/api/users')
def get_users():
	users = User.query.all()
	for user in users:
		return json.dumps(user)
	return "hello"




# Get one user API

@app.route('/api/users/user/<int:user_id>')
def get_user(user_id):
	user = User.query.filter_by(user_id=user_id).first()
	user1 = {'id': user.user_id, 'username': user.username, 'email': user.email, 'password': user.password, 'date_joined': user.date_joined}
	return jsonify({'user': user1})



# Add one user API

@app.route('/api/users', methods=['POST'])
def add_user():
	if request.method == 'POST':
		data = request.get_json()
		user = User(username=data['username'], email=data['email'], password=data['password'])
		db.session.add(user)
		db.session.commit()
		return "good"
	else:
		return 'add somethings'



		

# Update one user API

@app.route('/api/users/user/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
	user = User.query.filter_by(user_id=user_id).first()
	if request.method == 'PUT':
		data = request.get_json()
		user.username = data['username']
		user.email = data['email']
		user.password = data['password']
		db.session.commit()
		return "good"
	else:
		return "update something"


# Delete one user API

@app.route('/api/users/user/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
	if request.method == 'DELETE':
		users = User.query.all()
		for user in users:
			if user.user_id == user_id:
				db.session.delete(user)
				db.session.commit()
				return "good"
			else:
				return "no user found"
	else:
		return 'delete something'





# Posts API
		

# Get all Posts

@app.route('/api/posts')
def get_posts():
	posts = Post.query.all()
	return posts


# Get one post 

@app.route('/api/posts/post/<int:post_id>')
def get_post(post_id):
	post = Post.query.filter_by(post_id=post_id).first()
	postie = {'post_id': post.post_id, 'title': post.title, 'content': post.content, 'date_created': post.date_created, 'userid': post.userid, 'comments': post.comments}
	return jsonify({'post': postie})


# Add One Post

@app.route('/api/posts', methods=['POST'])
def add_post():
	if request.method == 'POST':
		data = request.get_json()
		post = Post(title=data['title'], content=data['content'], userid=data['userid'])
		db.session.add(post)
		db.session.commit()
		return "good"
	else:
		return "add post"


# Update One Post

@app.route('/api/posts/post/update/<int:post_id>', methods=['PUT'])
def update_post(post_id):
	post = Post.query.filter_by(post_id=post_id).first()
	if request.method == 'PUT':
		data = request.get_json()
		post.title = data['title']
		post.content = data['content']
		db.session.commit()
		return "good"
		
	else:
		return "update post"



# Delete One Post

@app.route('/api/posts/post/delete/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
	#post = Post.query.filter_by(post_id=post_id).first()
	if request.method == 'DELETE':
		posts = Post.query.all()
		for post in posts:
			if post.post_id == post_id:
				db.session.delete(post)
				db.session.commit()
				return "good"
			else:
				return "no post found"
		
	else:
		return "delete post"






# Comment API 

# Get all comments API

@app.route('/api/comments')
def get_comments():
	comments = Comment.query.all()
	return jsonify({'comments': comments})


# Get one comment API


@app.route('/api/comments/comment/<int:comment_id>')
def get_comment(comment_id):
	comment = Comment.query.filter_by(comment_id=comment_id).first()
	comment1 = {"comment_id": comment.comment_id, "comment": comment.comment, "userid": comment.userid, "postid": comment.postid}
	return jsonify({"comment": comment1})



# Add one comment API 

@app.route('/api/comments', methods=['POST'])
def add_comment():
	if request.method == 'POST':
		data = request.get_json()
		comment = Comment(comment=data['comment'], userid=data['userid'], postid=data['postid'])
		db.session.add(comment)
		db.session.commit()
		return "good"
	else:
		return "add something"


# Update one comment API

@app.route('/api/comments/comment/update/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
	comment = Comment.query.filter_by(comment_id=comment_id).first()
	if request.method == 'PUT':
		data = request.get_json()
		comment.comment = data['comment']
		db.session.commit()
		return "good"
	else:
		return comment.comment



# Delete one comment API

@app.route('/api/comments/comment/delete/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
	#comment = Comment.query.filter_by(comment_id=comment_id).first()
	if request.method == 'DELETE':
		comments = Comment.query.all()
		for comment in comments:
			if comment.comment_id == comment_id:
				db.session.delete(comment)
				db.session.commit()
				return "good"
			else:
				return "comment not found"
	else:
		return "delete something"