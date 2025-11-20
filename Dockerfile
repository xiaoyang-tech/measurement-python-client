FROM xiaoyangtech/measurement-python-client-sdk:latest
LABEL authors="colin chang"

ARG ACCELERATE_CONFIG
COPY ./src .
COPY ./requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir ${ACCELERATE_CONFIG} -r requirements.txt

CMD ["python3", "VideoFileSample.py"]