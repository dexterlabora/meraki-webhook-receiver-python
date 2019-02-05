#!flask/bin/python

"""
Cisco Meraki Webhook Receiver

A simple example demonstrating how to receive Meraki alerts using webhooks.

How it works:
- 
- Meraki will then send a JSON message to this application's POST URL (i.e. http://yourserver/ method=[POST])
- The JSON is checked to ensure it matches the expected secret and version
- The resulting data is sent to the "save_data(data)" function where it can be sent to a databse or other service
    - This example will simply print the POST data to the console.

Default port: 5000

[Cisco Meraki Webhook Documentation](https://create.meraki.io/guides/webhooks/)
[Webhook Sample Data - Postman Collection](https://documenter.getpostman.com/view/897512/RWaLwTY4)

Written by Cory Guynn
2019

www.meraki.io
"""

# Libraries
from pprint import pprint
from flask import Flask
from flask import json
from flask import request
import sys, getopt
from pymongo import MongoClient

############## USER DEFINED SETTINGS ###############
# MERAKI SETTINGS
shared_secret = "yourSharedSecret" # or provied with the ` -s yourSharedSecret` argument
db = "test"
version = "0.1" #This code was written to support the Webhook Alert JSON version specified

# Save Webhook Alert Data
# Save CMX Data
def save_data(data):
    print("---- SAVING Webhook DATA ----")
    # CHANGE ME - send 'data' to a database or storage system
    pprint(data, indent=1)

    # Commit to database
    client = MongoClient("mongodb://localhost:27017")
    db = client.test
    result = db.alerts.insert_one(data)
    print("MongoDB insert result: ",result )


####################################################
app = Flask(__name__)

# Respond to Meraki with validator
@app.route('/', methods=['GET'])
def get_home():
    print("validator sent to: ",request.environ['REMOTE_ADDR'])
    return "Meraki Webhook Receiver is Online"

# Accept CMX JSON POST
@app.route('/', methods=['POST'])
def post_webhook_data():
    #if not request.json or not 'data' in request.json:
        #return("invalid data",400)
    webhook_data = request.json
    #pprint(webhook_data, indent=1)
    print("Received POST from ",request.environ['REMOTE_ADDR'])

    # Verify secret
    if webhook_data['sharedSecret'] != shared_secret:
        print("secret invalid:", webhook_data['sharedSecret'], shared_secret)
        return("invalid secret",403)
    else:
        print("secret verified: ", webhook_data['sharedSecret'])

    # Verify version
    if webhook_data['version'] != version:
        print("invalid version")
        return("invalid version",400)
    else:
        print("version verified: ", webhook_data['version'])

   
    # Do something with data (commit to database)
    save_data(webhook_data)

    # Return success message
    return ("Meraki Webhook Alert POST Received", 201)


# Launch application with supplied arguments

def main(argv):
    global shared_secret

    try:
       opts, args = getopt.getopt(argv,"h:s:",["secret="])
    except getopt.GetoptError:
       print("meraki-webhook-receiver.py -s <secret>")
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
           print("meraki-webhook-receiver.py -s <secret>")
           sys.exit()
       elif opt in ("-s", "--secret"):
           shared_secret = arg
    print ('secret: ', shared_secret)


if __name__ == '__main__':
    main(sys.argv[1:])
    app.run(port=5000,debug=False)
