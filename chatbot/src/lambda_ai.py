#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from __future__ import print_function 
from socialBrain import SocialBrain
import json
import requests


def lambda_handler(even, context):
    msg = even['msg']
    fbBrain = SocialBrain()
    resp = fbBrain.think(msg)
   
    return {'res':resp}


if __name__ == '__main__':
    import sys

    msg = sys.argv[1]

    # To try from command line
    params={}
    params['msg'] = sys.argv[1]
    print(lambda_handler(params, None))

    
