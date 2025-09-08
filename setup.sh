# build image 
docker build -t qwen-vllm .

# Run vLLM server 
docker run --gpus all -it --rm \
  -p 8000:8000 \
  -v /data/models:/models \ 
  qwen-vllm \
  python3 -m vllm.entrypoints.openai.api_server \
    --model /models/Qwen2.5-VL-30B-Instruct \
    --port 8000 \
    --host 0.0.0.0 \
    --max-num-seqs 16 \
    --tensor-parallel-size 2
