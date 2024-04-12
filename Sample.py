import logging
from abc import ABC, abstractmethod
from xy_health_measurement_sdk.Measurement import Measurement


class Sample(ABC):
    def __init__(self, *args, **kwargs):
        self._measurement = Measurement(*args, **kwargs)
        self._measurement.subscribe('started', self._started_handler)
        self._measurement.subscribe('collected', self._collected_handler)
        self._measurement.subscribe('chunk_report_generated', self._chunk_report_handler)
        self._measurement.subscribe('whole_report_generated', self._whole_report_handler)
        self._measurement.subscribe('crashed', self._exception_handler)

        self._collected = False

    def _started_handler(self, sender, **kwargs):
        print(kwargs)

    def _collected_handler(self, sender):
        self._collected = True

    def _chunk_report_handler(self, sender, **kwargs):
        print(kwargs)

    def _whole_report_handler(self, sender, **kwargs):
        print(kwargs)

    def _exception_handler(self, sender, **kwargs):
        print(kwargs['msg_cn'])
        if kwargs['level'] == 'error':
            self._collected_handler(self)
            self._measurement.stop()

    @abstractmethod
    def start(self, *args):
        pass


def get_sample_args():
    config = {
        'logging_config': {
            'level': logging.DEBUG,
            'format': '%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d]: %(message)s',
            'filename': 'log.txt',
            'filemode': 'w'
        }
    }
    logging.basicConfig(**config['logging_config'])
    app_id, sdk_key = '', ''
    return app_id, sdk_key, config
