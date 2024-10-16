import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main
from simulation_engine import SimulationEngine
from topology_manager import TopologyManager
from flow_manager import FlowManager
from central_controller import CentralController
from failure_manager import FailureManager
from metrics_collector import MetricsCollector
from configuration_manager import ConfigurationManager

class TestIntegration(unittest.TestCase):
    """
    システム全体の統合テストクラス
    """

    def test_simulation_run(self):
        """
        シミュレーション全体の実行テスト
        """
        # 設定の読み込み
        config_manager = ConfigurationManager()
        config_manager.load_configuration('data/config.yaml')
        simulation_parameters = config_manager.simulation_parameters

        # シミュレーションエンジンの初期化
        simulation_engine = SimulationEngine()
        simulation_engine.initialize(simulation_parameters['simulation_time'])

        # トポロジの読み込み
        topology_manager = TopologyManager()
        topology_manager.load_topology('data/topology.yaml')

        # 中央コントローラの初期化
        central_controller = CentralController(topology_manager, algorithm=simulation_parameters['algorithm'])

        # メトリクスコレクタの初期化
        metrics_collector = MetricsCollector()

        # フローマネージャの初期化
        flow_manager = FlowManager(topology_manager, simulation_engine, central_controller, metrics_collector)
        flow_manager.generate_flows(flow_scenario='data/config.yaml')

        # フロー開始イベントのスケジュール
        flow_manager.schedule_flow_starts(simulation_engine)

        # 障害マネージャの初期化
        failure_manager = FailureManager(simulation_engine, topology_manager, central_controller)
        failure_manager.schedule_failures(
            failure_rate=simulation_parameters['failure_rate'],
            failure_distribution=simulation_parameters['failure_distribution'],
            simulation_time=simulation_parameters['simulation_time']
        )

        # シミュレーションの実行
        simulation_engine.run()

        # メトリクスの検証
        self.assertGreater(len(metrics_collector.flow_metrics), 0)
        self.assertGreater(len(metrics_collector.network_metrics), 0)

        # メトリクスの値が妥当であることを確認
        for flow_metric in metrics_collector.flow_metrics:
            self.assertGreaterEqual(flow_metric.throughput, 0)
            self.assertGreaterEqual(flow_metric.delay, 0)
            self.assertGreaterEqual(flow_metric.packet_loss_rate, 0)
            self.assertGreaterEqual(flow_metric.jitter, 0)

        for network_metric in metrics_collector.network_metrics:
            self.assertGreaterEqual(network_metric.average_throughput, 0)
            self.assertGreaterEqual(network_metric.average_delay, 0)
            self.assertGreaterEqual(network_metric.average_packet_loss_rate, 0)
            self.assertGreaterEqual(network_metric.average_jitter, 0)

if __name__ == '__main__':
    unittest.main()