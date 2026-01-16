FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apk update && apk add --no-cache bash

WORKDIR /app

COPY ./app/requirements ./requirements

RUN pip install -r requirements/dev.txt


COPY ./app .

RUN chmod +x ./prestart.sh
RUN chmod +x ./run

ENTRYPOINT ["./prestart.sh"]
CMD ["./run"]