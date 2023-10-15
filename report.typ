#set heading(level: 1, numbering: "1.1.")

= 作业1 - 报告

#set text(font: "Noto Serif CJK SC")


软件03 陈启乾 202012385

== 要求

- 简单描述单元测试部分用例的设计思路、实现思路、测试用例列表及覆盖率并进行分析；

- 简要描述集成测试和端到端测试部分的实现思路；

- 简要描述 Docker 部署部分的实现思路以及体会；

== 代码风格测试

编写 Flake8 配置文件即可。

```
[flake8]
# 忽略且仅忽略 .git，所有 __pycache__ 文件夹，所有 migrations 文件夹
exclude = 
    .git,
    __pycache__,
    migrations
```

忽略文件需要使用 `exclude` 命令。

```yaml
# 对 tests/test_e2e.py 忽略E501错误，对 tests/test_api.py 忽略E501错误，对 driver.py 忽略E501错误，对 app/settings.py 忽略E501错误，对 user/views.py 忽略E722错误，对 app/settings_prod.py 忽略F401和F403错误
per-file-ignores =
    tests/test_e2e.py: E501,
    tests/test_api.py: E501,
    driver.py: E501,
    app/settings.py: E501,
    user/views.py: E722,
    app/settings_prod.py: F401,F403
```

忽略个别错误需要使用 `per-file-ignores` 命令。

在 lint.sh 文件中：

```sh
autopep8 --in-place --recursive .
```

使用 `autopep8` 对代码自动格式化。

```sh
autoflake --in-place --recursive --remove-unused-variables .
```

使用 autoflake 对代码自动格式化。

```sh
isort .
```

使用 isort 对代码自动格式化。

```sh
flake8
```

使用 flake8 检查代码风格。

== 单元测试

单元测试包括两部分：基础函数的补全和单元测试的编写。

=== 基础函数的补全: `register_params_check`

1. 针对必填项，会首先判断是否存在该项目，不存在则直接报错；对于可选项，不存在时则会填充默认值。
2. 其次会判断内容的类型、长度等简单的信息
3. 最后利用正则表达式判断所有其他限制。对于较为复杂的情况例如域名，也会结合 Python 语句先进行分割。

=== 测试函数

针对每一个分支判断的判断的错误的输入，我们都编写了一个对应的测试函数，函数名就反映了测试的范围。

总体样例：

#align(center, 
    image("image.png", width: 75%)
)
具体实现：

#align(center, 
    image("image-1.png", width: 75%)
)

例如在这个例子中，我们想要测试没有用户名的情况下程序的输出，因此我们就构造了一个没有用户名的用例。

测试样例列表：

#table(
    columns: (auto, auto, auto, auto, auto, auto, auto),
    [username], [password], [nickname], [mobile], [url], [magic_number], [备注],
    [], [Abc12345\*], [test], [+86.123456789012], [https://www.google.com], [0]

)


=== 覆盖率

运行：`python manage.py test --filter test_basic`

#image("image-2.png")

== 集成测试

在 `tests/test_api.py` 中完成集成测试。

=== 整体思路

用请求模拟用户的错误的操作。需要手动记录登录成功后的 `jwt` token 并传作 Header 的 `Authorization` 字段。

```py
data = { ... }  # 构造错误数据
response = self.client.patch(
    reverse(user_views.login),
    data=data,
    content_type="application/json"
) # 发送请求
json_data = response.json()
# 判断返回值
self.assertEqual(response.status_code, 401) # 1. 如果失败
self.assertEqual(response.status_code, 200) # 2. 如果成功
self.assertEqual(json_data['message'], "Invalid credentials") # 失败 / 成功信息 
```

=== 登录功能

+ 使用错误的信息进行登录，检查返回值为失败
    - 错误的用户名
    - 错误的密码
+ 使用正确的信息进行登录，检查返回值为成功
+ 进行登出，检查返回值为成功

=== 注册功能

+ 使用错误信息进行注册，检查返回值为失败
+ 使用正确的的信息进行注册，检查返回值为成功
+ 使用正确的信息进行登录，检查返回值为成功

=== 登出功能

+ 未登录直接登出，检查返回值为失败

=== 测试结果

#image("image-3.png")

== 端到端测试

端到端测试集成了 `selenium` 进行自动化操作。

只需将 `DRIVER_PATH` 修改为 `drivers/chromedriver` 即可。

运行 `python manage.py test --filter test_e2e` 即可。


== Docker 部署部分

=== 主体要求

创建了两个网络：`inner` 和 `front`，用来隔离 Mysql 和 Nginx。

=== 后端 Django 服务

Django 服务使用 DockerFile 构建，Docker Compose 集成。

Dockerfile 包括如下内容：

+ 从 `python:3.8-buster` 开始构建
+ 升级 `pip`，根据 `requirements.txt` 使用 `pip` 安装依赖
+ 复制当前文件夹内所有的文件到 `/app/` 下
+ 暴露 `8000` 端口
+ 定义环境变量：`ENV DJANGO_SETTINGS_MODULE app.settings_prod` 采用部署设置
+ 进行 migrate：`CMD python manage.py migrate --settings=app.settings_prod`
+ 运行 `Gunicorn` 服务器：`CMD gunicorn -w4 -b 0.0.0.0:8000 --log-level=debug app.wsgi`

Docker Compose 中包括如下内容：

+ 容器名为 `app`
+ 从当前文件夹构建 `build: .`
+ 依赖 mysql 服务：`depends_on: mysql`
+ 使用 `inner` 和 `front` 网络，可以同时被 `Nginx` 访问和访问 `Mysql` 服务


=== Mysql 服务器

Mysql 服务器在 Docker Compose 中启动。

+ 使用 `mysql:8.1` 镜像
+ 容器名为 `mysql`
+ 配置环境变量如下:
    - `MYSQL_ROOT_PASSWORD=2020012385` 密码为学号
    - `MYSQL_DATABASE=thss` 数据库名为
    - `TZ=Asia/Shanghai` 时区为背景时间
+ 持久化存储，将 `/home/ubuntu/mysql` 目录映射到 `/var/lib/mysql` 下
+ 启动命令：`mysqld --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci`
+ 使用 `inner` 网络，只有后端 Django 服务可以访问到


=== Nginx 反向代理

Nginx 反向代理在 Docker Compose 中启动

+ 使用 `nginx:latest` 镜像
+ 容器名为 `nginx` 
+ 依赖后端 Django 服务: `depends_on: backend`
+ 持久化存储：
    - `./nginx/app.conf:/etc/nginx/conf.d/default.conf` 配置文件
    - `./build/:/opt/build/` 生成的静态文件映射到 `/opt/build`
+ 使用 `front` 网络
+ 向外暴露 8000 端口

关于 Nginx 配置文件：

```conf
server {
    # 暴露 8000 端口
    listen 8000;
    server_name localhost;

    root /opt/build;

    # 处理静态部分
    location / { 
        try_files $uri $uri/ @router;
        index index.html;
    }

    # 后端
    location /api/v1 {
        proxy_pass http://backend:8000/api/v1;
    }
}
```


=== 体会

Docker 很好地隔绝了各个服务，让我们可以做到解耦之后专注于某个服务本身的构建。