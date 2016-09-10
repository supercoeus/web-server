# web-server
web后端



## 状态码定义

HTTP状态码 |  说明
---|---|
200 |请求正确
404 |资源不存在
400 |失败，字段错误，非法路径
500 |错误，内部错误


## 错误码定义

返回码 | HTTP状态码 | 说明
---|---|---
1000 | 400 | 查询参数错误
1001 | 500 | mongodb查询失败


## 使用容器
### 制作镜像

```
docker build -t web-server .
```

### 启动镜像

```
docker-compose -p web-server -f docker-compose.yml up -d
```

