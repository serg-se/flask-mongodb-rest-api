FROM python:3.10-slim-bullseye

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY flask_server.py config.py ./

ENV FLASK_APP flask_server.py

CMD ["gunicorn", "-b", ":5000", "--access-logfile", "-", "--error-logfile", "-", "flask_server:app"]