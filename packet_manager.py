# packet_manager.py

from typing import List, Optional
from packet import Packet
from flow import Flow
from topology_manager import TopologyManager
from node import Node
from simulation_engine import SimulationEngine

class PacketManager:
    """
    パケット管理クラス

    Attributes:
        packets_in_transit (List[Packet]): 転送中のパケットリスト
        topology_manager (TopologyManager): トポロジマネージャ
        simulation_engine (SimulationEngine): シミュレーションエンジン
    """

    def __init__(self, topology_manager: TopologyManager, simulation_engine: SimulationEngine):
        """
        パケットマネージャの初期化

        Args:
            topology_manager (TopologyManager): トポロジマネージャ
            simulation_engine (SimulationEngine): シミュレーションエンジン
        """
        self.packets_in_transit: List[Packet] = []
        self.topology_manager = topology_manager
        self.simulation_engine = simulation_engine

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

            if link and link.transmit_packet(packet):
                # リンクが使用可能な場合
                packet.current_node_index = next_node_index
                arrival_time = self.simulation_engine.current_time + link.delay
                self.simulation_engine.schedule_event(arrival_time, lambda: self.receive_packet(packet, next_node_id))
            else:
                # リンクが使用不可の場合
                packet.status = "lost"
        else:
            # 目的地に到達
            packet.status = "delivered"

    def receive_packet(self, packet: Packet, node_id: int):
        """
        パケットを受信

        Args:
            packet (Packet): パケットオブジェクト
            node_id (int): 受信ノードID
        """
        node = self.topology_manager.get_node(node_id)
        if node and node.enqueue_packet(packet):
            # バッファにパケットを追加し、次の送信をスケジュール
            self.simulation_engine.schedule_event(self.simulation_engine.current_time, lambda: self.send_packet(packet, node))
        else:
            # バッファオーバーフロー
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
