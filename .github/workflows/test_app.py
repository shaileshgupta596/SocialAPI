from app import app, User
from app import db
import json

client = app.test_client()


def login():
    print('----------------------------------------Login Test Case -------------------------------------------')
    res = client.post('https://socialmediaapi-cqjc.onrender.com/login', data= {"email" : "abc@gmail.com","password":"123"})
    res = json.loads(res.text)
    print('After Successful Login JWT Token Created : {}'.format(res))
    token = res['token']
    return token

def follow(token):
    print('----------------------------------------Following TestCase -------------------------------------------')
    res = client.post('https://socialmediaapi-cqjc.onrender.com/follow/1',headers= {"x-access-token" : token })
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/follow/1', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/follow/2', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/follow/2', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/follow/3', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/follow/3', headers={"x-access-token": token})
    print(res.text)

def unfollow(token):
    print('----------------------------------------UnFollowing TestCase -------------------------------------------')
    res = client.post('https://socialmediaapi-cqjc.onrender.com/unfollow/1',headers= {"x-access-token" : token })
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/unfollow/1', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/unfollow/2', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/unfollow/2', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/unfollow/3', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/unfollow/3', headers={"x-access-token": token})
    print(res.text)

def user_auth_profile(token):
    print('----------------------------------------Profile Details TestCase -------------------------------------------')
    res = client.get('https://socialmediaapi-cqjc.onrender.com/user', headers={"x-access-token": token})
    print(json.loads(res.text))

def add_post(token):
    print('----------------------------------------Add Post TestCase -------------------------------------------')
    res = client.post('https://socialmediaapi-cqjc.onrender.com/posts',headers={"x-access-token": token},data = {"title":"Cricket", 'description': 'Ind Wins Against NZ'})
    print(json.loads(res.text))
    res = client.post('https://socialmediaapi-cqjc.onrender.com/posts', headers={"x-access-token": token},
                      data={"title": "Cricket", 'description': 'Sky Hits 111 Not OUT'})
    print(json.loads(res.text))
    res = client.post('https://socialmediaapi-cqjc.onrender.com/posts', headers={"x-access-token": token},
                      data={"title": "Cricket", 'description': 'NZ 130 All Out.'})
    print(json.loads(res.text))

def del_post(token):
    print('----------------------------------------Del Post TestCase -------------------------------------------')
    res = client.post('https://socialmediaapi-cqjc.onrender.com/posts/3', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/posts/3', headers={"x-access-token": token})
    print(res.text)

def like(token):
    print('----------------------------------------like TestCase -------------------------------------------')
    res = client.post('https://socialmediaapi-cqjc.onrender.com/like/3', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/like/1', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/like/2', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/like/1', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/like/2', headers={"x-access-token": token})
    print(res.text)

def unlike(token):
    print('----------------------------------------unlike TestCase -------------------------------------------')
    res = client.post('https://socialmediaapi-cqjc.onrender.com/unlike/3', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/unlike/1', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/unlike/2', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/unlike/1', headers={"x-access-token": token})
    print(res.text)
    res = client.post('https://socialmediaapi-cqjc.onrender.com/unlike/2', headers={"x-access-token": token})
    print(res.text)

def add_comment(token):
    print('----------------------------------------AddComments TestCase -------------------------------------------')
    res = client.post('https://socialmediaapi-cqjc.onrender.com/comment/1', headers={"x-access-token": token}, data = {"comments":"Yes Well Deserved win"})
    print(json.loads(res.text))
    res = client.post('https://socialmediaapi-cqjc.onrender.com/comment/2', headers={"x-access-token": token},
                      data={"comments": "Sky has No limits Now.Great Innings"})
    print(json.loads(res.text))

def post_details(token):
    print('----------------------------------------Post Details TestCase -------------------------------------------')
    res = client.get('https://socialmediaapi-cqjc.onrender.com/posts/1', headers={"x-access-token": token})
    print(json.loads(res.text))
    res = client.get('https://socialmediaapi-cqjc.onrender.com/posts/2', headers={"x-access-token": token})
    print(json.loads(res.text))
    res = client.get('https://socialmediaapi-cqjc.onrender.com/posts/3', headers={"x-access-token": token})
    print(res.text)
    res = client.get('https://socialmediaapi-cqjc.onrender.com/posts/4', headers={"x-access-token": token})
    print(res.text)

def all_post(token):
    print('----------------------------------------All Post to Current User TestCase -------------------------------------------')
    res = client.get('https://socialmediaapi-cqjc.onrender.com/all_posts/', headers={"x-access-token": token})
    print(json.loads(res.text))

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    u1 = User(1, 1234, 'Shailesh', 'abc@gmail.com', '123')
    u2 = User(2, 1235, 'Mahesh', 'xyz@gmail.com', '123')
    u3 = User(3, 1246, 'Ramesh', 'mno@gmail.com', '123')
    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.commit()
    token = login()
    print(token)
    print('\n')
    follow(token)
    print('\n')
    unfollow(token)
    print('\n')
    follow(token)
    print('\n')
    user_auth_profile(token)
    print('\n')
    add_post(token)
    print('\n')
    del_post(token)
    print('\n')
    like(token)
    print('\n')
    unlike(token)
    print('\n')
    add_comment(token)
    print('\n')
    post_details(token)
    print('\n')
    all_post(token)

