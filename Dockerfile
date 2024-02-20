FROM python:3.8-slim

WORKDIR /app

COPY app.py /app/app.py
COPY model.joblib /app/model.joblib
COPY src/ /app/src/
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
