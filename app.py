# flask imports
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid # for public id
from werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps

# creates Flask object
app = Flask(__name__)

app.config['SECRET_KEY'] = 'ReunionAssignment'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# Database ORMs
class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key = True)
	public_id = db.Column(db.String(50), unique = True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(70), unique = True)
	password = db.Column(db.String(80))

	def __init__(self,uid,public_id,name,email,password):
		self.uid = uid
		self.public_id = public_id
		self.name = name
		self.email = email
		self.password = password

	def __repr__(self):
		return f'{self.uid}  {self.email}  {self.name}'


class Followers(db.Model):
	__tablename__ = 'followers'
	fid =  db.Column(db.Integer, primary_key = True)
	fid1 = db.Column(db.Integer)
	fid2 = db.Column(db.Integer , db.ForeignKey("users.uid"))

	def __init__(self,fid1,fid2):
		self.fid1 = fid1
		self.fid2 = fid2

	def __repr__(self):
		return f'{self.fid1}  {self.fid2}'

class Posts(db.Model):
	__tablename__ = 'posts'

	poid = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50))
	decription = db.Column(db.String(50))
	likes = db.Column(db.Integer)
	Created_at = db.Column(db.DateTime , default = datetime.utcnow())
	uid = db.Column(db.Integer, db.ForeignKey("users.uid"))

	def __init__(self,title,description,uid):
		self.title = title
		self.decription = description
		self.uid = uid

	def __repr__(self):
		return f'{self.title}  {self.description}'

class Likes(db.Model):
	__tablename__ = 'likes'
	lid = db.Column(db.Integer, primary_key=True)
	poid = db.Column(db.Integer, db.ForeignKey("posts.poid"))
	uid = db.Column(db.Integer)

	def __init__(self,poid,uid):
		self.poid = poid
		self.uid = uid



class Comments(db.Model):
	__tablename__ = 'comments'
	coid = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer , db.ForeignKey("users.uid"))
	poid = db.Column(db.Integer)
	comments = db.Column(db.String(100))

	def __init__(self,poid,uid,comments):
		self.poid = poid
		self.uid = uid
		self.comments = comments

	def __repr__(self):
		return f'{self.uid} {self.comments}'



# decorator for verifying the JWT
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		# jwt is passed in the request header
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		# return 401 if token is not passed
		if not token:
			return jsonify({'message' : 'Token is missing !!'}), 401

		try:
			# decoding the payload to fetch the stored details
			data = jwt.decode(token, app.config['SECRET_KEY'])
			current_user = User.query\
				.filter_by(public_id = data['public_id'])\
				.first()
		except:
			return jsonify({
				'message' : 'Token is invalid !!'
			}), 401
		# returns the current logged in users contex to the routes
		return f(current_user, *args, **kwargs)

	return decorated

# User Database Route
# this route sends back list of users
@app.route('/user', methods =['GET'])
@token_required
def get_user(current_user):

	print(current_user.email)
	user = User.query.filter_by(uid=current_user.uid).first()
	followers_count = len(list(Followers.query.filter_by(fid1 = current_user.uid)))
	following_count = len(list(Followers.query.filter_by(fid2 = current_user.uid)))
	output = []

	# appending the user data json
	# to the response list
	output.append({
		'public_id': user.public_id,
		'name' : user.name,
		'email' : user.email,
		'followers' : followers_count,
		'following' : following_count
	})

	return jsonify({'users': output})

@app.route('/follow/<puid>', methods =['POST'])
@token_required
def add_follower(current_user,puid):

	print(puid)
	user = User.query.filter_by(uid=current_user.uid).first()
	output = []

	user = User.query \
		.filter_by(uid=puid) \
		.first()


	if not user:
		# returns 401 if user does not exist
		return make_response(
			'Could not verify ID which needs to be Followed.',
			401,
			{'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
		)

	#v_follow = Followers.query.filter_by(fid2=current_user.uid, fid1=puid).first()
	v_follow = db.session.query(Followers).filter(Followers.fid2==current_user.uid, Followers.fid1==puid).first()

	if v_follow:
		# returns 401 if user does not exist
		return make_response(
			'{} Already Present in Following list . Unable to follow.'.format(user.name),
			401,
			{'WWW-Authenticate': 'Basic realm ="User does exist !!"'}
		)
	v_follow = Followers(puid,current_user.uid)
	db.session.add(v_follow)
	db.session.commit()
	return make_response(
		'Successfully Followed {}'.format(user.name),
		401
	)

@app.route('/unfollow/<puid>', methods =['POST'])
@token_required
def remove_follower(current_user,puid):

	user = User.query.filter_by(uid=current_user.uid).first()
	output = []

	user = User.query \
		.filter_by(uid=puid) \
		.first()

	if not user:
		# returns 401 if user does not exist
		return make_response(
			'Could not verify ID which needs to Unfollowed.',
			401,
			{'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
		)
	v_follow = Followers.query.filter_by(fid2 = current_user.uid , fid1 = puid).first()

	if not v_follow:
		# returns 401 if user does not exist
		return make_response(
			'{} Not Present in Following list . Unable to Unfollow.'.format(user.name),
			401,
			{'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
		)
	db.session.delete(v_follow)
	db.session.commit()
	return make_response(
		'Successfully UnFollowed {}'.format(user.name),
		401
	)

@app.route('/posts', methods =['POST'])
@token_required
def posts(current_user):

	auth = request.form

	if not auth or not auth.get('title') or not auth.get('description'):
		# returns 401 if any email or / and password is missing
		return make_response(
			'No Data Found',
			401,
			{'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
		)

	vpost = Posts(auth.get('title'), auth.get('description'),current_user.uid)
	db.session.add(vpost)
	db.session.commit()
	output = []

	output.append({
		'Post-ID': vpost.poid,
		'title': vpost.title,
		'Description': vpost.decription,
		'Created At (UTC)': vpost.Created_at
	})

	return jsonify({'POST': output})

@app.route('/posts/<ppoid>', methods =['POST'])
@token_required
def del_posts(current_user,ppoid):

	post = Posts.query.filter_by(poid = ppoid).first()

	if not post:
		# returns 401 if user does not exist
		return make_response(
			'Unable to Find POST Which Needs to be deleted',
			401,
			{'WWW-Authenticate': 'Unable to Find POST Which Needs to be deleted !!"'}
		)

	db.session.delete(post)
	db.session.commit()

	return make_response(
		'POST Deleted Successfully',
		201
	)


@app.route('/like/<ppoid>', methods =['POST'])
@token_required
def like(current_user,ppoid):

	post = Posts.query.filter_by(poid = ppoid).first()

	if not post:
		# returns 401 if user does not exist
		return make_response(
			'Unable to Find POST Which Needs to be liked',
			401,
			{'WWW-Authenticate': 'Basic realm ="Unable to Find POST Which Needs to be liked !!"'}
		)

	like = Likes.query.filter_by(poid= ppoid , uid = current_user.uid).first()
	if  like:
		# returns 401 if user does not exist
		return make_response(
			'POST Already Liked By User {}'.format(current_user.name),
			401,
			{'WWW-Authenticate': 'Basic realm ="Already Liked By User !!"'}
		)


	like = Likes(ppoid ,current_user.uid)
	db.session.add(like)
	db.session.commit()

	return make_response(
		'POST liked by {}'.format(current_user.name),
		201
	)

@app.route('/unlike/<ppoid>', methods =['POST'])
@token_required
def unlike(current_user,ppoid):

	post = Posts.query.filter_by(poid = ppoid).first()

	if not post:
		# returns 401 if user does not exist
		return make_response(
			'Unable to Find POST Which Needs to be unliked',
			401,
			{'WWW-Authenticate': 'Basic realm ="Unable to Find POST Which Needs to be unliked !!"'}
		)

	like = Likes.query.filter_by(poid= ppoid , uid = current_user.uid).first()
	if not like:
		# returns 401 if user does not exist
		return make_response(
			'POST Already unliked By User {}'.format(current_user.name),
			401,
			{'WWW-Authenticate': 'Basic realm ="Already Liked By User !!"'}
		)


	db.session.delete(like)
	db.session.commit()

	return make_response(
		'POST unliked by {}'.format(current_user.name),
		201
	)


@app.route('/comment/<ppoid>', methods =['POST'])
@token_required
def add_comment(current_user,ppoid):
	auth = request.form

	if not auth or not auth.get('comments') :
		# returns 401 if any email or / and password is missing
		return make_response(
			'No Data Found',
			401,
			{'WWW-Authenticate': 'Basic realm ="Login required !!"'}
		)

	post = Posts.query.filter_by(poid = ppoid).first()

	if not post:
		# returns 401 if user does not exist
		return make_response(
			'Unable to Find POST to add comment.',
			401,
			{'WWW-Authenticate': 'Unable to Find POST to add comment. !!"'}
		)


	comment = Comments(ppoid ,current_user.uid,auth.get('comments'))
	db.session.add(comment)
	db.session.commit()

	output = []

	# appending the user data json
	# to the response list
	output.append({
		'Comment ID': comment.coid,
		'Comments' : comment.comments
	})
	return jsonify({'Comment': output})

@app.route('/posts/<ppoid>', methods =['GET'])
@token_required
def get_lc__posts(current_user,ppoid):

	post = Posts.query.filter_by(poid = ppoid).first()

	if not post:
		# returns 401 if user does not exist
		return make_response(
			'Unable to Find POST .',
			401,
			{'WWW-Authenticate': 'Unable to Find POST !!"'}
		)

	like = Likes.query.filter_by(poid=ppoid).count()
	comment = Comments.query.filter_by(poid = ppoid).count()

	output = []

	# appending the user data json
	# to the response list
	output.append({
		'Comments': comment,
		'likes':like
	})
	return jsonify({'Comment': output})

@app.route('/all_posts/', methods =['GET'])
@token_required
def get_all_posts(current_user):

	posts = Posts.query.filter_by(uid = current_user.uid).all()

	if not posts:
		# returns 401 if user does not exist
		return make_response(
			'Unable to Find POST Which Needs to be deleted',
			401,
			{'WWW-Authenticate': 'Unable to Find POST Which Needs to be deleted !!"'}
		)

	output = []
	for rec in posts:
		output.append({
			'Post ID': rec.poid,
			'title': rec.title,
			'Description': rec.decription,
			'Created At': rec.Created_at,
			'Comments': Comments.query.filter_by(poid = rec.poid).count(),
			'likes': Likes.query.filter_by(poid=rec.poid).count()
		})
	return jsonify({'Posts': output})

# route for logging user in
@app.route('/login', methods =['POST'])
def login():
	# creates dictionary of form data
	auth = request.form

	if not auth or not auth.get('email') or not auth.get('password'):
		# returns 401 if any email or / and password is missing
		return make_response(
			'Could not verify3',
			401,
			{'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
		)

	user = User.query\
		.filter_by(email = auth.get('email'))\
		.first()

	if not user:
		# returns 401 if user does not exist
		return make_response(
			'Could not verify1',
			401,
			{'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
		)

	if user.password == auth.get('password'):
		# generates the JWT Token
		token = jwt.encode({
			'public_id': user.public_id,
			'exp' : datetime.utcnow() + timedelta(minutes = 30)
		}, app.config['SECRET_KEY'])

		return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
	# returns 403 if password is wrong
	return make_response(
		'Could not verify2',
		403,
		{'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
	)


if __name__ == "__main__":
	app.run(debug = True)
	
