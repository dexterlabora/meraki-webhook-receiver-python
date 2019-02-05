## Cisco Meraki Webhook Receiver

A simple example demonstrating how to receive Meraki alerts using webhooks.

## How it works

- Meraki will send a JSON message to this application's POST URL (i.e. http://yourserver/ method=[POST])
- The JSON is checked to ensure it matches the expected secret and version
- The resulting data is sent to the "save_data(data)" function where it can be sent to a databse or other service
  - This example will simply print the POST data to the console.

## Prerequisites

- [Python 3](https://www.python.org/downloads/)
- [Flask](http://flask.pocoo.org/docs/1.0/installation/#installation)
- [Cisco Meraki Network](https://dashboard.meraki.com) with an [HTTP webhook](https://create.meraki.io/guides/webhooks/) server configured for Alerts

* [MongoDB](https://www.mongodb.com/download-center/community)
  - [MAC OSX - Homebrew method](https://gist.github.com/nrollr/9f523ae17ecdbb50311980503409aeb3)

## Installation and Run

```
$ git clone <<this repo>>
```

### Direct Run with Python3

- Option 1 - Basic Receiver

```
meraki-webhook-receiver.py -s <secret>
```

- Option 2 - Receiver with MongoDB

```
python3 meraki-webhook-receiver-mongodb.py -s <secret>
```

### Via Flask

- Option 1 - Basic Receiver

```
export FLASK_APP=meraki-webhook-receiver.py -s <secret>
flask run -h 0.0.0.0
 * Running on http://0.0.0.0:5000/
```

- Option 2 - Receiver with MongoDB

```
export FLASK_APP=meraki-webhook-receiver-mongodb.py -s <secret>
flask run -h 0.0.0.0
 * Running on http://0.0.0.0:5000/
```

## Defaults

- Port: 5000
- Webhook Post URL: http://yourserver:5000/

## TIP

- use ngrok to expose port 5000

```
ngrok http 5000
```

Then use the new url it creates as your base URL. `https://2a6eed03.ngrok.io/`

**Example**

```
$ python3 meraki-webhook-receiver.py -s asdf1234
secret:  asdf1234
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Docs & Tools

[Cisco Meraki Webhook Documentation](https://create.meraki.io/guides/webhooks/)
[Webhook Sample Data - Postman Collection](https://documenter.getpostman.com/view/897512/RWaLwTY4)
[Meraki Developer Portal](https://create.meraki.io)

## Author

Written by Cory Guynn
2019

## License

**Apache**
