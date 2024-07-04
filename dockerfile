FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt && rm requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:8050", "--reload", "index:server"]