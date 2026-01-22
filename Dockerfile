FROM python:3.9-slim
 
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
 
WORKDIR /app

# install system dependecies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*
 
COPY requirements.txt .
 
RUN pip install --upgrade pip && pip install -r requirements.txt
 
COPY django_blog/ .
 
RUN mkdir -p staticfiles media

EXPOSE 8000
 
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "blog_project.wsgi:application"]
