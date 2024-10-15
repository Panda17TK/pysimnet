# packet.py

from typing import List

class Packet:
    """
    パケットクラス

    Attributes:
        packet_id (int): パケットID
        flow_id (int): フローID
        size (int): パケットサイズ（バイト）
        route (List[int]): 通過予定ノードIDのリスト
        current_node_index (int): 現在のノードインデックス
        status (str): パケットの状態（"in_transit", "delivered", "lost"）
    """

    def __init__(self, packet_id: int, flow_id: int, size: int):
        """
        パケットの初期化

        Args:
            packet_id (int): パケットID
            flow_id (int): フローID
            size (int): パケットサイズ（バイト）
        """
        self.packet_id = packet_id
        self.flow_id = flow_id
        self.size = size
        self.route: List[int] = []
        self.current_node_index = 0
        self.status = "in_transit"
        self.sent_time: float = 0.0  # 送信時間
        self.arrival_time: float = 0.0  # 到着時間
