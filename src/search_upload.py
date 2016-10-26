#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

config_file = 'search.conf'
api_version = '2015-02-28'

# SS:SS:SS -> # of sec
def get_sec_from_timestr(s):
    arr=s.split(':')
    if len(arr) == 3:
        return str(int(arr[0])* 3600 + int(arr[1])*60 + int(arr[2]) )
    else:
        return "0"

# SS:SS:SS.SSS -> # of sec
def trim_milsec_part(s):
    arr=s.split('.')
    if len(arr)==2:
        return arr[0]
    else:
        return ''

def read_config(s):
    config = {}
    f = open(s)
    line = f.readline().strip()
    while line:
        #print line
        line = f.readline().strip()
        # skip if line start from sharp
        if line[0:1] == '#':
            continue
        arrs=line.split('=')
        if len(arrs) != 2:
            continue
        config[arrs[0]] = arrs[1]
    f.close
    return config

class AzureSearchClient:
    def __init__(self, api_url, api_key, api_version):
        self.api_url=api_url
        self.api_key=api_key
        self.api_version=api_version
        self.headers={
            'Content-Type': "application/json; charset=UTF-8",
            'Api-Key': self.api_key,
            'Accept': "application/json", 'Accept-Charset':"UTF-8"
        }

    def add_documents(self,index_name, documents, merge):
        #raise ConfigError, 'no index_name' if index_name.empty?
        #raise ConfigError, 'no documents' if documents.empty?
        #action = merge ? 'mergeOrUpload' : 'upload'
        action = 'mergeOrUpload' if merge else 'upload'
        for document in documents:
            document['@search.action'] = action
        
        # Create JSON string for request body
        import simplejson as json
        reqobjects={}
        reqobjects['value'] = documents
        from StringIO import StringIO
        io=StringIO()
        json.dump(reqobjects, io)
        req_body = io.getvalue()
        # HTTP request to Azure search REST API
        import httplib
        conn = httplib.HTTPSConnection(self.api_url)
        conn.request("POST",
                "/indexes/{0}/docs/index?api-version={1}".format(index_name, self.api_version),
                req_body, self.headers)
        response = conn.getresponse()
        print "status:", response.status, response.reason
        data = response.read()
        print "data:", data
        conn.close()

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 4):
        print 'Usage: # python %s <webvtt> <contentid> <indexname>' % argvs[0]
        quit()
   
    webvttfile = argvs[1];
    contentid = argvs[2];
    indexname = argvs[3];
    documents = []
    c =0
    docindex=0

    config = read_config(config_file)
    client=AzureSearchClient( 
        "{0}.search.windows.net".format(config["SEARCH_SERVICE_NAME"]),
        config["SEARCH_API_KEY"],
        api_version)

    f = open(webvttfile)
    # skip 1st 3line
    f.readline()
    f.readline()
    line = f.readline()
    while line:
        line = f.readline().strip()
        beginstr= line[0:8]
        endstr= line[17:25]
        ## text
        line = f.readline().strip()
        text = line[0:len(line)]
        # empty line
        line = f.readline()
        document = {
            "id" : "{0}-{1}".format(contentid,str(docindex)),
            "contentid": contentid,
            "beginsec": get_sec_from_timestr(beginstr),
            "begin": beginstr,
            "end": endstr,
            "caption": text
            }
        documents.append(document)
        c +=1
        docindex +=1
        if (c > 999):
            client.add_documents(indexname, documents, 'upload')
            c =0
            documents = []
    f.close
    if (len(documents) > 0):
        client.add_documents(indexname, documents, 'upload')

