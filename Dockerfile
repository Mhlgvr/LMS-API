FROM python:3.9-slim
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
LABEL authors="zampo"
COPY . .
CMD ["python", "app.py"]
