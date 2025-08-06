# 🐳 BFAChallenge Docker 使用说明

📂 **项目地址**： [https://github.com/WanZhonghua/BFAChallenge](https://github.com/WanZhonghua/BFAChallenge)

---

## 📦 构建镜像

1. **克隆仓库**
   ```bash
   git clone https://github.com/WanZhonghua/BFAChallenge.git
   cd BFAChallenge
2. **构建 Docker 镜像**
   ```bash
   DOCKER_BUILDKIT=1 sudo docker build -t nimg:v0.8.6 .

## ▶️ 运行容器

1. **设置输入/输出目录**
   ```bash
   input_dir=".../input_data"
   output_dir=".../output_data"
   mkdir -p $output_dir
2. **创建临时卷**
   ```bash
   DOCKER_NOOP_VOLUME="beyondfa_baseline-volume"
   sudo docker volume create "$DOCKER_NOOP_VOLUME" > /dev/null
3. **运行容器**
   ```bash
   sudo docker run \
       -it \
       --platform linux/amd64 \
       --network none \
       --gpus all \
       --rm \
       --volume $input_dir:/input:ro \
       --volume $output_dir:/output \
       --volume "$DOCKER_NOOP_VOLUME":/tmp \
       nimg:v0.8.6

4. **删除临时卷**
   ```bash
   sudo docker volume rm "$DOCKER_NOOP_VOLUME" > /dev/null
