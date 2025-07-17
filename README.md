# 🧠 AI Optimization Lab

This repository is a personal lab designed to experiment with the full lifecycle of modern language models (LLMs) — from training to hardware-level optimization.

## 🎯 Goals

- Train a small-scale LLM on a custom corpus
- Apply model **pruning**, **distillation**, and **quantization**
- Simulate hardware deployment via **FPGA (HLS)** using Vitis AI or HLS4ML
- Visualize performance trade-offs: size, speed, accuracy, memory usage

## 📦 Structure

ai-optimization-lab/
├── data/ # datasets and preprocessing
├── training/ # training scripts (TinyGPT, etc.)
├── pruning/ # weight pruning experiments
├── distillation/ # student-teacher models
├── quantization/ # int8/fp16 quantization
├── simulation_fpga/ # Vivado/HLS4ML integration
├── notebooks/ # Jupyter analysis
├── utils/ # shared helpers
├── Dockerfile # reproducible environment
├── requirements.txt
└── README.md

markdown
Copier
Modifier

## 🧪 Future Work

- Add CI pipeline (pytest + pre-commit)
- Add HuggingFace Spaces integration
- Setup ArgoCD for MLOps demo
