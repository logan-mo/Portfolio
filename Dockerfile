FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
ENV PORT=8080

CMD ["gunicorn", "-b", ":8080", "run:app"]
