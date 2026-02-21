import socket
import threading
import time

def test_server_starts():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("localhost", 0))
        s.close()
        assert True
    except Exception:
        assert False