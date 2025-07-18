from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
import torch

# 1. Load pretrained tokenizer & model
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_name)

# 2. Load and tokenize the dataset (using WikiText-2 as an example)
dataset = load_dataset("wikitext", "wikitext-2-raw-v1")
def tokenize_function(batch):
    return tokenizer(batch["text"], return_special_tokens_mask=True, truncation=True, padding="max_length", max_length=128)

tokenized_datasets = dataset.map(tokenize_function, batched=True, remove_columns=["text"])

# 3. Prepare data collator for causal language modeling (since we're not using MLM)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# 4. Define training arguments (with TensorBoard logging enabled)
training_args = TrainingArguments(
    output_dir="./model_output",
    eval_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=1,
    logging_dir="./logs",             # directory for TensorBoard logs
    logging_strategy="steps",         # log training metrics every few steps
    logging_steps=100,                # log every 100 steps (adjust as needed)
    report_to="tensorboard",          # enable logging to TensorBoard
    push_to_hub=False
)

# 5. Create Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator
)

# 6. Fine-tune the model
trainer.train()

# 7. Save the fine-tuned model and tokenizer
trainer.save_model("tiny-gpt2-finetuned")
tokenizer.save_pretrained("tiny-gpt2-finetuned")
