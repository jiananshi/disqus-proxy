## Disqus-proxy

> 基于 disqus-python 和 Flask 的 API 工具，通过在日本/香港等可以调通 Disqus 的地方部署一个代理服务来转发国内请求解决 Disqus 被墙问题，原理如下图

![theory](https://oiw32lugp.qnssl.com/2017-03-07-disqus-proxy.jpg)

### 依赖

- python
- pip
- 一台可以访问 Disqus 服务的机器（VM）

### 使用

首先执行 `pip install disqusapi` 和 `pip install flask` 安装项目依赖，安装后就可以通过 `python app.py` 运行项目了，环境等相关配置通过创建 `config.py` 进行配置，目前需要的配置项如下：

```bash
# 域名
HOST
# 端口
PORT

# Disqus PUBLIC_KEY
PUBLIC_KEY
# Disqus SECRET_KEY
SECRET_KEY

# Disqus 应用名
FORUM_NAME
# Disqus 用户名
USER_NAME = 'giraffe0813'

# 远程目录（用于发布）
REMOTE_DIR = '/data'
```

### API
1. 获取某篇文章全部文章

请求

`GET /comments?url=myblog.com`

这个接口会优先使用 queryString 中的 url 尝试从 Disqus 获取评论，默认是用请求的 Referer 作为博客 url，也就是说在博客的页面发起请求即可获得对应的评论列表，返回如下：

```javascript
{
  response: [
    {
      "author": {
        "about": "",
        "avatar": {
          "cache": "https://c.disquscdn.com/uploads/users/15662/206/avatar92.jpg?1456163221",
          "isCustom": true,
          "large": {
            "cache": "https://c.disquscdn.com/uploads/users/15662/206/avatar92.jpg?1456163221",
            "permalink": "https://disqus.com/api/users/avatars/runningkevin.jpg"
          },
          "permalink": "https://disqus.com/api/users/avatars/runningkevin.jpg",
          "small": {
            "cache": "https://c.disquscdn.com/uploads/users/15662/206/avatar32.jpg?1456163221",
            "permalink": "https://disqus.com/api/users/avatars/runningkevin.jpg"
          }
        },
        "disable3rdPartyTrackers": false,
        "id": "156620206",
        "isAnonymous": false,
        "isPowerContributor": false,
        "isPrimary": true,
        "isPrivate": false,
        "joinedAt": "2015-05-07T06:00:40",
        "location": "",
        "name": "Running Kevin",
        "profileUrl": "https://disqus.com/by/runningkevin/",
        "rep": 1.265688,
        "reputation": 1.265688,
        "reputationLabel": "Average",
        "signedUrl": "",
        "url": "",
        "username": "runningkevin"
      },
      "canVote": false,
      "createdAt": "2017-02-28T02:40:01",
      "dislikes": 0,
      "forum": "giraffe0813new",
      "id": "3178410745",
      "isApproved": true,
      "isDeleted": false,
      "isDeletedByAuthor": false,
      "isEdited": false,
      "isFlagged": false,
      "isHighlighted": false,
      "isSpam": false,
      "likes": 0,
      "media": [],
      "message": "<p>\u963f\u59e8\u8fd8\u6709\u66f4\u5389\u5bb3\u7684\u672c\u9886</p>",
      "moderationLabels": [],
      "numReports": 0,
      "parent": 3174464739,
      "points": 0,
      "raw_message": "\u963f\u59e8\u8fd8\u6709\u66f4\u5389\u5bb3\u7684\u672c\u9886",
      "thread": "5564282007"
    }
  ]
}
```

2. 发表评论

请求

`POST /comments`

参数

| 名字 | 类型 | 描述 |
| --- | --- | --- |
| email | String |  评论者邮箱 |
| name | String | 评论者昵称 |
| comment | String | 评论内容 |

这三个参数都是调用 Disqus API 时都是必须的

3. 获取最近评论

请求

`GET /comments/recent`

默认获取最近的十条评论，并且会将博主的评论过滤（捂脸），响应结构同获取评论接口，这里不再赘述。

### 部署

可以看到根目录下有一个用于发布的 fabfile.py，执行 `fab deploy` 即可根据 `config.py` 的配置发布到远程服务器指定目录下，推荐使用 supervisor 启动。

### FAQ

**1.** __call__() takes exactly 1 argument (5 given)

这个项目依赖于官方的 [python SDK](https://github.com/disqus/disqus-python)，直接通过 pip 安装这个库会报错，通过这条命令安装：`pip install git+https://github.com/disqus/disqus-python.git`

### LICENSE

MIT
built upon love &heart:
