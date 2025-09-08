FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Install python and dependencies
RUN apt-get update && apt-get install -y \
    git wget curl python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install vLLM (support VLM and OpenAI API server)
RUN pip install --upgrade pip
RUN pip install vllm[all] transformers accelerate

# Install gradio interface
RUN pip install gradio

WORKDIR /app
