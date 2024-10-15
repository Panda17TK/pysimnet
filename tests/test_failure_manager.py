import unittest
from failure_manager import FailureManager, FailureEvent
from simulation_engine import SimulationEngine
from topology_manager import TopologyManager
from central_controller import CentralController
from node import Node
from link import Link

class TestFailureManager(unittest.TestCase):
    """
    FailureManagerクラスのユニットテストクラス
    """

    def setUp(self):
        self.simulation_engine = SimulationEngine()
        self.simulation_engine.initialize(1000.0)
        self.topology_manager = TopologyManager()
        # 簡単なトポロジを設定
        self.topology_manager.nodes = {
            1: Node(node_id=1),
            2: Node(node_id=2)
        }
        self.topology_manager.links = {
            1: Link(link_id=1, capacity=1000000.0, delay=0.01, jitter=0.001, connected_nodes=(1, 2))
        }
        self.central_controller = CentralController(self.topology_manager)
        self.failure_manager = FailureManager(self.simulation_engine, self.topology_manager, self.central_controller)

    def test_schedule_failures(self):
        """
        schedule_failuresメソッドのテスト
        """
        self.failure_manager.schedule_failures(failure_rate=0.01, failure_distribution="uniform", simulation_time=1000.0)
        self.assertGreater(len(self.failure_manager.failure_events), 0)

    def test_execute_failure(self):
        """
        execute_failureメソッドのテスト
        """
        failure_event = FailureEvent(event_time=100.0, element_type="node", element_id=1, duration=50.0)
        self.failure_manager.execute_failure(failure_event)
        node = self.topology_manager.get_node(1)
        self.assertEqual(node.status, "failed")

    def test_recover_element(self):
        """
        recover_elementメソッドのテスト
        """
        # 障害を発生させる
        failure_event = FailureEvent(event_time=100.0, element_type="node", element_id=1, duration=50.0)
        self.failure_manager.execute_failure(failure_event)
        # 復旧
        self.failure_manager.recover_element(element_type="node", element_id=1)
        node = self.topology_manager.get_node(1)
        self.assertEqual(node.status, "active")

if __name__ == '__main__':
    unittest.main()