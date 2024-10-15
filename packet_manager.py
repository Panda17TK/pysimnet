# packet_manager.py

from typing import List, Optional
from packet import Packet
from flow import Flow
from link import Link
from node import Node

import random

import networkx as nx
class PacketManager:
    """
    パケット管理クラス

    Attributes:
        packets_in_transit (List[Packet]): 転送中のパケットリスト
        topology_manager (TopologyManager): トポロジマネージャ
        simulation_engine (SimulationEngine): シミュレーションエンジン
    """

    def __init__(self, topology_manager, simulation_engine, central_controller, metrics_collector):
        """
        パケットマネージャの初期化

        Args:
            topology_manager (TopologyManager): トポロジマネージャ
            simulation_engine (SimulationEngine): シミュレーションエンジン
        """
        self.packets_in_transit: List[Packet] = []
        self.topology_manager = topology_manager
        self.simulation_engine = simulation_engine
        self.central_controller = central_controller
        self.metrics_collector = metrics_collector

    def create_packets(self, flow: Flow) -> List[Packet]:
        """
        フローからパケットを生成

        Args:
            flow (Flow): フローオブジェクト

        Returns:
            List[Packet]: 生成されたパケットのリスト
        """
        packets = []
        for i in range(flow.packet_count):
            packet_id = flow.flow_id * 100000 + i  # 一意なID
            packet = Packet(packet_id, flow.flow_id, 1500)  # パケットサイズ1500バイト
            packet.route = self.calculate_route(flow.source_node, flow.destination_node)
            packets.append(packet)
        flow.packets = packets
        return packets

    def calculate_route(self, source_node_id: int, destination_node_id: int) -> List[int]:
        """
        パケットの経路を計算

        Args:
            source_node_id (int): 送信元ノードID
            destination_node_id (int): 送信先ノードID

        Returns:
            List[int]: 経路上のノードIDリスト
        """
        # ルーティングアルゴリズムを実装（例：ダイクストラ法）
        # 仮の実装として直接接続を返す
        return [source_node_id, destination_node_id]

    def send_packet(self, packet: Packet, current_node: Node):
        """
        パケットを送信

        Args:
            packet (Packet): パケットオブジェクト
            current_node (Node): 現在のノード
        """
        if current_node.status == "failed":
            # ノードがダウンしている場合
            packet.status = "lost"
            return

        next_node_index = packet.current_node_index + 1
        if next_node_index < len(packet.route):
            next_node_id = packet.route[next_node_index]
            link_id = self.find_link_between_nodes(current_node.node_id, next_node_id)
            link = self.topology_manager.get_link(link_id)

            if link and link.status == "active":
                # リンクが使用可能な場合
                # 帯域幅チェック
                if link.current_load + packet.size <= link.capacity:
                    link.update_load(packet.size, "add")
                    packet.sent_time = self.simulation_engine.current_time
                    packet.current_node_index = next_node_index

                    # 遅延とジッターを考慮
                    actual_delay = link.delay + random.uniform(-link.jitter, link.jitter)
                    arrival_time = self.simulation_engine.current_time + actual_delay

                    # パケット到着イベントをスケジュール
                    self.simulation_engine.schedule_event(arrival_time, lambda p=packet, nid=next_node_id: self.receive_packet(p, nid, link))
                else:
                    # 帯域幅不足
                    # パケットをバッファに戻すか、ロスとするかの判断
                    packet.status = "lost"
                    link.packet_loss_count += 1
            else:
                # リンクが使用不可の場合
                packet.status = "lost"
        else:
            # 目的地に到達
            packet.status = "delivered"
            packet.arrival_time = self.simulation_engine.current_time
            # フローのメトリクスを更新
            self.metrics_collector.record_flow_metrics(self.simulation_engine.current_time, self.flow_manager.flows[packet.flow_id])

    def receive_packet(self, packet: Packet, node_id: int, link: Link):
        """
        パケットを受信

        Args:
            packet (Packet): パケットオブジェクト
            node_id (int): 受信ノードID
            link (Link): パケットを通過したリンク
        """
        link.update_load(packet.size, "remove")
        node = self.topology_manager.get_node(node_id)
        if node and node.status == "active":
            # バッファにパケットを追加
            if node.enqueue_packet(packet):
                # 次の送信をスケジュール
                self.simulation_engine.schedule_event(self.simulation_engine.current_time, lambda: self.send_packet(packet, node))
            else:
                # バッファオーバーフロー
                packet.status = "lost"
        else:
            # ノードがダウンしている場合
            packet.status = "lost"

    def find_link_between_nodes(self, node1_id: int, node2_id: int) -> Optional[int]:
        """
        2つのノード間のリンクIDを取得

        Args:
            node1_id (int): ノード1のID
            node2_id (int): ノード2のID

        Returns:
            Optional[int]: リンクIDまたはNone
        """
        node1 = self.topology_manager.get_node(node1_id)
        if node1:
            for link_id in node1.adjacent_links:
                link = self.topology_manager.get_link(link_id)
                if link and node2_id in link.connected_nodes:
                    return link_id
        return None

    def retransmit_packet(self, packet: Packet):
        """
        パケットの再送

        Args:
            packet (Packet): パケットオブジェクト
        """
        packet.current_node_index = 0  # 送信元から再送
        self.send_packet(packet, self.topology_manager.get_node(packet.route[0]))

    def calculate_route(self, source_node_id: int, destination_node_id: int) -> List[int]:
        """
        パケットの経路を計算

        Args:
            source_node_id (int): 送信元ノードID
            destination_node_id (int): 送信先ノードID

        Returns:
            List[int]: 経路上のノードIDリスト
        """
        if self.central_controller.algorithm == "dijkstra":
            return self._calculate_route_dijkstra(source_node_id, destination_node_id)
        elif self.central_controller.algorithm == "dqn":
            return self._calculate_route_dqn(source_node_id, destination_node_id)
        elif self.central_controller.algorithm == "ddpg":
            return self._calculate_route_ddpg(source_node_id, destination_node_id)
        else:
            raise ValueError(f"Unknown algorithm: {self.central_controller.algorithm}")

    def _calculate_route_dijkstra(self, source_node_id: int, destination_node_id: int) -> List[int]:
        """
        ダイクストラ法による経路計算

        Args:
            source_node_id (int): 送信元ノードID
            destination_node_id (int): 送信先ノードID

        Returns:
            List[int]: 経路上のノードIDリスト
        """
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
                # リンクがダウンしている場合、エッジを追加しない
                pass

        try:
            path = nx.dijkstra_path(G, source=source_node_id, target=destination_node_id)
            return path
        except nx.NetworkXNoPath:
            print(f"No path between {source_node_id} and {destination_node_id}")
            return []

    def _calculate_route_dqn(self, source_node_id: int, destination_node_id: int) -> List[int]:
        """
        DQNによる経路計算（ダミー実装）

        Returns:
            List[int]: 経路上のノードIDリスト
        """
        # ダミーとしてダイクストラ法を使用
        return self._calculate_route_dijkstra(source_node_id, destination_node_id)

    def _calculate_route_ddpg(self, source_node_id: int, destination_node_id: int) -> List[int]:
        """
        DDPGによる経路計算（ダミー実装）

        Returns:
            List[int]: 経路上のノードIDリスト
        """
        # ダミーとしてダイクストラ法を使用
        return self._calculate_route_dijkstra(source_node_id, destination_node_id)