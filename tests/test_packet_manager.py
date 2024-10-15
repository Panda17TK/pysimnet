import sys
import os
import unittest
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from packet_manager import PacketManager
from flow import Flow
from topology_manager import TopologyManager
from simulation_engine import SimulationEngine
from node import Node
from link import Link
from central_controller import CentralController
from metrics_collector import MetricsCollector

class TestPacketManager(unittest.TestCase):
    """
    PacketManagerクラスのユニットテストクラス
    """

    def setUp(self):
        """
        各テストメソッドの前に実行されるセットアップメソッド
        """
        self.topology_manager = TopologyManager()
        self.simulation_engine = SimulationEngine()
        self.central_controller = CentralController(self.topology_manager)
        self.metrics_collector = MetricsCollector()

        # シンプルなトポロジを設定
        self.topology_manager.nodes = {
            1: Node(node_id=1),
            2: Node(node_id=2)
        }
        self.topology_manager.links = {
            1: Link(link_id=1, capacity=1000.0, delay=0.1, jitter=0.0, connected_nodes=(1, 2))
        }
        self.topology_manager.nodes[1].adjacent_links.append(1)
        self.topology_manager.nodes[2].adjacent_links.append(1)

        self.packet_manager = PacketManager(
            topology_manager=self.topology_manager,
            simulation_engine=self.simulation_engine,
            central_controller=self.central_controller,
            metrics_collector=self.metrics_collector
        )

    def test_create_packets(self):
        """
        create_packetsメソッドのテスト
        """
        flow = Flow(flow_id=1, service_type='data', flow_size=3000, source_node=1, destination_node=2)
        packets = self.packet_manager.create_packets(flow)
        self.assertEqual(len(packets), 2)  # 1500バイトごとに分割

    def test_send_packet(self):
        """
        send_packetメソッドのテスト
        """
        flow = Flow(flow_id=1, service_type='data', flow_size=1500, source_node=1, destination_node=2)
        packet = self.packet_manager.create_packets(flow)[0]
        packet.route = [1, 2]
        packet.current_node_index = 0  # ノード1から送信

        current_node = self.topology_manager.get_node(1)

        # リンクの状態を設定
        link_id = self.packet_manager.find_link_between_nodes(1, 2)
        link = self.topology_manager.get_link(link_id)
        link.status = "active"
        link.current_load = 0
        link.capacity = 2000  # 帯域幅に余裕を持たせる

        # パケットを送信
        self.packet_manager.send_packet(packet, current_node)

        # イベントキューにイベントがスケジュールされたか確認
        self.assertEqual(len(self.simulation_engine.event_queue), 1)
        event = self.simulation_engine.event_queue[0]
        expected_arrival_time = self.simulation_engine.current_time + link.delay  # 遅延時間を考慮
        self.assertEqual(event.event_time, expected_arrival_time)

    def test_receive_packet(self):
        """
        receive_packetメソッドのテスト
        """
        flow = Flow(flow_id=1, service_type='data', flow_size=1500, source_node=1, destination_node=2)
        packet = self.packet_manager.create_packets(flow)[0]
        packet.route = [1, 2]
        packet.current_node_index = 1  # ノード2に到着

        # リンクを取得
        link_id = self.packet_manager.find_link_between_nodes(1, 2)
        link = self.topology_manager.get_link(link_id)

        # ノード2のバッファに空きがある場合
        self.packet_manager.receive_packet(packet, 2, link)
        self.assertEqual(len(self.topology_manager.get_node(2).buffer), 1)

        # バッファに空きがない場合
        self.topology_manager.get_node(2).buffer_size = 0  # バッファサイズを0に設定
        packet.status = "in_transit"
        self.packet_manager.receive_packet(packet, 2, link)
        self.assertEqual(packet.status, "lost")

if __name__ == '__main__':
    unittest.main()