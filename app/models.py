class Bot:
    def __init__(self):
        self.__to_do_list = ToDoList()

    def run_command(self, command):

        commands = command.split()

        if commands[0] == 'bot':
            commands = commands[1:]
        else:
            return {'data': 'command not found'}

        if commands[0] == 'ping':
            return self.__ping()

        if commands[0] == 'todo':
            return self.__to_do_list.run_command(commands[1:])

    def __ping(self):
        return {'data': 'pong'}


class ToDoList:
    def __init__(self):
        self.__to_do_list = []

    def run_command(self, commands):
        if commands[0] == 'add':
            return self.add(commands[1:])

        elif commands[0] == 'delete':
            return self.delete(commands[1:])

        elif commands[0] == 'list':
            return self.list()

    def add(self, commands):
        self.__to_do_list.append({'name': commands[0], 'description': commands[1]})
        return {'data': 'todo added'}

    def delete(self, command):
        self.__to_do_list = [x for x in self.__to_do_list if x['name'] != command[0]]
        return {'data': 'todo deleted'}

    def list(self):
        data = '\n'.join(['{} {}'.format(x['name'], x['description']) for x in self.__to_do_list])
        return {'data': data}


class Users:
    def __init__(self):
        self.__user_set = set()

    def add(self, user):
        self.__user_set.add(user)

    def remove(self, ws):
        for user in self.__user_set:
            if user.get_ws() == ws:
                return self.__user_set.remove(user)

    def get_by_ws(self, ws):
        for user in self.__user_set:
            if user.get_ws() == ws:
                return user

    def include(self, ws):
        for user in self.__user_set:
            if user.get_ws() == ws:
                return True

        return False

    def size(self):
        return len(self.__user_set)

    def broadcast_message(self, message):
        for user in self.__user_set:
            user.write_message(message)

    def __iter__(self):
        for user in self.__user_set:
            yield user


class User:
    def __init__(self, ws):
        self.__ws = ws

    def get_ws(self):
        return self.__ws

    def write_message(self, message):
        self.__ws.write_message(message)


