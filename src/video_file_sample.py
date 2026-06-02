"""以本地视频文件作为输入源驱动测量的示例。

用法：在 src/.env 配置 APP_ID / SDK_KEY 后执行
    python video_file_sample.py
（需 x86_64 Linux + libmeasurement.so 环境，详见 README「运行环境说明」。）
"""

import logging

import cv2

from sample import Sample, get_sample_args


class VideoFileSample(Sample):
    """从本地视频文件读取帧并驱动测量的示例。

    时间戳直接取自视频文件的播放时钟
    （:data:`cv2.CAP_PROP_POS_MSEC`）。
    """

    def start(self, video: str) -> None:
        """从 *video* 读取帧并驱动测量。

        Args:
            video: 视频文件路径（如 ``video.mp4``）。
        """
        cap = None
        try:
            cap = cv2.VideoCapture(video)
            if not cap.isOpened():
                logging.error('Unable to open the %s.', video)
                return

            success, frame = cap.read()
            if not success:
                logging.error('Unable to read the %s.', video)
                return
            self._measurement.start(frame)

            while not self._collected:
                success, frame = cap.read()
                if not success:
                    break
                timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
                self._measurement.enqueue(frame, timestamp)

        except Exception as ex:
            logging.critical(ex)
            self.close()
        finally:
            if cap:
                cap.release()


if __name__ == '__main__':
    app_id, sdk_key, config = get_sample_args()
    with VideoFileSample(app_id, sdk_key, **config) as sample:
        sample.start('video.mp4')

    input("测量中，请勿退出...")
