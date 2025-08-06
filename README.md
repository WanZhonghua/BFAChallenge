# 🐳 BFAChallenge Docker 使用说明

## 📦 构建镜像

1. **克隆仓库**
   ```bash
   git clone <repository_url>
   cd <repository_name>
构建 Docker 镜像

bash
复制
编辑
DOCKER_BUILDKIT=1 sudo docker build -t nimg:v0.8.6 .
💡 说明
镜像运行时会执行 scripts/entrypoint.sh 中的代码。

▶️ 运行容器
设置输入/输出目录

bash
复制
编辑
input_dir=".../input_data"
output_dir=".../output_data"

mkdir -p $output_dir
创建临时卷

bash
复制
编辑
DOCKER_NOOP_VOLUME="beyondfa_baseline-volume"
sudo docker volume create "$DOCKER_NOOP_VOLUME" > /dev/null
运行容器

bash
复制
编辑
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
删除临时卷

bash
复制
编辑
sudo docker volume rm "$DOCKER_NOOP_VOLUME" > /dev/null
