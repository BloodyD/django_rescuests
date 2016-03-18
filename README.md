# Django Rescuests (RESCued reqUESTS)
This is a simple framework which helps creating external web requests in your Django App. A REST request (currently only GET request) will be send, and if sending was not successfull, it can be retried a defined amount of times.

To track the status of the created request, signals inform your app about success or failure of a request.
