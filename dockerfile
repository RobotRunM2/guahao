FROM python:3.8-alpine as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv && apk add gcc

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN adduser -D appuser
USER appuser

# Install application into container
COPY /src/ /home/appuser/app_guahao

WORKDIR /home/appuser/app_guahao

# 定义配置文件卷
VOLUME /home/appuser/app_guahao/config

# Run the application
ENTRYPOINT ["python", "start.py"]

# run cdm
# docker run -d --restart=always  -v ~/guahao/config:/home/appuser/app_guahao/config  --name=app_guahao guahao:20220630
