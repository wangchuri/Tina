import os
import torch
from transformers import AutoTokenizer, Qwen2VLForConditionalGeneration
from peft import LoraConfig, get_peft_model
from datasets import Dataset
import pandas as pd
from transformers import TrainingArguments, Trainer
from transformers.data.data_collator import DataCollatorForSeq2Seq
import torch.distributed as dist

# 初始化分布式环境
dist.init_process_group(backend='nccl')

# 设备加载
device = 'cuda' if torch.cuda.is_available() else 'cpu'
local_rank = int(os.environ["LOCAL_RANK"])
torch.cuda.set_device(local_rank)

# 使用相对路径
BASEDIR = "./"
model_dir = os.path.join(BASEDIR, '../model/Qwen2-VL-7B-Instruct')
print(model_dir)

# 分词器加载
tokenizer = AutoTokenizer.from_pretrained(
    model_dir,
    use_fast=False, 
    trust_remote_code=True
)

# 模型加载
model = Qwen2VLForConditionalGeneration.from_pretrained(
    model_dir,
    device_map='auto',  # 使用自动设备映射
    torch_dtype=torch.bfloat16  # 使用半精度浮点数
)

# 将模型和lora配置结合
config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.2,
    target_modules=["q_proj", "k_proj", "v_proj", "fc1", "fc2"]
)
model = get_peft_model(model, config)
model = model.to(device)

# 数据集处理
dataset_dir = os.path.join(BASEDIR, "train_TCG/train.jsonl")
print(dataset_dir)

def process(data):
    MAX_LENGTH = 384
    input_ids, attention_mask, labels = [], [], []
    instruction = tokenizer(
        f"<| im_start |>system\n{data['instruction']}<| im_end |>\n <| im_start |>user\n {data['input']} <| im_end |>\n<| im_start |>assistant\n",
        add_special_tokens=False,
        padding=True,
        truncation=True
    )
    response = tokenizer(f"{data['output']} <| im_end |>", add_special_tokens=False)
    input_ids = instruction['input_ids'] + response['input_ids'] + [tokenizer.pad_token_id]
    attention_mask = instruction['attention_mask'] + response['attention_mask'] + [1]
    labels = [-100] * len(instruction["input_ids"]) + response["input_ids"] + [tokenizer.pad_token_id]

    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels
    }

# 加载数据集
datadf = pd.read_json(dataset_dir, lines=True)
datads = Dataset.from_pandas(datadf)
train_data = datads.map(
    process,
    remove_columns=datads.column_names
)

# 加载训练器
args = TrainingArguments(
    output_dir='./output_dir',
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    logging_steps=10,
    num_train_epochs=2,
    save_steps=100,
    learning_rate=1e-4,
    save_on_each_node=True,
    gradient_checkpointing=True,
    report_to="none",
    remove_unused_columns=False,
    no_cuda=False,
    dataloader_drop_last=True  # 确保每个进程的数据可均分
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_data,
    data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer, padding=True)
)

# 训练模型
trainer.train()

# 结束时清理分布式环境
dist.destroy_process_group()
