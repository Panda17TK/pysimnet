import heapq
from typing import Callable, List
import threading

class Event:
    """
    イベントクラス

    Attributes:
        event_time (float): イベントが発生するシミュレーション時間
        event_function (Callable): イベント時に実行される関数
    """

    def __init__(self, event_time: float, event_function: Callable):
        """
        イベントの初期化

        Args:
            event_time (float): イベントが発生するシミュレーション時間
            event_function (Callable): イベント時に実行される関数
        """
        self.event_time = event_time
        self.event_function = event_function

    def __lt__(self, other):
        """
        イベントの比較（優先度付きキュー用）

        Args:
            other (Event): 比較対象のイベント

        Returns:
            bool: 自身のイベントが他のイベントよりも早い場合True
        """
        return self.event_time < other.event_time

class SimulationEngine:
    """
    シミュレーションエンジン

    Attributes:
        current_time (float): 現在のシミュレーション時間
        event_queue (List[Event]): イベントの優先度付きキュー
        simulation_end_time (float): シミュレーションの終了時間
    """

    def __init__(self):
        """
        シミュレーションエンジンの初期化
        """
        self.current_time: float = 0.0
        self.event_queue: List[Event] = []
        self.simulation_end_time: float = 0.0
        self.lock = threading.Lock()  # スレッドセーフのためのロック

    def initialize(self, simulation_time: float):
        """
        シミュレーションの初期化

        Args:
            simulation_time (float): シミュレーションの総時間
        """
        self.current_time = 0.0
        self.event_queue = []
        self.simulation_end_time = simulation_time

    def run(self):
        """
        シミュレーションの開始
        """
        while self.event_queue and self.current_time <= self.simulation_end_time:
            with self.lock:
                event = heapq.heappop(self.event_queue)
                self.current_time = event.event_time

            # 同一時間のイベントを集める
            simultaneous_events = [event]
            with self.lock:
                while self.event_queue and self.event_queue[0].event_time == self.current_time:
                    simultaneous_events.append(heapq.heappop(self.event_queue))

            # 同時イベントを並列処理
            threads = []
            for event in simultaneous_events:
                t = threading.Thread(target=event.event_function)
                threads.append(t)
                t.start()

            # 全てのスレッドが終了するのを待つ
            for t in threads:
                t.join()

    def schedule_event(self, event_time: float, event_function: Callable):
        """
        イベントのスケジューリング

        Args:
            event_time (float): イベントが発生する時間
            event_function (Callable): 実行する関数
        """
        event = Event(event_time, event_function)
        with self.lock:
            heapq.heappush(self.event_queue, event)
