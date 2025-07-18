############################
# 1. Base CUDA + PyTorch
############################
FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime AS base

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

############################
# 2. Point d’entrée polyvalent
############################
# mode par défaut : train
ENV MODE=train

ENTRYPOINT ["/bin/bash", "-c", "\
if [ \"$MODE\" = \"train\" ]; then \
    python training/train_tiny_gpt.py; \
elif [ \"$MODE\" = \"api\" ]; then \
    uvicorn api.main:app --host 0.0.0.0 --port 8000; \
elif [ \"$MODE\" = \"tensorboard\" ]; then \
    tensorboard --logdir training/logs --host 0.0.0.0 --port 6006; \
else \
    exec /bin/bash; \
fi"]
