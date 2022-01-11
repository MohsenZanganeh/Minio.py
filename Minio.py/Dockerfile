FROM python:3.8
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
COPY ./requirements.txt /requirements.txt
RUN echo "y" | apt-get update
RUN echo "y" | apt-get upgrade
RUN echo "y" | apt install unixodbc unixodbc-dev freetds-dev tdsodbc 
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir /app
WORKDIR /app
COPY /app /app/
