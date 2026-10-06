import asyncio
import socket
import types
from contextlib import contextmanager
import runpy
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

MODULE = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'server.py'))

@contextmanager
def socket_factory(sock=None):
    factory = MagicMock(return_value=sock) if sock is not None else MagicMock()
    fake = types.SimpleNamespace(socket=factory, AF_INET=socket.AF_INET,
                                 SOCK_STREAM=socket.SOCK_STREAM, timeout=socket.timeout)
    with patch.dict(MODULE['_irc_cmd'].__globals__, {'socket': fake}):
        yield factory

class CommandTests(unittest.TestCase):
    def test_line_breaks_rejected_before_socket_creation(self):
        for name, args in [('msg', ('peer', 'hello\n/quit')), ('msg', ('peer\r/quit', 'hello')), ('search', ('term\n/quit',)), ('verify', ('peer\r/quit',)), ('quant', ('seed\n/quit',))]:
            with self.subTest(name=name, args=args), socket_factory() as factory:
                factory.return_value.recv.return_value = b""
                with self.assertRaises(ValueError):
                    asyncio.run(MODULE[name](*args))
                factory.assert_not_called()

    def test_valid_message_is_one_command_and_socket_closes(self):
        sock = MagicMock()
        sock.__enter__.return_value = sock
        sock.recv.side_effect = [b'banner\n', b'accepted\n', b'']
        with socket_factory(sock):
            self.assertEqual(asyncio.run(MODULE['msg']('peer', 'hello world')), 'accepted')
        sock.sendall.assert_called_once_with(b'/msg peer hello world\n')
        sock.__exit__.assert_called_once()

    def test_socket_closes_on_connect_error(self):
        sock = MagicMock()
        sock.__enter__.return_value = sock
        sock.connect.side_effect = OSError('synthetic failure')
        with socket_factory(sock):
            self.assertIn('synthetic failure', MODULE['_irc_cmd']('/rooms'))
        sock.__exit__.assert_called_once()

if __name__ == '__main__':
    unittest.main()
