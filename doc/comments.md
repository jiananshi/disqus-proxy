## 评论

### 目录

- [获取文章评论](#doc1)
- [发表评论](#doc2)
- [获取博客最近评论](#doc3)

<h2 id="doc1">获取文章评论</h2>

`GET /comments?url=http://yemengying.com/java-abc`

#### 参数

| 参数名 | 类型 | 必选 | 备注 |
| ------ | ---- | ---- | ---- |

#### 返回

```json
{
  "code": 0,
  "cursor": {},
  "response": [
    {
      "author": {
        "username": "giraffe0813",
        "id": "08131234"
      }
      "raw_message": "some comments balabala...",
      "media": [],
      "thread": 123123,
      "created_at": "2016-09-11T08:15:21"
    }
  ]
}
```

