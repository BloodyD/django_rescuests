# Django Rescuests (RESCued reqUESTS)
This is a simple framework which helps creating external web requests in your Django App. A REST request (currently only GET request) will be send, and if sending was not successfull, it can be retried a defined amount of times.

To track the status of the created request, signals inform your app about success or failure of a request.

## Short Example

```
#somewhere in your app

from rescuests.signals import request_done, request_failed
from django.dispatch import receiver

@receiver(request_done)
def success(sender, instance, response, *args, **kw):
  # handle successfull request

@receiver(request_failed)
def failed(sender, instance, response, error, *args, **kw):
  # handle each single request failure


from rescuests.models import Request
req = Request(url = "https://httpbin.org/get")
req.run() # > will call 'success'

req = Request(url = "https://httpbin.org/status/500")
req.run() # > will call 'failed'
```

## Using django_cron (http://github.com/tivix/django-cron)

```
# settings.py of your project
INSTALLED_APPS = [
  ...
  'rescuests',
  'django_cron',
  ...
]

CRON_CLASSES = [
  "rescuests.cron.SendRequests",
]

# following command will send requests to all existing Request objects, with the status Request.NEW or Request.RETRYING
>> python manage.py runcrons
```
