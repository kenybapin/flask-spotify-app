FROM python:3-alpine

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod 444 app.py
RUN chmod 444 requirements.txt

ENV PORT 5000

CMD ["python", "app.py"]
