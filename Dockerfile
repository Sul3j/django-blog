FROM python:3.9
 
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
 
WORKDIR /app
 
COPY requirements.txt .
 
RUN pip install --upgrade pip && pip install -r requirements.txt
 
COPY django_blog/ .
 
RUN mkdir -p staticfiles

EXPOSE 8000
 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]