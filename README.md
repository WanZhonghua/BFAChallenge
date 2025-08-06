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
