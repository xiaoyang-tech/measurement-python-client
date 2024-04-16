FROM xiaoyangtech/measurement-python-client-sdk:2.0
LABEL authors="colin chang"

WORKDIR /app
COPY ./resources /app/resources
COPY ./src /app/src

CMD ["python", "src/VideoFileSample.py"]