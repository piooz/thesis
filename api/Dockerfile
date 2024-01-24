FROM python:3.11.6-alpine
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
COPY . /code
EXPOSE 80
CMD ["uvicorn", "code.app.main:app", "--host", "0.0.0.0", "--port", "80"]
