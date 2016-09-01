

            Social Media Taiwanese Chatbot

######################################################################

A config-able chat microservice for better customer support.

* Could be a chatbot in facebook page
* Could be a service in your APP

######################################################################

# Project Plan

## analysis customer''s input from text message
- Third pary tool (jeiba)
- sentiment tool (not yet)
- bad language tool (done in basicHandler)
- response text repository <- use csv file and also dynamodb
- take notes   
## Config-able
- response text repository
- 
## a microservice 
- AWS lambda and API gateway
- put knowledge base in elasticsearch
- put log in dynamodb
> msglog (lkey)
- package method
> zip la.zip -r <file> ... <folder> <folder>

# TODOs
- simple api test client (instead of curl)

# Notes
- due to AWS limitation, only python2.7
- python requests is very slow?!

# how to make a Lambda?
- ZIP every thing.
- Check Lambda.py
