# coding: utf8

from disqusapi import DisqusAPI
from flask import (
    Flask,
    request,
    jsonify
)
from config import (
    HOST,
    PORT,

    PUBLIC_KEY,
    SECRET_KEY,

    CERTIFICATE_CERT,
    PRIVATE_CERT,

    FORUM_NAME,
    USER_NAME
)

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


# 根据 request.Referer 获取 Disqus 评论
@app.route('/comments', methods=['GET'])
def get_comments():
    # 通过 queryString 方便测试
    client_url = request.args.get('url') or request.headers.get('Referer')
    if not client_url:
        return jsonify(code=400, msg='url is required')
    # 有些 url 需要在结尾手动添加 `index.html`
    if client_url in URL_NEED_REWRITE:
        client_url += 'index.html'
    # 根据 url 获取博客
    thread = disqus.get(
        'threads.details',
        method='GET',
        forum=FORUM_NAME,
        thread=u'link:{}'.format(client_url))
    # 根据博客获取评论
    posts = disqus.get(
        'posts.list',
        method='GET',
        thread=thread.get('id'))
    return jsonify(response=posts)


@app.route('/comments', methods=['POST'])
def create_comment():
    REQUIRED_FIELD = ['email', 'comment', 'name']

    if not request.data:
        return jsonify(code=400, msg=u'request params can not be empty')

    req_data = json.loads(request.data)

    client_url = request.args.get('url') or request.headers.get('Referer')

    if not client_url:
        return jsonify(code=400, msg=u'url/referer is required')

    # 提交评论时，邮箱/评论内容/昵称 缺一不可
    for field in REQUIRED_FIELD:
        field_data = req_data.get(field, '')
        if not field_data or \
                not isinstance(field_data, str):
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

    return jsonify(response=create_result)


@app.route('/comments/recent', methods=['GET'])
def get_recentcomments():
    recent_posts = disqus.get(
        'forums.listPosts',
        method='GET',
        forum=FORUM_NAME,
        limit=10)

    # 过滤掉博主发出的评论
    recent_posts = filter(
        lambda post: post.get('author').get('username') != USER_NAME,
        recent_posts)

    return jsonify(response=recent_posts)

if CERTIFICATE_CERT and PRIVATE_CERT:
    app.run(host=HOST, port=PORT, context=(CERTIFICATE_CERT, PRIVATE_CERT))
else:
    app.run(host=HOST, port=PORT)
