#!/usr/bin/env python
"""
Generate text with the fine‑tuned Tiny‑GPT‑2 model.

Usage
-----
python generate.py --prompt "Il était une fois" --max_tokens 80 --temperature 0.8
"""

import argparse
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


def build_generator(model_dir: str = "training/tiny-gpt2-finetuned"):
    """Charge le modèle + tokenizer et retourne un pipeline de génération."""
    model = AutoModelForCausalLM.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)

    # S'assure qu'un token de padding est défini (utile si on ajoute padding later)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0  # -> GPU; remplace par -1 si CPU
    )
    return pipe


def parse_args():
    parser = argparse.ArgumentParser(description="Generate text with fine‑tuned GPT‑2")
    parser.add_argument(
        "--prompt", type=str, required=True, help="Texte d'amorce (prompt)"
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=50,
        help="Nombre maximum de nouveaux tokens générés",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Température (>1 = plus créatif, <1 = plus conservateur)",
    )
    parser.add_argument(
        "--top_p",
        type=float,
        default=0.9,
        help="Top‑p nucleus sampling",
    )
    parser.add_argument(
        "--do_sample",
        action="store_true",
        help="Active l'échantillonnage (sinon, greedy)",
    )
    parser.add_argument(
        "--out_file",
        type=Path,
        default=None,
        help="Fichier où sauver la sortie (append).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    generator = build_generator()

    outputs = generator(
        args.prompt,
        max_new_tokens=args.max_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        do_sample=args.do_sample,
        pad_token_id=generator.tokenizer.eos_token_id,
    )

    generated = outputs[0]["generated_text"]
    print("\n=== Generated text ===\n")
    print(generated)

    # Sauvegarde éventuelle dans un fichier
    if args.out_file:
        args.out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(args.out_file, "a", encoding="utf‑8") as f:
            f.write(generated + "\n")
        print(f"\n→ Texte ajouté dans {args.out_file.resolve()}")


if __name__ == "__main__":
    main()
