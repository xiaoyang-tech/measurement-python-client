"""示例程序公共基类。

演示订阅 SDK 事件、驱动测量流程的通用骨架。具体输入源（本地视频 / RTSP 流）
由子类实现 ``start`` 方法。运行需要有效的 ``app_id`` / ``sdk_key`` 及 C++ 动态库
环境，详见仓库 README「运行环境说明」。
"""

import logging
from abc import ABC, abstractmethod
from os import getenv
from typing import Any

from dotenv import load_dotenv

from xy_health_measurement_sdk import Event, Measurement


class Sample(ABC):
    """订阅测量事件并管理测量生命周期的示例基类。

    支持 ``with`` 上下文管理器自动释放资源。
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._measurement = Measurement(*args, **kwargs)
        self._measurement.subscribe(Event.STARTED, self._started_handler)
        self._measurement.subscribe(Event.COLLECTED, self._collected_handler)
        self._measurement.subscribe(
            Event.STATE_UPDATED, self._state_updated_handler)
        self._measurement.subscribe(
            Event.CHUNK_REPORT_GENERATED, self._chunk_report_handler)
        self._measurement.subscribe(
            Event.WHOLE_REPORT_GENERATED, self._whole_report_handler)
        self._measurement.subscribe(
            Event.INTERRUPTED, self._interrupted_handler)
        self._measurement.subscribe(Event.CRASHED, self._exception_handler)

        self._collected = False

    def __enter__(self) -> 'Sample':
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def close(self) -> None:
        """等待测量完成并释放资源。"""
        self._measurement.join()
        self._measurement.stop()

    # ------------------------------------------------------------------
    # 事件处理器
    # ------------------------------------------------------------------

    def _started_handler(self, sender: Any, **kwargs: Any) -> None:
        logging.info('Measurement started: %s', kwargs)

    def _collected_handler(self, sender: Any) -> None:
        self._collected = True

    def _state_updated_handler(self, sender: Any, **kwargs: Any) -> None:
        logging.info('State updated: %s', kwargs)

    def _chunk_report_handler(self, sender: Any, **kwargs: Any) -> None:
        logging.info('Chunk report generated: %s', kwargs)

    def _whole_report_handler(self, sender: Any, **kwargs: Any) -> None:
        logging.info('Whole report generated: %s', kwargs)

    def _interrupted_handler(self, sender: Any) -> None:
        logging.info('Measurement interrupted.')

    def _exception_handler(self, sender: Any, **kwargs: Any) -> None:
        logging.error('Measurement error: %s', kwargs.get('msg_cn', kwargs))
        if kwargs.get('level') == 'error':
            self._collected = True
            self.close()

    @abstractmethod
    def start(self, *args: Any, **kwargs: Any) -> None:
        """子类实现：从具体输入源读取视频帧并驱动测量。"""


# ------------------------------------------------------------------
# 环境配置工具
# ------------------------------------------------------------------


def get_sample_args() -> tuple[str, str, dict[str, Any]]:
    """从 ``.env`` 文件加载凭证和 SDK 配置。

    Returns:
        ``(app_id, sdk_key, config)`` 元组，可直接解包传入
        :class:`Sample` 构造函数。

    Raises:
        EnvironmentError: ``APP_ID`` 或 ``SDK_KEY`` 未设置时抛出。
    """
    load_dotenv()
    app_id = getenv('APP_ID', '').strip()
    sdk_key = getenv('SDK_KEY', '').strip()
    if not app_id or not sdk_key:
        raise EnvironmentError(
            'APP_ID and SDK_KEY must be set in the environment or .env file.'
        )

    config: dict[str, Any] = {
        'measurement_duration': int(getenv('MEASUREMENT_DURATION', '30000'))
    }
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d]: %(message)s',
    )
    return app_id, sdk_key, config
