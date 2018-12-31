from http.server import HTTPServer,BaseHTTPRequestHandler
from os import curdir,sep
import datetime
from crawler import crawl
#from crawler import crawl

class server_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if(self.path.endswith('.html')):
                f=open(curdir + sep + self.path,'rb')
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                print(type(f))
                self.wfile.write(f.read())
                f.close()
                return
            if self.path.endswith('.esp'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                Date=datetime.datetime.now()
                Date=Date.strftime('%m/%d/%Y')
                Message='No Dynamic Content Currently Provided'
                self.wfile.write(bytes(('Message :'+Message+' , '),'utf-8'))
                self.wfile.write(bytes('\n','utf-8'))
                self.wfile.write(bytes(("Today's Date : "+Date),'utf-8'))
                return
            if(self.path.endswith('.csv')):
                f=open(curdir + sep + self.path,'rb')
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                print(type(f))
                self.wfile.write(f.read())
                f.close()
                return
            if(self.path.endswith('.png')):
                f=open(curdir + sep + self.path,'rb')
                self.send_response(200)
                self.send_header('Content-type','image/png')
                self.end_headers()
                print(type(f))
                self.wfile.write(f.read())
                f.close()
                return
        except IOError:
            self.send_error(404,'File Not Found')
def main():
    print('Collecting the data: ')
    print('This may take some time.....................................................')
    crawl()
    print('Analyzing the data ............... Almost there...........')
    import sentiment
    try:
        server=HTTPServer(('',1456),server_handler)
        print('Server Started')
        server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting")
        server.socket.close()


if __name__=='__main__':
    main()

