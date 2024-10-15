# metrics_collector.py

from typing import List
import csv
from flow import Flow
from packet import Packet

class FlowMetric:
    """
    フローメトリッククラス

    Attributes:
        timestamp (float): 計測時刻
        flow_id (int): フローID
        throughput (float): スループット（bps）
        delay (float): 平均遅延（秒）
        packet_loss_rate (float): パケットロス率（%）
        jitter (float): ジッター（秒）
    """

    def __init__(self, timestamp: float, flow_id: int, throughput: float, delay: float, packet_loss_rate: float, jitter: float):
        self.timestamp = timestamp
        self.flow_id = flow_id
        self.throughput = throughput
        self.delay = delay
        self.packet_loss_rate = packet_loss_rate
        self.jitter = jitter

class NetworkMetric:
    """
    ネットワークメトリッククラス

    Attributes:
        timestamp (float): 計測時刻
        average_throughput (float): 平均スループット
        average_delay (float): 平均遅延
        average_packet_loss_rate (float): 平均パケットロス率
        average_jitter (float): 平均ジッター
    """

    def __init__(self, timestamp: float, average_throughput: float, average_delay: float, average_packet_loss_rate: float, average_jitter: float):
        self.timestamp = timestamp
        self.average_throughput = average_throughput
        self.average_delay = average_delay
        self.average_packet_loss_rate = average_packet_loss_rate
        self.average_jitter = average_jitter

class MetricsCollector:
    """
    メトリクス収集クラス

    Attributes:
        flow_metrics (List[FlowMetric]): フローメトリクスのリスト
        network_metrics (List[NetworkMetric]): ネットワークメトリクスのリスト
    """

    def __init__(self):
        self.flow_metrics: List[FlowMetric] = []
        self.network_metrics: List[NetworkMetric] = []

    def record_flow_metrics(self, timestamp: float, flow: Flow):
        """
        フローごとのメトリクスを記録

        Args:
            timestamp (float): 計測時刻
            flow (Flow): フローオブジェクト
        """
        # スループットの計算（bps）
        total_bytes_received = sum(packet.size for packet in flow.packets if packet.status == "delivered")
        duration = max((packet.arrival_time - packet.sent_time) for packet in flow.packets if packet.status == "delivered") if flow.packets else 0
        throughput = (total_bytes_received * 8) / duration if duration > 0 else 0

        # 平均遅延の計算（秒）
        delays = [(packet.arrival_time - packet.sent_time) for packet in flow.packets if packet.status == "delivered"]
        delay = sum(delays) / len(delays) if delays else 0

        # パケットロス率の計算（%）
        total_packets_sent = len(flow.packets)
        total_packets_received = sum(1 for packet in flow.packets if packet.status == "delivered")
        packet_loss_rate = ((total_packets_sent - total_packets_received) / total_packets_sent) * 100 if total_packets_sent > 0 else 0

        # ジッターの計算（秒）
        if len(delays) > 1:
            delay_diffs = [abs(delays[i] - delays[i - 1]) for i in range(1, len(delays))]
            jitter = sum(delay_diffs) / len(delay_diffs)
        else:
            jitter = 0

        flow_metric = FlowMetric(timestamp, flow.flow_id, throughput, delay, packet_loss_rate, jitter)
        self.flow_metrics.append(flow_metric)

    def record_network_metrics(self, timestamp: float):
        """
        ネットワーク全体のメトリクスを記録

        Args:
            timestamp (float): 計測時刻
        """
        if not self.flow_metrics:
            return

        avg_throughput = sum([fm.throughput for fm in self.flow_metrics]) / len(self.flow_metrics)
        avg_delay = sum([fm.delay for fm in self.flow_metrics]) / len(self.flow_metrics)
        avg_packet_loss_rate = sum([fm.packet_loss_rate for fm in self.flow_metrics]) / len(self.flow_metrics)
        avg_jitter = sum([fm.jitter for fm in self.flow_metrics]) / len(self.flow_metrics)

        network_metric = NetworkMetric(timestamp, avg_throughput, avg_delay, avg_packet_loss_rate, avg_jitter)
        self.network_metrics.append(network_metric)

    def export_metrics_csv(self, file_path: str):
        """
        メトリクスをCSV形式でエクスポート

        Args:
            file_path (str): ファイルパス
        """
        with open(file_path + '_flow_metrics.csv', 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'flow_id', 'throughput', 'delay', 'packet_loss_rate', 'jitter']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for fm in self.flow_metrics:
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
            for nm in self.network_metrics:
                writer.writerow({
                    'timestamp': nm.timestamp,
                    'average_throughput': nm.average_throughput,
                    'average_delay': nm.average_delay,
                    'average_packet_loss_rate': nm.average_packet_loss_rate,
                    'average_jitter': nm.average_jitter
                })
