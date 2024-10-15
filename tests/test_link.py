# tests/test_link.py

import unittest
from link import Link
from packet import Packet

class TestLink(unittest.TestCase):
    """
    Linkクラスのユニットテストクラス
    """

    def setUp(self):
        """
        各テストメソッドの前に実行されるセットアップメソッド
        """
        self.link = Link(link_id=1, capacity=1000.0, delay=0.1, jitter=0.01, connected_nodes=(1, 2))

    def test_transmit_packet(self):
        """
        transmit_packetメソッドのテスト
        """
        packet = Packet(packet_id=1, flow_id=1, size=500)
        result = self.link.transmit_packet(packet)
        self.assertTrue(result)
        self.assertEqual(self.link.current_load, 500)

        # 帯域幅を超えるパケット
        large_packet = Packet(packet_id=2, flow_id=1, size=600)
        result = self.link.transmit_packet(large_packet)
        self.assertFalse(result)
        self.assertEqual(self.link.current_load, 500)  # 変化なし

    def test_fail_and_recover_link(self):
        """
        fail_linkおよびrecover_linkメソッドのテスト
        """
        self.link.fail_link(duration=10.0)
        self.assertEqual(self.link.status, "failed")

        packet = Packet(packet_id=1, flow_id=1, size=500)
        result = self.link.transmit_packet(packet)
        self.assertFalse(result)

        self.link.recover_link()
        self.assertEqual(self.link.status, "active")

        result = self.link.transmit_packet(packet)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
