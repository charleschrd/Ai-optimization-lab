# 📝 Inference — Text Generation with Tiny‑GPT‑2

This script lets you generate text locally from the fine‑tuned model saved in `training/tiny-gpt2-finetuned/`.

---

## 1 · Quick Start (Docker)

```bash
docker run --rm -it --gpus all -e MODE=shell -v $(pwd):/workspace ai-opt-lab
# inside container
python inference/generate.py \
  --prompt "Il était une fois" \
  --max_tokens 80 \
  --temperature 0.8 \
  --do_sample
````

---

## 2 · CLI Options

| Flag            | Default    | Description                      |
| --------------- | ---------- | -------------------------------- |
| `--prompt`      | *required* | Initial text to continue         |
| `--max_tokens`  | 50         | Number of tokens to generate     |
| `--temperature` | 1.0        | >1 = creative, <1 = conservative |
| `--top_p`       | 0.9        | Nucleus sampling                 |
| `--do_sample`   | False      | If false → greedy decoding       |
| `--out_file`    | *None*     | Append output to file            |

Example:

```bash
python inference/generate.py --prompt "Once upon a time" --max_tokens 60 --temperature 0.7 --out_file outputs.txt
```

---

## 🇫🇷 Résumé rapide

* Lancer un shell Docker puis :

  ```bash
  python inference/generate.py --prompt "Bonjour" --max_tokens 60 --do_sample
  ```
* Paramètres modifiables : longueur, température, top‑p, etc.
* Ajoutez `--out_file` pour sauvegarder chaque sortie.

````

---
