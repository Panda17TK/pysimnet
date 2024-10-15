import unittest
from metrics_collector import MetricsCollector, FlowMetric, NetworkMetric
from flow import Flow
from packet import Packet

class TestMetricsCollector(unittest.TestCase):
    """
    MetricsCollectorクラスのユニットテストクラス
    """

    def setUp(self):
        self.metrics_collector = MetricsCollector()
        # テスト用のフローとパケットを作成
        self.flow = Flow(flow_id=1, service_type='data', flow_size=3000, source_node=1, destination_node=2)
        packet1 = Packet(packet_id=1, flow_id=1, size=1500)
        packet1.sent_time = 0.0
        packet1.arrival_time = 1.0
        packet1.status = "delivered"
        packet2 = Packet(packet_id=2, flow_id=1, size=1500)
        packet2.sent_time = 0.5
        packet2.arrival_time = 1.5
        packet2.status = "delivered"
        self.flow.packets = [packet1, packet2]
        self.flow.start_time = 0.0

    def test_record_flow_metrics(self):
        """
        record_flow_metricsメソッドのテスト
        """
        self.metrics_collector.record_flow_metrics(timestamp=2.0, flow=self.flow)
        self.assertEqual(len(self.metrics_collector.flow_metrics), 1)
        flow_metric = self.metrics_collector.flow_metrics[0]
        self.assertEqual(flow_metric.flow_id, 1)
        self.assertGreater(flow_metric.throughput, 0)
        self.assertGreater(flow_metric.delay, 0)

    def test_record_network_metrics(self):
        """
        record_network_metricsメソッドのテスト
        """
        # まずフローメトリクスを記録
        self.metrics_collector.record_flow_metrics(timestamp=2.0, flow=self.flow)
        # 次にネットワークメトリクスを記録
        self.metrics_collector.record_network_metrics(timestamp=2.0)
        self.assertEqual(len(self.metrics_collector.network_metrics), 1)
        network_metric = self.metrics_collector.network_metrics[0]
        self.assertGreater(network_metric.average_throughput, 0)

if __name__ == '__main__':
    unittest.main()