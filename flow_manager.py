# flow_manager.py

import random
from typing import Optional, Dict, List
import yaml
from flow import Flow
from topology_manager import TopologyManager

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
