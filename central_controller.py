# central_controller.py

from typing import Dict, Optional
from topology_manager import TopologyManager
import networkx as nx

class CentralController:
    """
    中央コントローラクラス

    Attributes:
        algorithm (str): 使用中のルーティングアルゴリズム
        topology_manager (TopologyManager): トポロジマネージャ
        network_state (Dict): ネットワークの状態情報
    """

    def __init__(self, topology_manager: TopologyManager, algorithm: str = "dijkstra"):
        """
        初期化

        Args:
            topology_manager (TopologyManager): トポロジマネージャ
            algorithm (str, optional): ルーティングアルゴリズムの種類（デフォルトは "dijkstra"）
        """
        self.algorithm = algorithm
        self.topology_manager = topology_manager
        self.network_state = {
            'node_statuses': {},
            'link_statuses': {},
            'link_bandwidths': {},
            'node_buffers': {},
            'link_delays': {},
            'link_jitters': {}
        }
        self.update_network_state()

    def update_network_state(self):
        """
        ノードとリンクの状態を更新
        """
        # ノードの状態を更新
        for node_id, node in self.topology_manager.nodes.items():
            self.network_state['node_statuses'][node_id] = node.status
            self.network_state['node_buffers'][node_id] = node.buffer_occupancy

        # リンクの状態を更新
        for link_id, link in self.topology_manager.links.items():
            self.network_state['link_statuses'][link_id] = link.status
            self.network_state['link_bandwidths'][link_id] = link.capacity
            self.network_state['link_delays'][link_id] = link.delay
            self.network_state['link_jitters'][link_id] = link.jitter

    def calculate_virtual_weights(self):
        """
        仮想重みを計算し、各ノードに設定

        Note:
            使用するアルゴリズムに応じて処理を分岐
        """
        if self.algorithm == "dijkstra":
            self._calculate_weights_dijkstra()
        elif self.algorithm == "dqn":
            self._calculate_weights_dqn()
        elif self.algorithm == "ddpg":
            self._calculate_weights_ddpg()
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")

    def _calculate_weights_dijkstra(self):
        """
        ダイクストラ法による仮想重みの計算
        """
        # NetworkXのグラフを作成
        G = nx.Graph()
        for node_id in self.topology_manager.nodes:
            G.add_node(node_id)

        for link in self.topology_manager.links.values():
            if link.status == "active":
                node1, node2 = link.connected_nodes
                # 重みはリンクの遅延と帯域幅に基づく（簡易的な例）
                weight = link.delay + (1 / link.capacity)
                G.add_edge(node1, node2, weight=weight)
            else:
                # リンクがダウンしている場合、重みを無限大に設定
                node1, node2 = link.connected_nodes
                G.add_edge(node1, node2, weight=float('inf'))

        # 各ノードの仮想重みを更新
        for node_id in self.topology_manager.nodes:
            # 隣接ノードへの重みを設定
            node = self.topology_manager.get_node(node_id)
            node.virtual_weights = {}
            for neighbor in G.neighbors(node_id):
                edge_data = G.get_edge_data(node_id, neighbor)
                node.virtual_weights[neighbor] = edge_data['weight']

    def _calculate_weights_dqn(self):
        """
        DQNによる仮想重みの計算（ダミー実装）
        """
        # ここではダミーとしてランダムな重みを設定
        import random
        for node in self.topology_manager.nodes.values():
            node.virtual_weights = {neighbor: random.random() for neighbor in node.adjacent_links}

    def _calculate_weights_ddpg(self):
        """
        DDPGによる仮想重みの計算（ダミー実装）
        """
        # ここではダミーとして固定の重みを設定
        for node in self.topology_manager.nodes.values():
            node.virtual_weights = {neighbor: 1.0 for neighbor in node.adjacent_links}

    def distribute_virtual_weights(self):
        """
        仮想重みを各ノードに配信
        """
        # 既にノードのvirtual_weightsに設定済みなので、ここでは処理不要
        pass

    def notify_failure(self, failure_type: str, element_id: int):
        """
        障害情報を受信し処理

        Args:
            failure_type (str): 障害の種類（"node" または "link"）
            element_id (int): 障害が発生した要素のID
        """
        print(f"Failure detected: {failure_type} {element_id}")
        self.update_network_state()
        self.calculate_virtual_weights()
        self.distribute_virtual_weights()
