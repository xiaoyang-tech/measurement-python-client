import logging
from multiprocessing import Value
from ctypes import c_bool
from abc import ABC, abstractmethod
from xy_health_measurement_sdk.Measurement import Measurement


class Sample(ABC):
    def __init__(self, *args, **kwargs):
        self._measurement = Measurement(*args, **kwargs)
        self._measurement.subscribe('started', self._started_handler)
        self._measurement.subscribe('collected', self._collected_handler)
        self._measurement.subscribe('chunk_report_generated', self._chunk_report_handler)
        self._measurement.subscribe('whole_report_generated', self._whole_report_handler)
        self._measurement.subscribe('state_updated', self._state_updated_handler)
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
            self._measurement.stop()

    @property
    def stopped(self):
        with self._stopped.get_lock():
            return self._stopped.value


def get_sample_args():
    config = {
        'logging_config': {
            'level': logging.WARNING,
            'format': '%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d]: %(message)s',
            'filename': 'log.txt',
            'filemode': 'w'
        }
    }
    logging.basicConfig(**config['logging_config'])
    app_id, sdk_key = '3a11e2900a80cc6281f8409b5b103722', '3a11e2900a802476cb35026baff6e3db'
    return app_id, sdk_key, config
