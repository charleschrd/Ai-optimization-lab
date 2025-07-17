# 🧠 AI Optimization Lab

This repository is a personal AI lab focused on experimenting with the complete lifecycle of Large Language Models (LLMs): from training to optimization (pruning, quantization, distillation), and eventually deployment simulation on hardware accelerators like FPGAs.

---

## 🚀 Project Goals

- Fine-tune small-scale LLMs (e.g., DistilGPT2) on local data
- Apply core optimization techniques:
  - ✅ Pruning
  - ✅ Quantization
  - ✅ Knowledge Distillation
- Simulate deployment on hardware: NVIDIA GPU passthrough + FPGA via HLS
- Build everything locally with reproducible infrastructure (Proxmox + Docker)

---

## 💻 Infrastructure Overview

This project runs fully **on-premise**, leveraging a custom GPU virtualized environment.

### 🧱 Base Host

- **Proxmox VE** (bare metal)
- **CPU:** Ryzen 5 3600
- **RAM:** 16 GB DDR4
- **GPU:** NVIDIA RTX 3070 (8GB VRAM)

### ⚙️ Virtual Machine Setup

- **OS:** Ubuntu 24.04 (VM guest)
- **GPU Passthrough:** enabled via VFIO and `q35` machine model
- **Config:**

  - BIOS: `OVMF` (UEFI)
  - GRUB: `amd_iommu=on iommu=pt`
  - PCI passthrough:
    ```
    qm set 100 -hostpci0 07:00.0,pcie=1
    qm set 100 -hostpci1 07:00.1,pcie=1
    ```
  - Netplan configuration for static IP

### 🐳 Docker Stack

- Containerized with GPU support using `--gpus all`
- Base image: `pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime`
- Mounts local repo via `-v $(pwd):/workspace`

---

## 🏗️ Project Structure

```bash
ai-optimization-lab/
├── training/               # LLM training scripts
├── pruning/                # Model pruning experiments
├── distillation/           # Teacher-student compression
├── quantization/           # INT8/FP16 inference optimizations
├── simulation_fpga/        # Vitis/HLS exploration (WIP)
├── notebooks/              # Jupyter/analysis
├── data/                   # Preprocessing and datasets
├── utils/                  # Helper utilities
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🔧 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/charleschrd/ai-optimization-lab.git
cd ai-optimization-lab

# Build the container
docker build -t ai-opt-lab .

# Run with GPU passthrough
docker run --rm -it --gpus all -v $(pwd):/workspace ai-opt-lab
```

---

## 🧪 Example: Fine-tuning DistilGPT2

```bash
cd training
python train_tiny_gpt.py
```

---

## 🛠️ Roadmap

- [x] GPU passthrough & Docker GPU-ready
- [x] Fine-tune DistilGPT2 locally
- [ ] ONNX + INT8 quantization
- [ ] Knowledge distillation pipeline
- [ ] HLS model conversion with Vivado/Vitis AI
- [ ] Streamlit/Grafana-based model metrics dashboard

---

## 🤝 Contributing

This lab is personal and evolving — feel free to fork, test, and submit ideas via Issues or Pull Requests.

---

## 📜 License

MIT — feel free to reuse with credit.
