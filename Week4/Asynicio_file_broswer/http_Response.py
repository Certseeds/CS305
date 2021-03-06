import os
import mimetypes
import urllib.parse
import html

state_code_msg = {
    404: "Not Found",
    405: "Method Not Allowed"
}


class http_Response(object):
    def __init__(self, root_path):
        self.head_normal = ['HTTP/1.0 200 OK\r\n',
                            'Connection: close\r\n',
                            'Cache-Control: no-cache\r\n'
                            'Server: nanoseeds\r\n',
                            'Content-Type:text/html',
                            '; charset=utf-8\r\n',
                            '\r\n'
                            ]
        self.body_head = ['<!DOCTYPE html>\r\n',
                          '<html>\r\n',
                          '<head><title>Index of {}</title></head>\r\n',
                          '<body bgcolor="white"> \r\n',
                          '<h1>Index of {}</h1><hr>\r\n ',
                          '<pre>\r\n']
        self.file = []
        self.msg = ''
        self.dir = []
        self.body_default = ['</pre>\r\n ',
                             '<hr> \r\n',
                             '\r\n']
        self.wrong = ['<!DOCTYPE html>\r\n', "<html>\r\n<body>{} {}<body>\r\n</html>\r\n"]
        self.root_path = root_path
        self.body_head[2] = self.body_head[2].format(root_path)
        self.body_head[4] = self.body_head[4].format(root_path)

    def set_headmessage(self, code, msg):
        self.head_normal[0] = 'HTTP/1.0 {} {}\r\n'.format(code, msg)

    def set_state_code_msg(self, code):
        try:
            msg = state_code_msg[code]
        except KeyError:
            msg = "Wrong Code"
        self.wrong[1] = self.wrong[1].format(code, msg)
        self.set_headmessage(code, msg)

    def set_headers(self, name, value):
        if name == 'Content-Type':
            changeline = ''
        else:
            changeline = '\r\n'
        for i in range(len(self.head_normal)):
            if self.head_normal[i].count(':') > 0 and self.head_normal[i].split(':')[0] == name:
                self.head_normal[i] = name + ': ' + value + changeline
                return
        self.head_normal.insert(-1, name + ': ' + value + changeline)

    def get_header(self, name):
        for i in range(len(self.head_normal)):
            if self.head_normal[i].count(':') > 0 and self.head_normal[i].split(':')[0] == name:
                return self.head_normal[i].split(':')[1]
        return ""

    def get_head(self):
        return (get_string(self.head_normal)).encode()

    def get_body(self):
        if self.msg == '':
            return (get_string(self.body_head) + get_string(self.dir) + get_string(self.file) +
                    get_string(self.body_default)).encode()
        else:
            return ((get_string(self.body_head) + get_string(self.dir) + get_string(self.file)).encode() +
                    self.msg + get_string(self.body_default).encode())

    def get_file(self, file_name):
        try:
            file = open(file_name, mode='rb')
        except FileNotFoundError:
            return b'Not Found'
        willreturn = file.read()
        self.set_headers('Content-Length', str(len(willreturn)))
        file.close()
        return willreturn

    def get_wrong(self):
        return get_string(self.wrong).encode()

    def get_response(self):
        return self.get_head() + self.get_body()

    def get_response_wrong(self):
        return self.get_head() + self.get_wrong()

    def fill_file_dir(self, names):
        for i in names:
            if os.path.isfile(i):
                self.file.append("<a href=\"{}\">{}</a><br\r\n>".format(urllib.parse.quote(i), html.escape(i)))
            elif os.path.isdir(i):
                self.dir.append("<a href=\"{}\">{}</a><br\r\n>".format(urllib.parse.quote(i + '/'), html.escape(i + '/')))


def get_string(array):
    willreturn = ""
    for i in array:
        willreturn += str(i)
    return willreturn
