# Django Rescuests (RESCued reqUESTS)

[![Build Status](https://travis-ci.org/BloodyD/django_rescuests.svg)](https://travis-ci.org/BloodyD/django_rescuests)

This is a simple framework which helps creating external web requests in your Django App. A REST request (currently only GET request) will be send, and if sending was not successfull, it can be retried a defined amount of times.

To track the status of the created request, signals inform your app about success or failure of a request.

## Installation

1. install from pypi or from github
<pre>pip install django-rescuests</pre>
or
<pre>
git clone https://github.com/BloodyD/django_rescuests
cd django_rescuests
pip install -r requirements.txt
python setup.py install
</pre>
2. add <code>django_rescuests</code> to your app:
<pre>
INSTALLED_APPS = [
  ...
  'rescuests',
  ...
]
</pre>
3. run migrations
<pre>
python manage.py migrate rescuests
</pre>

## Short Example

```
# register the signals

from rescuests.signals import request_done, request_failed
from django.dispatch import receiver

@receiver(request_done)
def success(sender, instance, response, *args, **kw):
  # handle successfull request

@receiver(request_failed)
def failed(sender, instance, response, error, *args, **kw):
  # handle each single request failure


# create Requests objects and run them. 
# will send different signals depending on the status code of the response
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

# following command will send requests to all existing Request objects, 
# with the status Request.NEW or Request.RETRYING
>> python manage.py runcrons
```

## Testing your app with Rescuests
For test cases, where your app uses requests you sometimes don't want to send real requests. For this case, Rescuests has a mock context manager. Here is a short example how the manager can be used:

```
import mock # python 2.7 import of mock library
from unittest import mock # python 3 import of the mock library

# somewhere in a test case class
def test_your_app_does_a_request(self):
  inner_func = mock.Mock()
  
  with Request.mock(inner_func):
    request = Request(url = "http://someurl.com")
    request.save()
    request.run()
  
  inner_func.assert_called_with(200, "http://someurl.com")
  
def test_your_app_does_a_bad_request(self):
  inner_func = mock.Mock()
  
  with Request.mock(inner_func):
    request = Request(url = "http://someurl.com", status = 404)
    request.save()
    request.run()
  
  inner_func.assert_called_with(404, "http://someurl.com")
  
```

With this context manager you can simply test the <code>request_done</code> and <code>request_failed</code> signals and whether your app react properly to these. For more examples, check <code>tests</code> folder and the test cases there.

## Project Structure
```
rescuests
|--- admin.py   > AdminModel for the Request model
|--- cron.py    > Cron job definition
|--- models.py  > Reuest model definition
|--- signals.py > signal definition
```
