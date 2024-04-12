import cv2
import logging
from Sample import Sample, get_sample_args


class VideoFileSample(Sample):
    def start(self, *args):
        video = args[0]
        cap = None
        try:
            cap = cv2.VideoCapture(video)
            if not cap.isOpened():
                logging.error(f'Unable to open the {video}.')
                return

            success, frame = cap.read()
            if not success:
                logging.error(f'Unable to read the {video}.')
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
        finally:
            if cap:
                cap.release()


if __name__ == '__main__':
    app_id, sdk_key, config = get_sample_args()
    VideoFileSample(app_id, sdk_key, **config).start('resources/video.mp4')

    input("测量中，请勿退出...")
