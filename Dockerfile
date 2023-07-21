FROM python:3.11-slim

WORKDIR app/

COPY requirements.txt requirements.txt

EXPOSE 8080

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "-u", "/app/quickstart.py"]
