FROM python:3.12

WORKDIR /app

RUN pip install tinydb discord

COPY ./src /app

CMD [ "python3", "bot.py" ]

