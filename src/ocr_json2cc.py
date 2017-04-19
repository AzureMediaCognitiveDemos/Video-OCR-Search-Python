#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
import json


def empty(s):
    return False if (s and not s.isspace()) else True

def get_if_key_exist(obj,key):
    return obj[key] if obj.has_key(key) else ''

def sec2timefmt(int_sec):
    h= int_sec / 3600
    m= (int_sec % 3600)/60
    s= int_sec % 60
    return '%02d:%02d:%02d' % (h,m,s)

def remove_dup_items_in_list(li):
    li_uniq = []
    for x in li:
        if x not in li_uniq:
            li_uniq.append(x)
    return li_uniq

def print_simple(fragments):
    for frag in fragments:
        frag.print_fragment_simple()

def print_webvtt (fragments):
    print "WEBVTT"
    print "NOTE\n"
    for frag in fragments:
        frag.print_fragment_webvtt()
        
def usage(c):
    print 'Usage: # python %s <jsonfile> <outmode>' % c
    print 'outmode : 0 - simple text, 1 - vtt'

class Fragment:
    def __init__(self,js,timescale):
        self.__start = get_if_key_exist(js,'start')
        self.__timescale = timescale
        self.__duration = get_if_key_exist(js,'duration')
        self.__interval = get_if_key_exist(js,'interval')
        self.__texts = []
        events_js =  get_if_key_exist(js,'events')
        if isinstance(self.__start, (int, long)) and events_js:
            for event_js in events_js:
                self.__parse_event__(event_js)

    def __parse_event__(self, event_js):
        if not event_js:
            return
        for rs_js in event_js:
            lang= get_if_key_exist(rs_js,'language')
            t = get_if_key_exist(rs_js,'text')
            #print "debug t={0}".format(t.encode('utf8'))
            t = t.replace(' ', '') #strip space
            if not empty(t):
                self.__texts.append(t)

    def __get_time_in_sec(self, intval):
        return intval / int(self.__timescale)

    def __get_time_in_timefmt(self,intval):
        return sec2timefmt(self.__get_time_in_sec(intval))

    def get_start_in_sec(self):
        return int(self.__start) /int( self.__timescale)

    def get_start_in_timefmt(self):
        return sec2timefmt(self.get_start_in_sec())

    def get_end_in_sec(self):
        return (self.__start + self.__duration ) / self.__timescale
   
    def get_end_in_timefmt(self):
        return sec2timefmt(self.get_end_in_sec())

    def get_texts(self):
        return self.__texts 

    def get_serialized_texts(self):
        texts_uniq = remove_dup_items_in_list(self.__texts)
        return ' | '.join(texts_uniq).encode('utf8')

    def print_fragment_simple(self):
        if len(self.__texts) > 1 and self.__duration != self.__interval:
            start_ticks = int(self.__start)
            end_ticks = start_ticks + int(self.__interval)
            for text in self.__texts:
                print "[{0} - {1}] {2}".format(
                    self.__get_time_in_timefmt(start_ticks),
                    self.__get_time_in_timefmt(end_ticks),
                    text.encode('utf8')) 
                start_ticks = start_ticks + int(self.__interval)
                end_ticks = end_ticks + int(self.__interval)
        else:
            print "[{0} - {1}] {2}".format(
                    self.get_start_in_timefmt(),
                    self.get_end_in_timefmt(),
                    self.get_serialized_texts())

    def print_fragment_webvtt (self):
        if len(self.__texts) > 1 and self.__duration != self.__interval:
            start_ticks = int(self.__start)
            end_ticks = start_ticks + int(self.__interval)
            for text in self.__texts:
                print "{0}.000 --> {1}.000\n{2}\n".format(
                    self.__get_time_in_timefmt(start_ticks),
                    self.__get_time_in_timefmt(end_ticks),
                    text.encode('utf8')) 
                start_ticks = start_ticks + int(self.__interval)
                end_ticks = end_ticks + int(self.__interval)
        else:
            print "{0}.000 --> {1}.000\n{2}\n".format(
                    self.get_start_in_timefmt(),
                    self.get_end_in_timefmt(),
                    self.get_serialized_texts())


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if (argc != 3):
        usage(argvs[0])
        quit()
    jsonfile = argvs[1]
    if ( not str(argvs[2]).isdigit()) or (int(argvs[2]) !=0 and int(argvs[2]) !=1 ):
        usage(argvs[0])
        quit()
    outmode = int(argvs[2])

    frag_list = []
    with open(jsonfile, 'r') as f:
        obj = json.load(f)
        timescale =obj["timescale"]
        frags_js =obj["fragments"]
        for frag_js in frags_js:
            f = Fragment(frag_js,timescale)
            if len(f.get_texts()) > 0:
                frag_list.append(f)
    if ( outmode == 0 ):  # simple
        print_simple(frag_list)
    else: # webvtt or ttml
        print_webvtt(frag_list)
