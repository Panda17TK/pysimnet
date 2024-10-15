# tests/test_node.py

import unittest
from node import Node
from packet import Packet

class TestNode(unittest.TestCase):
    """
    Nodeクラスのユニットテストクラス
    """

    def setUp(self):
        """
        各テストメソッドの前に実行されるセットアップメソッド
        """
        self.node = Node(node_id=1, buffer_size=3000)

    def test_enqueue_packet(self):
        """
        enqueue_packetメソッドのテスト
        """
        packet = Packet(packet_id=1, flow_id=1, size=1500)
        result = self.node.enqueue_packet(packet)
        self.assertTrue(result)
        self.assertEqual(len(self.node.buffer), 1)
        self.assertEqual(self.node.buffer_occupancy, 1500)

        # バッファサイズを超えるパケットを追加
        large_packet = Packet(packet_id=2, flow_id=1, size=2000)
        result = self.node.enqueue_packet(large_packet)
        self.assertFalse(result)
        self.assertEqual(len(self.node.buffer), 1)  # 変化なし

    def test_dequeue_packet(self):
        """
        dequeue_packetメソッドのテスト
        """
        packet = Packet(packet_id=1, flow_id=1, size=1500)
        self.node.enqueue_packet(packet)
        dequeued_packet = self.node.dequeue_packet()
        self.assertEqual(dequeued_packet, packet)
        self.assertEqual(len(self.node.buffer), 0)
        self.assertEqual(self.node.buffer_occupancy, 0)

        # バッファが空の場合
        dequeued_none = self.node.dequeue_packet()
        self.assertIsNone(dequeued_none)

if __name__ == '__main__':
    unittest.main()
