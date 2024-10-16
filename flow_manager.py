import random
from typing import Optional, Dict, List
import yaml
from flow import Flow
from topology_manager import TopologyManager
from simulation_engine import SimulationEngine
from packet_manager import PacketManager


class FlowManager:
	"""
	フロー管理クラス

	Attributes:
		flows (Dict[int, Flow]): フローIDをキーとするフローの辞書
		topology_manager (TopologyManager): トポロジマネージャ
		simulation_engine (SimulationEngine): シミュレーションエンジン
		central_controller (CentralController): 中央コントローラ
		metrics_collector (MetricsCollector): メトリクスコレクタ
		packet_manager (PacketManager): パケット管理クラスのインスタンス
	"""

	def __init__(self, topology_manager, simulation_engine, central_controller, metrics_collector):
		"""
		FlowManagerクラスのコンストラクタ。

		Args:
			topology_manager (TopologyManager): トポロジ情報を管理するクラス
			simulation_engine (SimulationEngine): シミュレーションの時間管理を行うエンジン
			central_controller (CentralController): ルーティングを管理する中央コントローラ
			metrics_collector (MetricsCollector): シミュレーションメトリクスを収集するクラス
		"""
		self.topology_manager = topology_manager
		self.simulation_engine = simulation_engine
		self.central_controller = central_controller
		self.metrics_collector = metrics_collector
		self.flows = {}

		# PacketManagerの初期化
		self.packet_manager = PacketManager(
			topology_manager=self.topology_manager,
			simulation_engine=self.simulation_engine,
			central_controller=self.central_controller,
			metrics_collector=self.metrics_collector
		)

	def generate_flows(self, flow_scenario: Optional[str] = None):
		"""
		フローの生成。

		YAMLファイルからフローを読み込むか、指定がない場合はランダムにフローを生成する。

		Args:
			flow_scenario (Optional[str]): フローシナリオYAMLファイルのパス。指定がない場合はランダム生成。
		"""

		if flow_scenario:
			# YAMLファイルからフローを読み込む
			with open(flow_scenario, 'r', encoding='utf-8') as file:
				flow_data = yaml.safe_load(file)
			for flow_info in flow_data.get('flows', []):
				flow = Flow(
					flow_id=flow_info['flow_id'],
					service_type=flow_info['service_type'],
					flow_size=flow_info['flow_size'],
					source_node=flow_info['source_node'],
					destination_node=flow_info['destination_node']
				)
				self.flows[flow.flow_id] = flow
				print(f"ランダムフロー生成: {flow.flow_id}, "
					f"サービス: {flow.service_type}, "
					f"サイズ: {flow.flow_size} bytes, "
					f"送信元: {flow.source_node}, "
					f"送信先: {flow.destination_node}")
		else:
			# ランダムにフローを生成
			node_ids = list(self.topology_manager.nodes.keys())
			for i in range(1, 101):  # 例として100個のフロー
				flow_id = i
				service_type = random.choice(["video", "voice", "data"])
				flow_size = random.randint(1_000_000, 100_000_000)  # 1MBから100MB
				source_node = random.choice(node_ids)
				destination_node = random.choice(node_ids)
				while destination_node == source_node:
					destination_node = random.choice(node_ids)
				flow = Flow(flow_id, service_type, flow_size, source_node, destination_node)
				self.flows[flow_id] = flow
				print(f"ランダムフロー生成: {flow.flow_id}, "
				f"サービス: {flow.service_type}, "
				f"サイズ: {flow.flow_size} bytes, "
				f"送信元: {flow.source_node}, "
				f"送信先: {flow.destination_node}")

	def track_flow(self, flow_id: int):
		"""
		フローの状態を追跡し、必要に応じてログやメトリクスを記録する。

		Args:
			flow_id (int): 追跡するフローのID
		"""
		flow = self.flows.get(flow_id)
		if flow:
			# フローの状態をログやメトリクスに記録
			pass

	def handle_flow_completion(self, flow_id: int):
		"""
		フローの完了処理。

		フローが完了した際にステータスを "completed" に設定し、メトリクスを記録する。

		Args:
			flow_id (int): 完了するフローのID
		"""
		flow = self.flows.get(flow_id)
		if flow:
			flow.status = "completed"
			# メトリクスの記録など
			pass

	def schedule_flow_starts(self, simulation_engine: SimulationEngine):
		"""
		フロー開始イベントをシミュレーションエンジンにスケジュールする。

		フローの開始時間をランダムに決定し、その時間にイベントをスケジュールする。

		Args:
			simulation_engine (SimulationEngine): シミュレーションエンジン。イベントをスケジュールするために使用。
		"""
		for flow in self.flows.values():
			start_time = random.uniform(0, simulation_engine.simulation_end_time / 2)
			flow.start_time = start_time
			simulation_engine.schedule_event(start_time, lambda f=flow: self.start_flow(f))

	def start_flow(self, flow: Flow):
		"""
		指定されたフローの送信を開始する。

		フローに含まれるパケットを生成し、最初のパケットを送信する。

		Args:
			flow (Flow): 送信を開始するフローオブジェクト
		"""
		# パケットを生成
		packets = self.packet_manager.create_packets(flow)
		# 最初のパケットを送信
		if packets:
			first_packet = packets[0]
			source_node = self.topology_manager.get_node(flow.source_node)
			if source_node:
				print(f"Starting flow {flow.flow_id} from node {flow.source_node}")
				self.packet_manager.send_packet(first_packet, source_node)
			else:
				print(f"Source node {flow.source_node} not found for flow {flow.flow_id}")