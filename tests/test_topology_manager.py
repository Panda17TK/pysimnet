# tests/test_topology_manager.py

import unittest
from topology_manager import TopologyManager
from node import Node
from link import Link

class TestTopologyManager(unittest.TestCase):
    """
    TopologyManagerクラスのユニットテストクラス
    """

    def setUp(self):
        """
        各テストメソッドの前に実行されるセットアップメソッド
        """
        self.topology_manager = TopologyManager()

        # テスト用のトポロジデータを直接設定
        self.topology_manager.nodes = {
            1: Node(node_id=1),
            2: Node(node_id=2)
        }
        self.topology_manager.links = {
            1: Link(link_id=1, capacity=1000.0, delay=0.1, jitter=0.01, connected_nodes=(1, 2))
        }
        self.topology_manager.nodes[1].adjacent_links.append(1)
        self.topology_manager.nodes[2].adjacent_links.append(1)

    def test_get_node(self):
        """
        get_nodeメソッドのテスト
        """
        node = self.topology_manager.get_node(1)
        self.assertIsNotNone(node)
        self.assertEqual(node.node_id, 1)

        node_none = self.topology_manager.get_node(3)
        self.assertIsNone(node_none)

    def test_get_link(self):
        """
        get_linkメソッドのテスト
        """
        link = self.topology_manager.get_link(1)
        self.assertIsNotNone(link)
        self.assertEqual(link.link_id, 1)

        link_none = self.topology_manager.get_link(2)
        self.assertIsNone(link_none)

if __name__ == '__main__':
    unittest.main()
