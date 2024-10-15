# tests/test_data_exporter.py

import unittest
from data_exporter import DataExporter
from metrics_collector import FlowMetric, NetworkMetric
import os

class TestDataExporter(unittest.TestCase):
    """
    DataExporterクラスのユニットテストクラス
    """

    def setUp(self):
        self.data_exporter = DataExporter()
        self.flow_metrics = [
            FlowMetric(timestamp=1.0, flow_id=1, throughput=1000.0, delay=0.1, packet_loss_rate=0.0, jitter=0.01),
            FlowMetric(timestamp=2.0, flow_id=2, throughput=2000.0, delay=0.2, packet_loss_rate=0.0, jitter=0.02)
        ]
        self.network_metrics = [
            NetworkMetric(timestamp=1.0, average_throughput=1500.0, average_delay=0.15, average_packet_loss_rate=0.0, average_jitter=0.015)
        ]
        self.output_file_path = 'tests/output/metrics'

    def test_export_simulation_data(self):
        """
        export_simulation_dataメソッドのテスト
        """
        # 出力ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(self.output_file_path), exist_ok=True)
        self.data_exporter.export_simulation_data(
            flow_metrics=self.flow_metrics,
            network_metrics=self.network_metrics,
            format='csv',
            file_path=self.output_file_path
        )
        # ファイルが作成されたか確認
        flow_metrics_file = self.output_file_path + '_flow_metrics.csv'
        network_metrics_file = self.output_file_path + '_network_metrics.csv'
        self.assertTrue(os.path.exists(flow_metrics_file))
        self.assertTrue(os.path.exists(network_metrics_file))
        # テスト終了後にファイルを削除
        os.remove(flow_metrics_file)
        os.remove(network_metrics_file)

if __name__ == '__main__':
    unittest.main()
