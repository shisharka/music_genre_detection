import tornado.ioloop
import tornado.web
import os


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('app/index.html')

app = tornado.web.Application([
    (r'/', MainHandler),
    (r'/app/(.*)', tornado.web.StaticFileHandler, {
        'path': 'app'
    }),
    (r'/uploads/(.*)', tornado.web.StaticFileHandler, {
        'path': 'uploads'
    }),
], debug=True)

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()