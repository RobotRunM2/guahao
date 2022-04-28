FROM python:3.8-alpine as build


ENV WORKDIR="GUAHAO"

# 复制项目文件到工作区
COPY Pipfile Pipfile.lock /$WORKDIR/



WORKDIR /$WORKDIR/

# alpine 设置国内软件源
# pip 安装 whell
# 通过 wheel 生成包的二进制文件
RUN set -eux && sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk add --no-cache gcc musl-dev libxslt-dev jpeg-dev zlib-dev libjpeg build-base linux-headers pcre-dev postgresql-dev libffi-dev \
    && pip install wheel -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir \
    && pip wheel -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple --wheel-dir=/$WORKDIR/wheels

FROM python:3.9-alpine

ENV WORKDIR="BenNiu-IoT-PaaS"
COPY --from=base /$WORKDIR /$WORKDIR

WORKDIR /$WORKDIR/

RUN set -eux && sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk add --no-cache libuuid pcre libxml2 mailcap\
    && pip install --no-index --find-links=/$WORKDIR/wheels -r requirements.txt \
    && rm -rf wheels

EXPOSE 8088

CMD python main.py