from typing import List, Dict, Optional
from packet import Packet

class Node:
    """
    ノードクラス

    Attributes:
        node_id (int): ノードID
        buffer (List[Packet]): パケットバッファ
        adjacent_links (List[int]): 隣接リンクIDのリスト
        virtual_weights (Dict[int, float]): 仮想重み（リンクIDをキーとする辞書）
        status (str): ノードの状態（"active" または "failed"）
        buffer_size (int): バッファの最大容量（バイト）
        buffer_occupancy (int): 現在のバッファ使用量（バイト）
    """

    def __init__(self, node_id: int, buffer_size: int = 1000000, demand_params: float = 0.0):
        """
        ノードの初期化

        Args:
            node_id (int): ノードID
            buffer_size (int, optional): バッファサイズ（デフォルトは1,000,000バイト）
        """
        self.node_id = node_id
        self.buffer: List[Packet] = []
        self.adjacent_links: List[int] = []
        self.virtual_weights: Dict[int, float] = {}
        self.status: str = "active"
        self.buffer_size = buffer_size
        self.buffer_occupancy = 0

    def enqueue_packet(self, packet: Packet) -> bool:
        """
        パケットをバッファに追加

        Args:
            packet (Packet): 追加するパケット

        Returns:
            bool: 成功した場合True、バッファオーバーフローの場合False
        """
        if self.buffer_occupancy + packet.size <= self.buffer_size:
            self.buffer.append(packet)
            self.buffer_occupancy += packet.size
            return True
        else:
            # バッファオーバーフロー
            return False

    def dequeue_packet(self) -> Optional[Packet]:
        """
        バッファからパケットを取り出す

        Returns:
            Optional[Packet]: 取り出したパケット、バッファが空の場合None
        """
        if self.buffer:
            packet = self.buffer.pop(0)
            self.buffer_occupancy -= packet.size
            return packet
        return None

    def process_buffer(self):
        """
        バッファ内のパケットを処理（送信など）
        """
        # バッファ内のパケットを順次処理
        pass

    def fail_node(self, duration: float):
        """
        ノードを障害状態に設定

        Args:
            duration (float): 障害の継続時間
        """
        self.status = "failed"
        # 障害復旧イベントをスケジュール
        pass

    def recover_node(self):
        """
        ノードを正常状態に復帰
        """
        self.status = "active"
