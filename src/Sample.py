import logging
from multiprocessing import Value
from ctypes import c_bool
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from os import getenv
from xy_health_measurement_sdk.Measurement import Measurement


class Sample(ABC):
    def __init__(self, *args, **kwargs):
        self._measurement = Measurement(*args, **kwargs)
        self._measurement.subscribe('started', self._started_handler)
        self._measurement.subscribe('collected', self._collected_handler)
        self._measurement.subscribe('state_updated', self._state_updated_handler)
        self._measurement.subscribe('chunk_report_generated', self._chunk_report_handler)
        self._measurement.subscribe('whole_report_generated', self._whole_report_handler)
        self._measurement.subscribe('crashed', self._exception_handler)

        self._collected = False
        self._stopped = Value(c_bool, False)

    def _started_handler(self, sender, **kwargs):
        print(kwargs)

    def _collected_handler(self, sender):
        self._collected = True

    def _chunk_report_handler(self, sender, **kwargs):
        print(kwargs)

    def _whole_report_handler(self, sender, **kwargs):
        print(kwargs)
        self.stop()

    def _state_updated_handler(self, sender, **kwargs):
        print(kwargs)

    def _exception_handler(self, sender, **kwargs):
        print(kwargs['msg_cn'])
        if kwargs['level'] == 'error':
            self._collected_handler(self)
            self.stop()

    @abstractmethod
    def start(self, *args):
        pass

    def stop(self):
        with self._stopped.get_lock():
            self._stopped.value = True
            self._measurement.join()
            self._measurement.stop()

    @property
    def stopped(self):
        with self._stopped.get_lock():
            return self._stopped.value


def get_sample_args():
    load_dotenv()

    config = {
        'measurement_duration': int( getenv("MEASUREMENT_DURATION", 30000)),
        'logging_config': {
            'level': logging.WARNING,
            'format': '%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d]: %(message)s',
            'filename': 'log.txt',
            'filemode': 'w'
        }
    }
    logging.basicConfig(**config['logging_config'])
    app_id, sdk_key = getenv("APP_ID"), getenv("SDK_KEY")
    return app_id, sdk_key, config
