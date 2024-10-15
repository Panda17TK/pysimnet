# data_exporter.py

import csv
from typing import List
from metrics_collector import FlowMetric, NetworkMetric

class DataExporter:
    """
    データエクスポートクラス
    """

    def export_simulation_data(self, flow_metrics: List[FlowMetric], network_metrics: List[NetworkMetric], format: str, file_path: str):
        """
        シミュレーションデータを指定された形式でエクスポート

        Args:
            flow_metrics (List[FlowMetric]): フローメトリクスのリスト
            network_metrics (List[NetworkMetric]): ネットワークメトリクスのリスト
            format (str): エクスポート形式（"csv", "json" など）
            file_path (str): ファイルパス
        """
        if format == "csv":
            self._export_csv(flow_metrics, network_metrics, file_path)
        else:
            print(f"Unsupported format: {format}")

    def _export_csv(self, flow_metrics: List[FlowMetric], network_metrics: List[NetworkMetric], file_path: str):
        """
        CSV形式でエクスポート

        Args:
            flow_metrics (List[FlowMetric]): フローメトリクスのリスト
            network_metrics (List[NetworkMetric]): ネットワークメトリクスのリスト
            file_path (str): ファイルパス
        """
        with open(file_path + '_flow_metrics.csv', 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'flow_id', 'throughput', 'delay', 'packet_loss_rate', 'jitter']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for fm in flow_metrics:
                writer.writerow({
                    'timestamp': fm.timestamp,
                    'flow_id': fm.flow_id,
                    'throughput': fm.throughput,
                    'delay': fm.delay,
                    'packet_loss_rate': fm.packet_loss_rate,
                    'jitter': fm.jitter
                })

        with open(file_path + '_network_metrics.csv', 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'average_throughput', 'average_delay', 'average_packet_loss_rate', 'average_jitter']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for nm in network_metrics:
                writer.writerow({
                    'timestamp': nm.timestamp,
                    'average_throughput': nm.average_throughput,
                    'average_delay': nm.average_delay,
                    'average_packet_loss_rate': nm.average_packet_loss_rate,
                    'average_jitter': nm.average_jitter
                })
