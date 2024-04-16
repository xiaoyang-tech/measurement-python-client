# 小阳心健康测量Python SDK示例客户端

[点击查看](https://measurement.xymind.cn/docs/sdk/python.html)用户手册。

**运行之前需要先在Sample.py中填入许可证（app_id, sdk_key）。**

### 本地运行
```bash
# dependencies installation
pip install -r requirements.txt

# samples
python VideoFileSample.py
python RtspSample.py # 运行该示例需要设置rtsp地址和实际帧率
```

### Docker
```bash
# build
docker build -t xiaoyangtech/measurement-python-client-sample:2.0 .

# execute
docker run -it --rm -v $PWD/src:/app/src xiaoyangtech/measurement-python-client-sample:2.0
```