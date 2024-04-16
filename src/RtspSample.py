import cv2
import logging
from time import time, sleep
from Sample import Sample, get_sample_args
from xy_health_measurement_sdk.protos.Category_pb2 import BloodPressure, Anxiety


class RtspSample(Sample):
    def start(self, *args):
        addr, fps = args
        cap, interval = None, 1 / fps
        try:
            cap = cv2.VideoCapture(addr)
            if not cap.isOpened():
                logging.error(f'Unable to load the {addr}.')
                return

            success, frame = cap.read()
            if not success:
                logging.error(f'Unable to read the {addr}.')
                return
            self._measurement.start(frame)

            while not self._collected and not self.stopped:
                ret, frame = cap.read()
                if not ret:
                    break

                timestamp = int(time() * 1000)  # 网络视频流中时间会被不断重置，不能取其中的时间戳
                sleep(interval)  # 根据帧率设置采集时间间隔，否则会密集获取重复视频帧
                self._measurement.enqueue(frame, timestamp)

        except Exception as ex:
            logging.critical(ex)
        finally:
            if cap:
                cap.release()


if __name__ == '__main__':
    app_id, sdk_key, config = get_sample_args()
    rtsp = 'rtsp://'
    fps = 25  # 假定帧率为25（需根据实际推流帧率调整，设置帧率应小于等于实际推流帧率）
    sample = RtspSample(app_id, sdk_key, BloodPressure, Anxiety, **config)
    sample.start(rtsp, fps)

    # input("测量中，请勿退出...")
    while not sample.stopped:
        sleep(0.2)
    print('all done')
