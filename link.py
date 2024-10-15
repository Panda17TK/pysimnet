# link.py

from typing import Tuple
from packet import Packet

class Link:
    """
    リンククラス

    Attributes:
        link_id (int): リンクID
        capacity (float): 最大帯域幅（bps）
        current_load (float): 現在の帯域使用量（bps）
        delay (float): 遅延時間（秒）
        jitter (float): ジッター（秒）
        status (str): リンクの状態（"active" または "failed"）
        connected_nodes (Tuple[int, int]): 接続ノードIDのタプル
    """

    def __init__(self, link_id: int, capacity: float, delay: float, jitter: float, connected_nodes: Tuple[int, int]):
        """
        リンクの初期化

        Args:
            link_id (int): リンクID
            capacity (float): 最大帯域幅（bps）
            delay (float): 遅延時間（秒）
            jitter (float): ジッター（秒）
            connected_nodes (Tuple[int, int]): 接続ノードIDのタプル
        """
        self.link_id = link_id
        self.capacity = capacity
        self.current_load = 0.0
        self.delay = delay
        self.jitter = jitter
        self.status = "active"
        self.connected_nodes = connected_nodes

    def transmit_packet(self, packet: Packet) -> bool:
        """
        パケットをリンク経由で転送

        Args:
            packet (Packet): 転送するパケット

        Returns:
            bool: 転送成功ならTrue、失敗ならFalse
        """
        if self.status == "failed":
            # リンクがダウンしている場合
            return False

        if self.current_load + packet.size <= self.capacity:
            self.current_load += packet.size
            # 遅延とジッターを考慮してパケットを転送
            # 実際の遅延処理はシミュレーションエンジンで行う
            return True
        else:
            # 帯域幅不足
            return False

    def update_load(self, packet_size: int, operation: str):
        """
        帯域使用量を更新

        Args:
            packet_size (int): パケットサイズ
            operation (str): "add" または "remove"
        """
        if operation == "add":
            self.current_load += packet_size
        elif operation == "remove":
            self.current_load -= packet_size

    def fail_link(self, duration: float):
        """
        リンクを障害状態に設定

        Args:
            duration (float): 障害の継続時間
        """
        self.status = "failed"
        # 障害復旧イベントをスケジュール
        pass

    def recover_link(self):
        """
        リンクを正常状態に復帰
        """
        self.status = "active"
