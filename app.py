# coding: utf8

from disqusapi import DisqusAPI
from flask import (
    Flask,
    jsonify
)
from config import (
    HOST,
    PORT,

    PUBLIC_KEY,
    SECRET_KEY,

    FORUM_NAME,
    USER_NAME
)

import request
import json

disqus = DisqusAPI(SECRET_KEY, PUBLIC_KEY)
app = Flask(__name__)
app.debug = True

URL_NEED_REWRITE = [
    'http://yemengying.com/message/',
    'http://yemengying.com/about/',
    'http://yemengying.com/friends/'
]


@app.route('/')
def index():
    return jsonify(code=200, msg='it works')


@app.route('/comments', methods=['GET'])
def get_comments():
    client_url = request.args.get('url') or request.headers.get('Referer')

    if not client_url:
        return jsonify(code=400, msg='url is required')

    if client_url in URL_NEED_REWRITE:
        client_url += 'index.html'

    thread = disqus.get(
        'threads.details',
        method='GET',
        forum=FORUM_NAME,
        thread=u'link:{}'.format(client_url))

    posts = disqus.get(
        'posts.list',
        method='GET',
        thread=thread.get('id'))

    return jsonify(posts)


@app.route('/comments', methods=['POST'])
def create_comment():
    REQUIRED_FIELD = ['email', 'comment', 'name']

    if not request.data:
        return jsonify(code=400, msg=u'request params can not be empty')

    request_data = json.loads(request.data)

    client_url = request.args.get('url') or request.headers.get('Referer')

    if not client_url:
        return jsonify(code=400, msg=u'url/referer is required')

    for field in REQUIRED_FIELD:
        field_data = req_data.get(field, '')
        if not field_data or \
            not isinstance(field_data, str) \
            not field_data.strip():

            return jsonify(
                code=400,
                msg=u'参数 {}: {} 不合法'.format(field, field_data))

    thread = disqus.get(
        'threads.details',
        method='GET',
        forum=FORUM_NAME,
        thread=u'link:{}'.format(client_url))

    create_result = disqus.get(
        'posts.create',
        method='POST',
        thread=thread.get('id'),
        author_email=req_data.get('email'),
        author_name=req_data.get('name'),
        message=req_data.get('comment'),
        parent=req_data.get('parent'))

    return jsonify(create_result)


@app.route('/comments/recent', methods=['GET'])
def get_recentcomments():
    recent_posts = disqus.get(
        'forums.listPosts',
        method='GET',
        forum=FORUM_NAME,
        limit=10)

    recent_posts = filter(
        lambda post: post.get('author').get('username') != USER_NAME,
        recent_posts)

    return jsonify(recent_posts)


app.run(host=HOST, port=PORT)
