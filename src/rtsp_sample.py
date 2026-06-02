"""以 RTSP 视频流作为输入源驱动测量的示例。

用法：在 src/.env 配置 APP_ID / SDK_KEY / RTSP_URL（及可选 RTSP_FPS）后执行
    python rtsp_sample.py
（需 x86_64 Linux + libmeasurement.so 环境，详见 README「运行环境说明」。）
"""

import logging
from os import getenv
from time import sleep, time

import cv2
from xy_health_measurement_sdk_configuration.protos.Category_pb2 import Anxiety, BloodPressure

from sample import Sample, get_sample_args


class RtspSample(Sample):
    """从 RTSP 网络流读取帧并驱动测量的示例。

    时间戳使用系统时钟（wall-clock），因为网络流内部时钟会在重连时重置。
    通过帧率控制读帧间隔以避免密集获取重复帧。
    """

    def start(self, addr: str, fps: float) -> None:
        """从 RTSP *addr* 读取帧并驱动测量。

        Args:
            addr: RTSP 流地址（如 ``rtsp://user:pass@host:554/stream``）。
            fps: 预期帧率，控制读帧间隔。应 **≤** 实际推流帧率。
        """
        cap, interval = None, 1 / fps
        try:
            cap = cv2.VideoCapture(addr)
            if not cap.isOpened():
                logging.error('Unable to load the %s.', addr)
                return

            success, frame = cap.read()
            if not success:
                logging.error('Unable to read the %s.', addr)
                return
            self._measurement.start(frame)

            while not self._collected:
                ret, frame = cap.read()
                if not ret:
                    break

                # 网络视频流中时间会被不断重置，不能取其中的时间戳
                timestamp = int(time() * 1000)
                # 根据帧率设置采集时间间隔，否则会密集获取重复视频帧
                sleep(interval)
                self._measurement.enqueue(frame, timestamp)

        except Exception as ex:
            logging.critical(ex)
            self.close()
        finally:
            if cap:
                cap.release()


if __name__ == '__main__':
    app_id, sdk_key, config = get_sample_args()
    rtsp = getenv('RTSP_URL', 'rtsp://<user>:<password>@<host>:554/h264/ch1/main/av_stream')
    fps = int(getenv('RTSP_FPS', '25'))  # 需根据实际推流帧率调整，设置帧率应小于等于实际推流帧率

    with RtspSample(app_id, sdk_key, BloodPressure, Anxiety, **config) as sample:
        sample.start(rtsp, fps)

    input("测量中，请勿退出...")
