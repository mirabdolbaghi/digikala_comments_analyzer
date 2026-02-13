FROM pytorch/pytorch:2.10.0-cuda12.6-cudnn9-devel

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt  --break-system-packages


WORKDIR /src
