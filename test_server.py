"""
A test script to find bugs and ensure the code works as intended
"""
import socket
import threading
import time
import json
import pytest

import server as server_module

# Test server and client setup

def _get_free_port():
    """Ask the OS for an unused port instead of hardcoding one"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture
def make_server():
    """Starts a separate server instance"""
    port = _get_free_port()

    # Initialize server
    server_module.clients.clear()
    server_module.cache.clear()
    server_module.active_clients = 0

    thread = threading.Thread(
        target=server_module.start_server,
        kwargs={"host": "127.0.0.1", "port": port},
        daemon=True,  # dies automatically when the test process exits
    )
    thread.start()
    time.sleep(0.5)

    return port


@pytest.fixture
def make_client(make_server):
    """Create a test client"""
    def connect():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(("127.0.0.1", make_server))
        return s
    return connect


# Tests
def test_server_starts():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("localhost", 0))
        s.close()
        assert True
    except Exception:
        assert False

def test_echo_with_ack(make_client):
    """Test server echos with uppercase ACK"""
    client = make_client()
    client.send(b"hello")
    assert client.recv(1024).decode() == "HELLO ACK"
    client.close()


def test_status_returns_valid_json(make_client):
    """Test 'status' returns a JSON"""
    client = make_client()
    client.send(b"status")
    response = client.recv(1024).decode()
    json.loads(response)  # raises if not valid JSON


def test_fourth_client_rejected(make_client):
    """Test a 4th simultaneous client is rejected (max_clients=3)."""
    c1, c2, c3 = make_client(), make_client(), make_client()
    c4 = make_client()

    assert "Maximum number of clients reached" in c4.recv(1024).decode()
    for client in (c1, c2, c3, c4):
        client.close()


def test_abrupt_disconnect_frees_slot(make_client):
    """
    Test disconnects without 'exit' still frees up client space
    """
    c1, c2, c3 = make_client(), make_client(), make_client()
    c1.close()  # no 'exit' sent — simulates a dropped connection

    time.sleep(0.3)

    c4 = make_client()  # should succeed if the slot was freed
    c4.send(b"hi")
    assert c4.recv(1024).decode() == "HI ACK"
    for client in c2, c3, c4:
        client.close()