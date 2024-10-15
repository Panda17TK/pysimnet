# tests/test_flow_manager.py

import unittest
from flow_manager import FlowManager
from topology_manager import TopologyManager
from flow import Flow

class TestFlowManager(unittest.TestCase):
    """
    FlowManagerクラスのユニットテストクラス
    """

    def setUp(self):
        """
        各テストメソッドの前に実行されるセットアップメソッド
        """
        self.topology_manager = TopologyManager()
        # 簡単なトポロジを設定
        self.topology_manager.nodes = {
            1: None,
            2: None
        }
        self.flow_manager = FlowManager(self.topology_manager)

    def test_generate_flows_random(self):
        """
        generate_flowsメソッドのランダム生成テスト
        """
        self.flow_manager.generate_flows()
        self.assertEqual(len(self.flow_manager.flows), 100)

    def test_generate_flows_from_scenario(self):
        """
        generate_flowsメソッドのシナリオ読み込みテスト
        """
        # テスト用のフローシナリオデータを作成
        flow_scenario = {
            'flows': [
                {
                    'flow_id': 1,
                    'service_type': 'video',
                    'flow_size': 1000000,
                    'source_node': 1,
                    'destination_node': 2
                }
            ]
        }
        # シナリオを読み込むようにモック
        def mock_open(*args, **kwargs):
            from io import StringIO
            return StringIO(yaml.dump(flow_scenario))

        import yaml
        yaml.open = mock_open

        self.flow_manager.generate_flows(flow_scenario='dummy_path')
        self.assertEqual(len(self.flow_manager.flows), 1)
        flow = self.flow_manager.flows[1]
        self.assertEqual(flow.flow_id, 1)
        self.assertEqual(flow.service_type, 'video')
        self.assertEqual(flow.flow_size, 1000000)
        self.assertEqual(flow.source_node, 1)
        self.assertEqual(flow.destination_node, 2)

if __name__ == '__main__':
    unittest.main()
