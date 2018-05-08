# -*- coding: utf-8 -*-

from pylink import TCPLink

class prologix():
    com = None
    host = None
    port = None
    port_tcp = 1234

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.com = TCPLink(host, self.port_tcp)

    def open(self):
        self.com.open()
        self.com.setup()

    def close(self):
        self.com.close()

    def read(self):
        self.select()
        self.com.write('++read eoi')
        return self.com.read()

    def write(self, cmd):
        self.select()
        self.com.write(cmd)

    def select(self):
        self.com.write('++addr %i' % int(self.port))

    def setup(self):
        self.com.write('++mode 1')
        self.com.write('++auto 0')
        # self.com.write('++eos 0')
