# 编写合适的 Dockerfile 以及 docker-compose 配置（必要时你需要调整清软论坛的代码）来实现：
# 清软论坛以 MySQL 为数据库、通过 nginx 以 8000 端口向外提供服务；
# 通过你的服务器 ip:8000 可以访问到论坛前端并正常进行各项操作；
# 通过你的服务器 ip:8000/api/v1 可以直接访问后端的各项 API；

FROM python:3.8-buster

RUN mkdir /app

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt --no-cache-dir

COPY . /app

EXPOSE 8000


ENV DJANGO_SETTINGS_MODULE app.settings_prod

CMD python manage.py migrate --settings=app.settings_prod

CMD gunicorn -w4 -b 0.0.0.0:8000 --log-level=debug app.wsgi
