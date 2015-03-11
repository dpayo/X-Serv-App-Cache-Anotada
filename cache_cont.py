#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Ejercicio 9.6 Cache de contenidos
    http://localhost:1234/url/recurso
    recursos: reload  cache   header
"""
import webapp
import urllib
import urllib2
import sys

class proxyApp(webapp.webApp):
    cache ={}
    cabecera_nav={}
    def parse(self, request):
        """Parse the received request, extracting the relevant information.

        request: HTTP request received from the client
        rest:    rest of the resource name after stripping the prefix
        """
        recurso = request.split(' ')[1].split('/')
        cabecera= request.split('\r\n')[1:]
        url= ""
        
        if len(recurso) == 2:
            url= recurso[1]
            recurso=""
        elif len(recurso)== 3:
            url= recurso[1]
            recurso = recurso[2]
       
        return (url,recurso,cabecera)

    def process(self, (url,recurso,cabecera)):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """
        
        if recurso == "":
            try:
                request= urllib2.urlopen('http://'+url)    
                html= request.read()
                self.cabecera_serv= request.info()
                self.cache[url]= html
                pos=html.find('<body')
                html_1=html[pos:]
                pos_1= html_1.find('>')
                res=html_1[:pos_1+1]+"<a href=http://"+url+"><p style= text-align:center><font size=4> Original webpage</font> </a>"+"<a href=http://localhost:1234/"+url+"/reload ><p style= text-align:center><font size=4> Reload </font> </a>"+"<a href=http://localhost:1234/"+url+"/cache ><p style= text-align:center><font size=4>Cache</font> </a>"+"<a href=http://localhost:1234/"+url+"/header ><p style= text-align:center><font size=4> Headers </font> </a>"+html
                code = "200 OK"
            except:
                code="404"
                res="Not Found"
        elif recurso == "header":
               try:
                code = "200 Ok"
                res= "<h1> HTTP enviado por el navegador: </h1>"+str(cabecera)+"<h1> HTTP de respuesta del servidor : </h1>"+str(self.cabecera_serv)
               except AttributeError:
                code= "404 "
                res= "Not Found"
        elif recurso== "cache":
            if url in self.cache:
                code = "200 Ok"
                res= self.cache[url]
            else:
                code = "404"
                res= "<h1>Error... No se encuentra en la cache"
        elif recurso =="reload":
           request= urllib.urlopen('http://'+url)    
           res= request.read()
           code= "200 OK"
        else:
            code= "404"
            res= "<h1>Not found"
        return (code, res)
                      
if __name__ == "__main__":
    try:
        testWebApp = proxyApp("localhost", 1234)
    except KeyboardInterrupt:
        print "KeyboardInterrupt"
        sys.exit()
