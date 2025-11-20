# 小阳心健康测量Python SDK示例客户端

> [用户手册](https://measurement.xymind.cn/docs/sdk/python.html)

## 运行环境说明

**运行之前需要先在`src/.env`中填入许可证（app_id, sdk_key）。**

自SDK >=2.2 版本起引入了部分C++库，这些库对OS环境和其自身依赖包可能存在较为严格的版本要求。

### 本地运行

如需本体环境调试，推荐版本如下：

- 运行平台
  - OS: Ubuntu 22.04 +
  - CPU: x86_64
- 依赖包
  - google protobuf 3.19.6
  - opencv 4.5.4

推荐使用本地Conda解释器。

```bash
# 初始化运行环境
conda create -n measurement_client -y python=3.10 && \
conda activate measurement_client && \
conda install -y -c conda-forge libstdcxx-ng && \
pip install -r requirements.txt

# 运行示例
python VideoFileSample.py
# python RtspSample.py # 运行该示例需要设置rtsp地址和实际帧率
```

### Docker运行

当前SDK运行环境也提供了Docker镜像，具体用法如下：

```bash
# 构建镜像
docker build --platform linux/amd64 -t xiaoyangtech/measurement-python-client-sample:latest .
# 运行容器
docker run -it --rm \
  -v ./src/.env:/app/.env \
  --platform linux/amd64 \
  xiaoyangtech/measurement-python-client-sample:latest
```