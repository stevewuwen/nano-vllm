import os
from dataclasses import dataclass
from transformers import AutoConfig


@dataclass
class Config:
    model: str # 模型的位置，包含模型的配置、权重、分词器、词汇表
    max_num_batched_tokens: int = 16384 # gpu在一个batch里面能够处理的最大token数目，是所有序列token的累加
    max_num_seqs: int = 512 # 推理系统可以同时处理的最大序列请求
    max_model_len: int = 4096 # 模型能够处理单个序列的最大长度
    gpu_memory_utilization: float = 0.9
    tensor_parallel_size: int = 1
    enforce_eager: bool = False
    hf_config: AutoConfig | None = None # 获取模型的架构信息，如层数、隐藏层
    eos: int = -1
    kvcache_block_size: int = 256 # kvcache缓存块的大小，表示一个block可以装256个kvcache块
    num_kvcache_blocks: int = -1

    def __post_init__(self):
        assert os.path.isdir(self.model)
        assert self.kvcache_block_size % 256 == 0
        assert 1 <= self.tensor_parallel_size <= 8
        self.hf_config = AutoConfig.from_pretrained(self.model)
        self.max_model_len = min(self.max_model_len, self.hf_config.max_position_embeddings)
        assert self.max_num_batched_tokens >= self.max_model_len
