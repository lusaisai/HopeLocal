import threading
import settings
import socket


class Tunnel(threading.Thread):
    def __init__(self, incoming, outgoing):
        super(Tunnel, self).__init__()
        self.incoming = incoming
        self.outgoing = outgoing
        self.logger = settings.logger

    def run(self):
        try:
            while True:
                self.incoming.settimeout(settings.tunnel_timeout)
                data = self.incoming.recv(4096)
                if len(data) == 0:
                    self.close()
                    break
                else:
                    self.outgoing.sendall(data)
        except socket.error:
            self.close()

    def close(self):
        self.incoming.close()
        self.outgoing.close()

    @classmethod
    def tunnelling(cls, s1, s2):
        t1 = cls(s1, s2)
        t1.start()
        t2 = cls(s2, s1)
        t2.start()
        t1.join()
        t2.join()
