# jarvis


Too many project has the same call name "jarvis", I will find another name latter.

This repository contains a few different projects. 

1. chatbot 
    A simple chatbot with a bit of AI and a bit of learnning.
    Well, this is actually not AI yet
    use webhook of facebook and line

    1.1. Stack

    * Very high level view: Input(String) --> (AI) --> Output(String)
      ** A bit more detail: http://www.5233.space/2017/06/chatbot.html
    * IM: LINE account + LINE Webhook (to AWS API Gateway)
    * Computing: All in Lambda
    * Data: dynamodb for user information, conversation log and even register
    * Data: elasticsearch for KB (knowledge Base)
       ** conversation KB: learn from conversation
       ** Books: parse EBook 
    * Scheduler: cloudwatch

    1.2. How to join

    * clone this repository
    * have a linux box and setup (a) AWS cli (b) python3 and pip3 
    * have a LINE account
    * 
 
2. socalbrainTest
    * some testing script on chinese message interpertor

3. talentAnalysis
    * A tool to analysis AD
