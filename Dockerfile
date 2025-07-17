FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /workspace
CMD ["bash"]
