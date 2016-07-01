import os
import tornado.ioloop
import tornado.web
import tornado.websocket

from models import *




class IndexHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    def get(self):
        self.render('index.html')


class SendWebSocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, users, bot):
        self.users = users
        self.bot = bot

    def data_received(self, chunk):
        pass

    def open(self):
        self.users.add(User(self))
        print('WebSocket opened')

    def on_message(self, message):
        print(message)
        self.users.broadcast_message({'data': message})
        send_data = self.bot.run_command(message)
        self.users.broadcast_message(send_data)

    def on_close(self):
        print('WebSocket closed')
        self.users.remove(self)


def make_app():
    users = Users()
    bot = Bot()
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/ws', SendWebSocketHandler, dict(users=users, bot=bot)),
    ],
        template_path=os.path.join(os.getcwd(), './app/templates'),
        static_path=os.path.join(os.getcwd(), './app/static'),
    )


if __name__ == '__main__':
    print('start_server')
    app = make_app()
    app.listen(int(os.environ.get("PORT", 5000)))
    tornado.ioloop.IOLoop.current().start()
