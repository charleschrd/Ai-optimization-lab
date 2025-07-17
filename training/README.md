# Training Log — TinyGPT

This is a snapshot of a successful training session performed on a local VM using GPU passthrough.

![Training in progress](./training_screenshot.png)

- Dataset: HuggingFace TinyStories (Parquet)
- GPU: RTX 3070 (via Proxmox PCIe passthrough)
- Framework: HuggingFace Transformers + Accelerate
- Runtime: Docker + CUDA 12.2

```bash
python train_tiny_gpt.py
```
