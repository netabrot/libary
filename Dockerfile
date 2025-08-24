FROM python:3.9


WORKDIR /app

EXPOSE 8000

COPY ./requirements.txt /requirements.txt


RUN pip install --no-cache-dir --upgrade -r /requirements.txt


COPY ./app ./app


CMD ["uvicorn", "run", "app/main.py", "--port", "8000"]