# tests/test_visualization_interface.py

import unittest
from visualization_interface import VisualizationInterface
from metrics_collector import MetricsCollector, FlowMetric
import pandas as pd

class TestVisualizationInterface(unittest.TestCase):
    """
    VisualizationInterfaceクラスのユニットテストクラス
    """

    def setUp(self):
        self.visualization_interface = VisualizationInterface()
        self.metrics_collector = MetricsCollector()
        # ダミーのフローメトリクスを作成
        self.metrics_collector.flow_metrics = [
            FlowMetric(timestamp=1.0, flow_id=1, throughput=1000.0, delay=0.1, packet_loss_rate=0.0, jitter=0.01),
            FlowMetric(timestamp=2.0, flow_id=2, throughput=2000.0, delay=0.2, packet_loss_rate=0.0, jitter=0.02)
        ]

    def test_update_visualization(self):
        """
        update_visualizationメソッドのテスト
        """
        # このテストでは例外が発生しないことを確認
        try:
            self.visualization_interface.update_visualization(self.metrics_collector)
            result = True
        except Exception as e:
            result = False
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
