from logging import Formatter

from gunicorn.glogging import Logger

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class GunicornLogger(Logger):
    def setup(self, cfg) -> None:
        super().setup(cfg)

        self._set_handler(
            log=self.access_log,
            output=cfg.accesslog,
            fmt=Formatter(fmt=LOG_DEFAULT_FORMAT),
        )
        self._set_handler(
            log=self.error_log,
            output=cfg.errorlog,
            fmt=Formatter(fmt=LOG_DEFAULT_FORMAT),
        )
