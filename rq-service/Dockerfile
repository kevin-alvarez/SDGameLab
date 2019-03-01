FROM python:3.7.2

ENV BIND_PORT 5000
ENV QUEUE_HOST localhost
ENV QUEUE_PORT 6379
ENV CACHE_HOST localhost
ENV CACHE_PORT 6379

COPY ./requeriments.txt /requeriments.txt

RUN pip install -r /requeriments.txt
RUN pip install -U flask-cors

COPY ./service.py ./service.py
COPY jobs/actions.py ./actions.py

EXPOSE $BIND_PORT

CMD ["python", "/service.py"]
