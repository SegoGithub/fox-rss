import http.server
import socketserver
import schedule
import time
import fox

class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/rss.xml":
            self.send_response(200)
            self.send_header("Content-type", "application/xml")
            self.end_headers()
            with open("rss.xml", "rb") as f:
                self.wfile.write(f.read())
        elif self.path == "/atom.xml":
            self.send_response(200)
            self.send_header("Content-type", "application/xml")
            self.end_headers()
            with open("atom.xml", "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("page", "r+", encoding="utf-8") as f:
                page = int(f.read())

            html = f"""<!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8"> 
            <title>OnlyFox - RSS Feed of Foxes 🦊</title>
            <link rel='stylesheet' href='https://cdn.simplecss.org/simple.min.css'>
            </head>
            <body>
            <div style='text-align:center'>
            <h2>OnlyFox - RSS Feed of Foxes 🦊</h2>
            RSS: <a href='https://fox.sego.app/rss.xml'>https://fox.sego.app/rss.xml</a> <br>
            ATOM: <a href='https://fox.sego.app/atom.xml'>https://fox.sego.app/atom.xml</a> <br>
            Source: <a href='https://github.com/SegoGithub/fox-rss'>https://github.com/SegoGithub/fox-rss</a> <br>
            Powered by: <a href='https://github.com/YuaFox/lynx-iberian'>https://github.com/YuaFox/lynx-iberian</a>
            <h3>Currently on page</h3>
            <h1>{page}</h1>
            <img src="https://validator.w3.org/feed/images/valid-rss-rogers.png" alt="This is a valid RSS feed.">
            <img src="https://validator.w3.org/feed/images/valid-atom.png" alt="This is a valid Atom 1.0 feed.">
            </div>
            </body>
            </html>
            """

            self.wfile.write(bytes(html, "utf8"))

            return

def update_rss():
    import fox

schedule.every().day.do(update_rss)

handler_object = HttpRequestHandler

PORT = 443
my_server = socketserver.TCPServer(("", PORT), handler_object)

my_server.serve_forever()