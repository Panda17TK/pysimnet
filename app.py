# app.py

import streamlit as st
from simulation_engine import SimulationEngine
from topology_manager import TopologyManager
from flow_manager import FlowManager
from central_controller import CentralController
from failure_manager import FailureManager
from metrics_collector import MetricsCollector
from configuration_manager import ConfigurationManager
from data_exporter import DataExporter
from visualization_interface import VisualizationInterface
import threading
import time

def run_simulation(simulation_time, failure_rate, algorithm):
    # 設定の読み込み
    config_manager = ConfigurationManager()
    config_manager.simulation_parameters = {
        'simulation_time': simulation_time,
        'failure_rate': failure_rate,
        'failure_distribution': 'uniform',
        'algorithm': algorithm
    }

    # シミュレーションエンジンの初期化
    simulation_engine = SimulationEngine()
    simulation_engine.initialize(simulation_time)

    # トポロジの読み込み
    topology_manager = TopologyManager()
    topology_manager.load_topology('data/topology.yaml')

    # 中央コントローラの初期化
    central_controller = CentralController(topology_manager, algorithm=algorithm)

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
        failure_rate=failure_rate,
        failure_distribution='uniform',
        simulation_time=simulation_time
    )

    # シミュレーションの実行を別スレッドで開始
    def simulation_thread():
        simulation_engine.run()
        st.success("Simulation completed.")
    
    threading.Thread(target=simulation_thread).start()

    # 可視化の更新
    visualization_interface = VisualizationInterface()

    placeholder = st.empty()
    while simulation_engine.event_queue:
        # メトリクスを収集
        metrics_collector.record_network_metrics(simulation_engine.current_time)
        # 可視化の更新
        with placeholder.container():
            visualization_interface.update_visualization(metrics_collector)
        time.sleep(1)  # 1秒ごとに更新

    # シミュレーション終了後の最終的なメトリクス表示
    visualization_interface.update_visualization(metrics_collector)

    # メトリクスのエクスポート
    data_exporter = DataExporter()
    data_exporter.export_simulation_data(
        flow_metrics=metrics_collector.flow_metrics,
        network_metrics=metrics_collector.network_metrics,
        format='csv',
        file_path='output/metrics'
    )

def main():
    st.title("ネットワークシミュレーションツール")

    # サイドバーで設定を取得
    st.sidebar.title("Simulation Settings")
    simulation_time = st.sidebar.number_input("Simulation Time", min_value=0.0, value=1000.0)
    failure_rate = st.sidebar.slider("Failure Rate", min_value=0.0, max_value=1.0, value=0.01)
    algorithm = st.sidebar.selectbox("Routing Algorithm", ["dijkstra", "dqn", "ddpg"])

    # テストの実行
    if st.sidebar.button("Run Tests"):
        st.write("Running tests...")
        import subprocess
        result = subprocess.run(['python', '-m', 'unittest', 'discover'], capture_output=True, text=True)
        st.code(result.stdout)
        if result.returncode == 0:
            st.success("All tests passed.")
        else:
            st.error("Some tests failed.")

    # シミュレーションの実行
    if st.button("Run Simulation"):
        st.write("Simulation is running...")
        run_simulation(simulation_time, failure_rate, algorithm)

if __name__ == '__main__':
    main()
