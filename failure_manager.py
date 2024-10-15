# failure_manager.py

import random
from typing import List, Dict
from simulation_engine import SimulationEngine
from topology_manager import TopologyManager
from central_controller import CentralController

class FailureEvent:
    """
    障害イベントクラス

    Attributes:
        event_time (float): イベントが発生する時間
        element_type (str): "node" または "link"
        element_id (int): 障害が発生する要素のID
        duration (float): 障害の継続時間
    """

    def __init__(self, event_time: float, element_type: str, element_id: int, duration: float):
        self.event_time = event_time
        self.element_type = element_type
        self.element_id = element_id
        self.duration = duration

class FailureManager:
    """
    障害管理クラス

    Attributes:
        failure_events (List[FailureEvent]): 障害イベントのリスト
        simulation_engine (SimulationEngine): シミュレーションエンジン
        topology_manager (TopologyManager): トポロジマネージャ
        central_controller (CentralController): 中央コントローラ
    """

    def __init__(self, simulation_engine: SimulationEngine, topology_manager: TopologyManager, central_controller: CentralController):
        """
        初期化

        Args:
            simulation_engine (SimulationEngine): シミュレーションエンジン
            topology_manager (TopologyManager): トポロジマネージャ
            central_controller (CentralController): 中央コントローラ
        """
        self.failure_events: List[FailureEvent] = []
        self.simulation_engine = simulation_engine
        self.topology_manager = topology_manager
        self.central_controller = central_controller

    def schedule_failures(self, failure_rate: float, failure_distribution: str, simulation_time: float):
        """
        障害のスケジューリング

        Args:
            failure_rate (float): 障害発生率
            failure_distribution (str): 障害継続時間の分布
            simulation_time (float): シミュレーションの総時間
        """
        num_failures = int(failure_rate * simulation_time)
        for _ in range(num_failures):
            event_time = random.uniform(0, simulation_time)
            element_type = random.choice(["node", "link"])
            if element_type == "node":
                element_id = random.choice(list(self.topology_manager.nodes.keys()))
            else:
                element_id = random.choice(list(self.topology_manager.links.keys()))
            duration = self._get_failure_duration(failure_distribution)
            failure_event = FailureEvent(event_time, element_type, element_id, duration)
            self.failure_events.append(failure_event)
            # 障害発生イベントをスケジュール
            self.simulation_engine.schedule_event(event_time, lambda fe=failure_event: self.execute_failure(fe))

    def _get_failure_duration(self, distribution: str) -> float:
        """
        障害継続時間を取得

        Args:
            distribution (str): 分布の種類

        Returns:
            float: 障害継続時間
        """
        if distribution == "uniform":
            return random.uniform(0, 100)
        elif distribution == "exponential":
            return random.expovariate(1.0 / 50)  # 平均50秒
        else:
            return random.uniform(0, 100)

    def execute_failure(self, failure_event: FailureEvent):
        """
        障害を実行

        Args:
            failure_event (FailureEvent): 障害イベント
        """
        if failure_event.element_type == "node":
            node = self.topology_manager.get_node(failure_event.element_id)
            if node:
                node.fail_node(failure_event.duration)
                self.central_controller.notify_failure("node", node.node_id)
                # 復旧イベントをスケジュール
                recovery_time = self.simulation_engine.current_time + failure_event.duration
                self.simulation_engine.schedule_event(recovery_time, lambda n=node: self.recover_element("node", n.node_id))
        elif failure_event.element_type == "link":
            link = self.topology_manager.get_link(failure_event.element_id)
            if link:
                link.fail_link(failure_event.duration)
                self.central_controller.notify_failure("link", link.link_id)
                # 復旧イベントをスケジュール
                recovery_time = self.simulation_engine.current_time + failure_event.duration
                self.simulation_engine.schedule_event(recovery_time, lambda l=link: self.recover_element("link", l.link_id))

    def recover_element(self, element_type: str, element_id: int):
        """
        障害要素の復旧

        Args:
            element_type (str): "node" または "link"
            element_id (int): 要素のID
        """
        if element_type == "node":
            node = self.topology_manager.get_node(element_id)
            if node:
                node.recover_node()
                self.central_controller.update_network_state()
        elif element_type == "link":
            link = self.topology_manager.get_link(element_id)
            if link:
                link.recover_link()
                self.central_controller.update_network_state()
