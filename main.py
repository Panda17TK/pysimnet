# main.py

from simulation_engine import SimulationEngine
from topology_manager import TopologyManager
from flow_manager import FlowManager
from packet_manager import PacketManager
from central_controller import CentralController
from failure_manager import FailureManager
from metrics_collector import MetricsCollector
from visualization_interface import VisualizationInterface
from configuration_manager import ConfigurationManager
from data_exporter import DataExporter

def main():
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

    # フローマネージャの初期化
    flow_manager = FlowManager(topology_manager)
    flow_manager.generate_flows()
    flow_manager.packet_manager = PacketManager(topology_manager, simulation_engine)
    flow_manager.packet_manager.flow_manager = flow_manager
    flow_manager.packet_manager.central_controller = central_controller
    flow_manager.packet_manager.metrics_collector = MetricsCollector()

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

    # メトリクスのエクスポート
    data_exporter = DataExporter()
    data_exporter.export_simulation_data(
        flow_metrics=flow_manager.packet_manager.metrics_collector.flow_metrics,
        network_metrics=flow_manager.packet_manager.metrics_collector.network_metrics,
        format='csv',
        file_path='output/metrics'
    )

    # 可視化
    visualization_interface = VisualizationInterface()
    visualization_interface.update_visualization(flow_manager.packet_manager.metrics_collector)

if __name__ == '__main__':
    main()
