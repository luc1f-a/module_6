FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get upgrade -y && apt-get install iputils-ping -y

COPY ./ /app

EXPOSE 3000

CMD ["python", "server.py"]