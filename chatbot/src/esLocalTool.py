#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch, RequestsHttpConnection
from datetime import datetime
import sys
import csv
import argparse
import json
    
    
class EsTool:
    

    def __init__(self, host, port):
        self.host = host 
        self.port = port
        self.es = Elasticsearch(
            hosts=[{'host': host, 'port': int(port)}],
            connection_class=RequestsHttpConnection
        )

    def createIndex(self, indexname):
        self.es.indices.create(index=indexname)
        print(dir(self.es))

    def rebuild(self, indexname,doctype, jsonfile):
        self.es.indices.delete(index=indexname)
        self.es.indices.create(index=indexname)
    
        for line in open(jsonfile):
            s = line.strip()
            toInsert = eval(s)
            res = self.es.index(index=indexname, doc_type=doctype,  body=toInsert)
            print(res)
    
        self.es.indices.refresh(index=indexname)
    
    def delete(self, indexname, docid):
        self.es.delete(index=indexname, id=docid, doc_type='fb')
        self.es.indices.refresh(index=indexname)
    
    def listAll(self, indexname, query=""):
    
        q = {
#            "min_score": 0.0000001,
            "query" :{
              "multi_match" : {
                  "query": query,
                  "fields": [ "pkey", "similar","res" ]
              } 
          },
             "size": 5000
        }
    
    
    #    es.indices.refresh(index=indexname)
        res = self.es.search(index=indexname, body=q)
    #print(res)
        print("Got %d Hits:" % res['hits']['total'])
        for h in res['hits']['hits']:
            print(h['_id']+ " "+ str(h['_source']))
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='elasticsearch tool')
    parser.add_argument('--list','-l', action='store_true', help='list all docs')
    parser.add_argument('--rebuild','-r',action='store_true', help='rebuild index via upload a json file')
    parser.add_argument('--indexname','-i', help='index name')
    parser.add_argument('--query','-q', help='query string')
    parser.add_argument('--jsondump','-j', help='jsondump file name, one line per json doc')
    parser.add_argument('--delete','-d', action='store_true', help='to delete document')
    parser.add_argument('--createIndex','-C', action='store_true', help='to create index')
    parser.add_argument('--docid','-c', help='document _id')
    parser.add_argument('--host','-H', help='elasticsearch host',default='127.0.0.1')
    parser.add_argument('--port','-p', help='elasticsearch host port',default='9200')
    
    args = parser.parse_args()
    esTool = EsTool(args.host, int(args.port))
    
    if args.createIndex:
        print("to create an index")
        esTool.createIndex(args.indexname)

    if args.delete:
        print('to delete a single document')
        delete(args.indexname, args.docid)
    
    if args.list :
        print('list all')
        listAll(args.indexname, args.query)
        exit(0)
    
    if args.rebuild:
        print('rebuild by jsonfile')
        rebuild(args.indexname, args.jsondump)
       
    
    
