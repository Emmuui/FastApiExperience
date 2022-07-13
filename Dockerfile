FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /workdir

COPY requirements.txt /workdir/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /workdir/requirements.txt


COPY . /workdir/


