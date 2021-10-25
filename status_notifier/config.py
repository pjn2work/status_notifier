
# Slack channel to notify (only when comes down or up)
slack_notify_urls = {"Myself": "https://hooks.slack.com/services/YourIdTokenHere"}


# Proxies to use
wan_proxies = {
    "http": "http://my.http.proxy:8080",
    "https": "https://my.https.proxy:8080"
}


# HTTP Services to monitor
services_list = {
    "Service 1": {
        "url": "http://localhost:9722/status",
        "proxies": None,
        "status": 200,
        "is_up": True
    }
}


# Other definitions
pulling_interval_sec = 1*60
log_filename = "notify_output.txt"
log_level = "DEBUG"
