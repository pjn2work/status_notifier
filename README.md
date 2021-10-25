# Status Notifier App

Python app to notify, via slack channel you choose to be notified, for the status_code change from the URL list you setup to be checked every yy seconds


### On config.py file you must configure your settings:
- Slack channels list to be notified
- Wan proxies - For slack notifications, set it to _None_ if no proxies used
- Services list with:
  - **url**: The http or https url that you want to access and receive the status code from
  - **proxies**: Set it to _None_ if you don't use proxies to access that url
  - **status**: Expected status code received from the url
  - **is_up**: Default is _True_. Set it to _False_ if you want to receive the first notifications that your service is up when launching the app
- Pulling interval (in seconds) - The amount of time to sleep between checks
- Log filename - Location for your log file (make sure you have write access)
- Log level - Default is _DEBUG_


### How to run
```
$ python3 notify_app.py
```