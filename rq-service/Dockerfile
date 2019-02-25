FROM python:3.7.2

ENV BIND_PORT 5000
ENV REDIS_HOST localhost
ENV REDIS_PORT 6379

COPY ./requeriments.txt /requeriments.txt

RUN pip install -r /requeriments.txt

COPY ./service.py ./service.py
COPY jobs/actions.py ./actions.py

EXPOSE $BIND_PORT

CMD ["python", "/service.py"]
