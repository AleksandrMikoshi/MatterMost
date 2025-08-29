FROM python:3.8-slim

WORKDIR /opt/moderator_bot/app

COPY moderator_bot.py /opt/moderator_bot/app/
COPY requirements.txt /opt/moderator_bot/app/

RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["python", "moderator_bot.py"]