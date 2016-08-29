import textwrap

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# Define web port
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

# Define app func
class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])


class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))

class WidgetHandler(tornado.web.RequestHandler):
    def get(self, widget_id):
        widget = retrieve_from_db(widget_id)
        self.write(widget.serialize())

    def post(self, widget_id):
        widget = retrieve_from_db(widget_id)
        widget['foo'] = self.get_argument('foo')
        save_to_db(widget)

class FrobHandler(tornado.web.RequestHandler):
    def head(self, frob_id):
        frob = retrieve_from_db(frob_id)
        if frob_id is not None:
            self.set_status(200)
        else:
            self.set_status(404)

    def get(self, frob_id):
        frob = retrieve_from_db(frob_id)
        self.write(frob.serialize())
        
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/reverse/(\w+)", ReverseHandler),
            (r"/wrap", WrapHandler),
            (r"/widget/(\d+)", WidgetHandler),
            (r"/frob/(\d+)", FrobHandler)
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()