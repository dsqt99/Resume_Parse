FROM python:3.9

EXPOSE 8080
COPY . .

RUN apt-get update && apt-get install -y poppler-utils
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]