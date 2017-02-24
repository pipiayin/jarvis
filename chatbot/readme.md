
            Social Media Taiwanese Chatbot

######################################################################

A config-able chat microservice for better customer support.

* Could be a chatbot in facebook page
* Could be a service in your APP

######################################################################

# Project Plan

## analysis customer''s input from text message
- Third pary tool (jeiba)
- sentiment tool (Still TO DO)
- bad language tool (done in basicHandler)
- response text repository <- use csv file and also dynamodb
- take notes   
## Config-able
- response text repository
- a bot-id in header to identify bot webhook 
## a few microservice 
- AWS lambda and API gateway
- put knowledge base in elasticsearch
- put log in dynamodb
> msglog (lkey)
- package method
> zip la.zip -r <file> ... <folder> <folder>

# TODOs
- elasticcache for AI to remember and allow to talk.
- move elasticsearch site to ai (for reduce cost)
- cancel the facebook messager and move to line

# Notes
- due to AWS limitation, only python2.7
- request slow and repeating issues: most of the webhook will set timeout! 
  make sure the time consuming workers should run in async way
- How to allow learnning from user?
   (0) a tricky 590590 prefix to force do indexing
   (1) user A ask question "Q1" and SandyAI can not answer
   (2) 
       * SandyAI then ask user B?
       * SandyAI then ask back user A?
- add books
# how to make a Lambda?
- ZIP every thing.
- check deployToAWS_AITS.sh


# Create Bot Ann
** name botann
** a stranger from original SandyAI request for new bot
steps

<TBD>
