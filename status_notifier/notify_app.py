import requests
import logging

from time import sleep
from datetime import datetime, timedelta

from config import slack_notify_urls, wan_proxies, services_list, \
    pulling_interval_sec, log_filename, log_level


# Setup log file
logging.basicConfig(filename=log_filename,
                    level=log_level,
                    format="%(asctime)s %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

# Remove this modules from logging
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

# My log
log = logging.getLogger(__name__)


class Timer:

    def __init__(self, seconds: float = 0.0, **kwargs):
        self.set_timer_for(seconds=seconds, **kwargs)

    def set_timer_for(self, seconds: float = 0.0, **kwargs):
        self.timer_end = datetime.now() + timedelta(seconds=seconds, **kwargs)
        return self

    def seconds_left(self) -> float:
        tl = (self.timer_end - datetime.now()).total_seconds()
        if tl > 0:
            return tl
        return 0

    def sleep_until_over(self):
        self.sleep_for(self.seconds_left())
        return self

    @staticmethod
    def sleep_for(seconds: float):
        if seconds > 0.0:
            sleep(seconds)


def notify_via_slack(message):
    for channel_name, notify_url in slack_notify_urls.items():
        try:
            requests.post(notify_url, json={"text": message}, proxies=wan_proxies)
        except Exception as ex:
            log.error(f"Can't reach slack channel {channel_name}: {ex}")


def check_service(service, end_point):
    url, status, is_up, proxies = end_point["url"], end_point["status"], end_point["is_up"], end_point["proxies"]

    result = requests.get(url, proxies=proxies)

    assert result.status_code == status, f"Unexpected {result.status_code}, expected {status}"

    if is_up:
        log.debug(f"{service}: Success! (still up)")
    else:
        end_point["is_up"] = True
        log.warning(f"{service}: Success! (back up again)")
        notify_via_slack(f"{service}: Success! (back up again)")


def check_all_services():
    for service, end_point in services_list.items():
        try:
            check_service(service, end_point)
        except Exception as ex:
            if end_point["is_up"]:
                end_point["is_up"] = False
                log.error(f"{service}: Down! {ex}")
                notify_via_slack(f"{service}: Down! {ex}")
            else:
                log.info(f"{service}: Down! (still down) {ex}")


class RunForever:
    def __init__(self):
        self.timer = Timer(pulling_interval_sec)

    def __enter__(self):
        return self

    def run_forever(self):
        while True:
            check_all_services()
            self.timer.sleep_until_over().set_timer_for(pulling_interval_sec)

    def __exit__(self, exc_type, exc_val, exc_tb):
        log.warning("Notifier ended")
        notify_via_slack("Notifier ended")


def run_notify():
    message = f"Running notifier every {pulling_interval_sec}sec for: {list(services_list.keys())}"
    print(message)
    log.info(message)
    notify_via_slack(message)

    with RunForever() as rf:
        rf.run_forever()


if __name__ == "__main__":
    run_notify()
