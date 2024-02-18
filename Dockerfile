FROM python:3.10

WORKDIR /game

COPY src /game/src
COPY data /game/data
COPY art_data /game/art_data
COPY requirements.txt /game/

RUN python3 -m venv /opt/venv
RUN  pip install --upgrade pip
RUN . /opt/venv/bin/activate && pip install -r requirements.txt

CMD . /opt/venv/bin/activate && exec python3 -u src/main.py