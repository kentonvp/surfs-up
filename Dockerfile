FROM python:3.9.7

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
COPY scripts/ scripts/
COPY surfsup/ surfsup/

RUN pip3 install -r requirements.txt

CMD ["python3", "scripts/telegram_bot.py"]