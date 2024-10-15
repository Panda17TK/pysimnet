# flow.py

from typing import List
from packet import Packet

class Flow:
    """
    フロークラス

    Attributes:
        flow_id (int): フローID
        service_type (str): サービスの種類（例："video", "voice", "data"）
        flow_size (int): フローサイズ（バイト）
        packet_count (int): パケット数
        source_node (int): 送信元ノードID
        destination_node (int): 送信先ノードID
        packets (List[Packet]): パケットのリスト
        status (str): フローの状態（"active", "completed", "failed"）
    """

    def __init__(self, flow_id: int, service_type: str, flow_size: int, source_node: int, destination_node: int):
        """
        フローの初期化

        Args:
            flow_id (int): フローID
            service_type (str): サービスの種類
            flow_size (int): フローサイズ（バイト）
            source_node (int): 送信元ノードID
            destination_node (int): 送信先ノードID
        """
        self.flow_id = flow_id
        self.service_type = service_type
        self.flow_size = flow_size
        self.packet_count = flow_size // 1500  # パケットサイズ1500バイト
        self.source_node = source_node
        self.destination_node = destination_node
        self.packets: List[Packet] = []
        self.status = "active"
        self.start_time: float = 0.0  # フロー開始時間
