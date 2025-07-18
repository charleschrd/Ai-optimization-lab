### 1️⃣ `inference/README.md` — copy/paste **entire block**

````markdown
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

### 2️⃣ `api/README.md` — copy/paste **entire block**

```markdown
# 🌐 API — FastAPI service for Tiny‑GPT‑2

Expose the fine‑tuned model through a REST endpoint compatible with browser, curl, or n8n workflows.

---

## 1 · Launch the API (Docker)

```bash
docker run --rm --gpus all \
  -e MODE=api \
  -p 8000:8000 \
  -v $(pwd):/workspace \
  ai-opt-lab
# Swagger UI: http://localhost:8000/docs
````

The container loads `training/tiny-gpt2-finetuned/` at startup.

---

## 2 · Endpoints

| Method | Route             | Purpose                              |
| ------ | ----------------- | ------------------------------------ |
| `GET`  | `/health`         | Liveness probe → `{ "ok": true }`    |
| `GET`  | `/models`         | List available models                |
| `POST` | `/v1/completions` | Generate continuation (OpenAI‑style) |

### Request (`POST /v1/completions`)

```json
{
  "prompt": "Hello, my name is",
  "generation": {
    "max_tokens": 80,
    "temperature": 0.8,
    "top_p": 0.9,
    "do_sample": true
  }
}
```

### Response

```json
{
  "id": "bf5e2b7e-e3cc-47df-8a06-0e6e6c9e2e1f",
  "model": "tiny-gpt2-finetuned",
  "choices": [
    {
      "text": "Hello, my name is Tiny‑GPT and I love to help you..."
    }
  ]
}
```

---

## 3 · Curl Test

```bash
curl -X POST http://localhost:8000/v1/completions \
     -H "Content-Type: application/json" \
     -d '{"prompt":"Bonjour","generation":{"max_tokens":60}}'
```

---

## 4 · Integrating with n8n

1. Add an **HTTP Request** node →

   * Method: POST
   * URL: `http://tiny-gpt-api:8000/v1/completions`
2. Body (JSON): `{ "prompt": "{{ $json.prompt }}" }`
3. Use response `{{ $json.choices[0].text }}` in next nodes (email, DB, etc.).

---

## 🇫🇷 Résumé rapide

* Démarrez le service :

  ```bash
  docker run --rm --gpus all -e MODE=api -p 8000:8000 -v $(pwd):/workspace ai-opt-lab
  ```

* **Tester** :

  ```bash
  curl -X POST http://localhost:8000/v1/completions \
       -H "Content-Type: application/json" \
       -d '{"prompt":"Il était une fois"}'
  ```

* Documentation interactive : [http://localhost:8000/docs](http://localhost:8000/docs). Integrable dans n8n via un nœud HTTP.

---

```

Each README is inside a **single copy‑paste block**, ready to drop into the corresponding folder.
```
