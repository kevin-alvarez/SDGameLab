FROM python:3.7.2

ENV BIND_PORT 5000
ENV REDIS_HOST localhost
ENV REDIS_PORT 6379

COPY ./requeriments.txt /requeriments.txt

RUN pip install -r /requeriments.txt

COPY ./app.py /app.py
COPY ./works.py /works.py

EXPOSE $BIND_PORT

CMD ["python", "/app.py"]
