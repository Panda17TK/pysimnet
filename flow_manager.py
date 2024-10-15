# flow_manager.py

import random
from typing import Optional, Dict, List
import yaml
from flow import Flow
from topology_manager import TopologyManager
from simulation_engine import SimulationEngine


class FlowManager:
    """
    フロー管理クラス

    Attributes:
        flows (Dict[int, Flow]): フローIDをキーとするフローの辞書
        topology_manager (TopologyManager): トポロジマネージャ
    """

    def __init__(self, topology_manager: TopologyManager):
        """
        フローマネージャの初期化

        Args:
            topology_manager (TopologyManager): トポロジマネージャ
        """
        self.flows: Dict[int, Flow] = {}
        self.topology_manager = topology_manager

    def generate_flows(self, flow_scenario: Optional[str] = None):
        """
        フローの生成

        Args:
            flow_scenario (Optional[str]): フローシナリオYAMLファイルパス
        """
        if flow_scenario:
            # YAMLファイルからフローを読み込む
            with open(flow_scenario, 'r') as file:
                flow_data = yaml.safe_load(file)
            for flow_info in flow_data.get('flows', []):
                flow = Flow(
                    flow_id=flow_info['flow_id'],
                    service_type=flow_info['service_type'],
                    flow_size=flow_info['flow_size'],
                    source_node=flow_info['source_node'],
                    destination_node=flow_info['destination_node']
                )
                self.flows[flow.flow_id] = flow
        else:
            # ランダムにフローを生成
            node_ids = list(self.topology_manager.nodes.keys())
            for i in range(1, 101):  # 例として100個のフロー
                flow_id = i
                service_type = random.choice(["video", "voice", "data"])
                flow_size = random.randint(1_000_000, 100_000_000)  # 1MBから100MB
                source_node = random.choice(node_ids)
                destination_node = random.choice(node_ids)
                while destination_node == source_node:
                    destination_node = random.choice(node_ids)
                flow = Flow(flow_id, service_type, flow_size, source_node, destination_node)
                self.flows[flow_id] = flow

    def track_flow(self, flow_id: int):
        """
        フローの状態を追跡

        Args:
            flow_id (int): フローID
        """
        flow = self.flows.get(flow_id)
        if flow:
            # フローの状態をログやメトリクスに記録
            pass

    def handle_flow_completion(self, flow_id: int):
        """
        フロー完了時の処理

        Args:
            flow_id (int): フローID
        """
        flow = self.flows.get(flow_id)
        if flow:
            flow.status = "completed"
            # メトリクスの記録など
            pass

    def schedule_flow_starts(self, simulation_engine: SimulationEngine):
        """
        フロー開始イベントをスケジュール

        Args:
            simulation_engine (SimulationEngine): シミュレーションエンジン
        """
        for flow in self.flows.values():
            start_time = random.uniform(0, simulation_engine.simulation_end_time / 2)
            flow.start_time = start_time
            simulation_engine.schedule_event(start_time, lambda f=flow: self.start_flow(f))

    def start_flow(self, flow: Flow):
        """
        フローを開始

        Args:
            flow (Flow): フローオブジェクト
        """
        # パケットを生成
        packets = self.packet_manager.create_packets(flow)
        # 最初のパケットを送信
        if packets:
            first_packet = packets[0]
            source_node = self.topology_manager.get_node(flow.source_node)
            if source_node:
                self.packet_manager.send_packet(first_packet, source_node)
