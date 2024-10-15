import sys
import os
import unittest
from unittest.mock import patch, mock_open
import yaml

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

    @patch('builtins.open')
    def test_generate_flows_from_scenario(self, mock_open_function):
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
        # モックされたファイルの内容を設定
        mock_open_function.return_value.__enter__.return_value = \
            yaml.dump(flow_scenario, default_flow_style=False)

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