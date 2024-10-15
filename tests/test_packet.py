# tests/test_packet.py

import unittest
from packet import Packet

class TestPacket(unittest.TestCase):
    """
    Packetクラスのユニットテストクラス
    """

    def test_packet_initialization(self):
        """
        パケットの初期化テスト
        """
        packet = Packet(packet_id=1, flow_id=1, size=1500)
        self.assertEqual(packet.packet_id, 1)
        self.assertEqual(packet.flow_id, 1)
        self.assertEqual(packet.size, 1500)
        self.assertEqual(packet.route, [])
        self.assertEqual(packet.current_node_index, 0)
        self.assertEqual(packet.status, "in_transit")

if __name__ == '__main__':
    unittest.main()
