FROM python:3.7

COPY . /keci
WORKDIR /keci

RUN pip install kafka-python
RUN pip install pytest

CMD ["python", "src/app.py"]
