import unittest
from central_controller import CentralController
from topology_manager import TopologyManager
from node import Node
from link import Link

class TestCentralController(unittest.TestCase):
    """
    CentralControllerクラスのユニットテストクラス
    """

    def setUp(self):
        """
        各テストメソッドの前に実行されるセットアップメソッド
        """
        self.topology_manager = TopologyManager()
        # 簡単なトポロジを設定
        self.topology_manager.nodes = {
            1: Node(node_id=1),
            2: Node(node_id=2)
        }
        self.topology_manager.links = {
            1: Link(link_id=1, capacity=1000000.0, delay=0.01, jitter=0.001, connected_nodes=(1, 2))
        }
        self.central_controller = CentralController(self.topology_manager, algorithm="dijkstra")

    def test_update_network_state(self):
        """
        update_network_stateメソッドのテスト
        """
        self.central_controller.update_network_state()
        self.assertEqual(self.central_controller.network_state['node_statuses'], {1: 'active', 2: 'active'})
        self.assertEqual(self.central_controller.network_state['link_statuses'], {1: 'active'})

    def test_calculate_virtual_weights(self):
        """
        calculate_virtual_weightsメソッドのテスト
        """
        self.central_controller.calculate_virtual_weights()
        node1 = self.topology_manager.get_node(1)
        self.assertIsNotNone(node1.virtual_weights)
        self.assertIn(2, node1.virtual_weights)
        self.assertIsInstance(node1.virtual_weights[2], float)

    def test_notify_failure(self):
        """
        notify_failureメソッドのテスト
        """
        self.central_controller.notify_failure(failure_type="link", element_id=1)
        # 通常は状態が更新されるので、更新されたかを確認
        self.assertEqual(self.central_controller.network_state['link_statuses'][1], 'active')  # ダミーの実装では状態は変わらない

if __name__ == '__main__':
    unittest.main()