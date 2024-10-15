# visualization_interface.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class VisualizationInterface:
    """
    可視化・インターフェースクラス

    Attributes:
        metrics_history (Dict[str, List[float]]): メトリクス名をキーとする時系列データ
    """

    def __init__(self):
        self.metrics_history = {}

    def display_metrics(self, metrics_data: pd.DataFrame):
        """
        メトリクスをグラフや表で表示

        Args:
            metrics_data (pd.DataFrame): メトリクスのデータフレーム
        """
        st.line_chart(metrics_data.set_index('timestamp'))

    def update_visualization(self, metrics_collector):
        """
        シミュレーション中の可視化を更新

        Args:
            metrics_collector (MetricsCollector): メトリクス収集クラス
        """
        # フローメトリクスをデータフレームに変換
        data = [{
            'timestamp': fm.timestamp,
            'throughput': fm.throughput,
            'delay': fm.delay,
            'packet_loss_rate': fm.packet_loss_rate,
            'jitter': fm.jitter
        } for fm in metrics_collector.flow_metrics]

        df = pd.DataFrame(data)
        self.display_metrics(df)

    def get_user_settings(self) -> dict:
        """
        ユーザーからの設定入力を取得

        Returns:
            dict: ユーザー設定の辞書
        """
        st.sidebar.title("Simulation Settings")
        simulation_time = st.sidebar.number_input("Simulation Time", min_value=0.0, value=1000.0)
        failure_rate = st.sidebar.slider("Failure Rate", min_value=0.0, max_value=1.0, value=0.01)
        algorithm = st.sidebar.selectbox("Routing Algorithm", ["dijkstra", "dqn", "ddpg"])

        return {
            'simulation_time': simulation_time,
            'failure_rate': failure_rate,
            'algorithm': algorithm
        }
