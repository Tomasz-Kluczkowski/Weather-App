"""Config file for all pytests
This disables internet connection by default in all tests.
To enable pass in a fixture:
def test_explicitly_enable_socket(socket_enabled):
    assert socket.socket(socket.AF_INET, socket.SOCK_STREAM)

or with a mark
@pytest.mark.enable_socket
def test_explicitly_enable_socket_with_mark():
    assert socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
#
# from pytest_socket import disable_socket
#
# def pytest_runtest_setup():
#     disable_socket()
