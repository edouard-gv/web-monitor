from datetime import datetime

import pycurl
import json
import certifi
import requests


WEB_SITES = [("agilenautes", "https://www.agilenautes.com"),
             ("blog_arolla", "https://www.arolla.fr/blog/author/edouard-gomez-vaez/"),
             ("lj", "https://laurencejardin.fr/"),
             ("madm", "https://monanneedemanager.fr/")]

ES = "https://search-monitor-nugnur4dneaojerl2i5p2qsi6y.eu-west-3.es.amazonaws.com/monitor/_doc/"

def main():

    for (shortname, url) in WEB_SITES:
        client_curl = pycurl.Curl()
        client_curl.setopt(pycurl.CAINFO, certifi.where())
        client_curl.setopt(pycurl.URL, url)              #set url
        client_curl.setopt(pycurl.FOLLOWLOCATION, 1)
        client_curl.setopt(pycurl.WRITEFUNCTION, lambda x: None)
        now = datetime.utcnow().isoformat()
        content = client_curl.perform()                        #execute
        dns_time = client_curl.getinfo(pycurl.NAMELOOKUP_TIME) #DNS time
        conn_time = client_curl.getinfo(pycurl.CONNECT_TIME)   #TCP/IP 3-way handshaking time
        starttransfer_time = client_curl.getinfo(pycurl.STARTTRANSFER_TIME)  #time-to-first-byte time
        total_time = client_curl.getinfo(pycurl.TOTAL_TIME)  #last requst time
        client_curl.close()

        data = json.dumps({'dns_time':dns_time,
                           'conn_time':conn_time,
                           'starttransfer_time':starttransfer_time,
                           'total_time':total_time,
                           'url':url,
                           'target':shortname,
                           'time':now})


        print(data)

        headers = {'content-type': 'application/json'}
        response = requests.post(ES, data=data, auth=('monitor', 'xxx'), headers=headers)


        print(response.status_code)
        print(response.content)

if __name__ == "__main__":
    main()