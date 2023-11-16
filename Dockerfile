# syntax=docker/dockerfile:1.4
FROM python:3.11.3-slim-buster
# ARG BUILDPLATFORM=linux/amd64
# FROM --platform=$BUILDPLATFORM python:3.11.3-slim-buster AS builder

WORKDIR /seven

COPY requirements.txt /seven
COPY boot.sh /seven
RUN python -m pip install --upgrade pip
RUN pip install wheel
RUN --mount=type=cache,target=/seven/.cache/pip \
    pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP entrypoint.py
ENV APP_SETTINGS_MODULE config.dev

EXPOSE 5000

# CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000", "--debug" ] # works!
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "entrypoint:app"] # works!
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "-t", "60", "entrypoint:app"]
