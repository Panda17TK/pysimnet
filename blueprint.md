# 通信ネットワークシミュレーションソフトウェアの設計図**

---
**

## 全体概要

本シミュレーションソフトウェアは、現実に近い通信ネットワーク環境を再現するために設計されます。以下の機能を持つ複数のモジュールから構成されます。

1. **シミュレーションエンジン**：時間の進行とイベントのスケジューリングを管理。
2. **ネットワークトポロジ管理**：ノードとリンクの構成を管理。
3. **フロー管理**：通信要求（フロー）の生成と追跡。
4. **パケット管理**：フローを構成するパケットの生成と転送。
5. **ノード管理**：バッファ、キューイング、障害処理を含むノードの動作を管理。
6. **リンク管理**：帯域幅、遅延、ジッター、障害処理を含むリンクの動作を管理。
7. **中央コントローラ**：ルーティングアルゴリズムと仮想重みの計算・配信。
8. **障害管理**：ノードおよびリンクの障害発生と復旧を管理。
9. **メトリクス収集**：スループット、遅延、パケットロス率、ジッターのデータを収集・保存。
10. **可視化・インターフェース**：シミュレーション結果の表示とユーザー設定。

---

### 1. シミュレーションエンジンモジュール

**概要**：シミュレーションの時間進行とイベント処理を管理します。

- **主要クラス/モジュール**
  - SimulationEngine

  **関数・メソッド**

- initialize(simulation_time: float): シミュレーションの初期化。
- run(): シミュレーションの開始。
- schedule_event(event_time: float, event_function: Callable): イベントのスケジューリング。
- process_events(): イベントの処理。

  **変数**

- current_time: float：現在のシミュレーション時間。
- event_queue: List[Event]：イベントの優先度付きキュー。

---

### 2. ネットワークトポロジ管理モジュール

  **概要**：ノードとリンクの構成を読み込み、管理します。

- **主要クラス/モジュール**
  - TopologyManager

  **関数・メソッド**

- load_topology(yaml_file: str): YAMLファイルからトポロジを読み込む。
- get_node(node_id: int) -> Node: ノードIDからノードオブジェクトを取得。
- get_link(link_id: int) -> Link: リンクIDからリンクオブジェクトを取得。

  **変数**

- nodes: Dict[int, Node]：ノードIDをキーとするノードオブジェクトの辞書。
- links: Dict[int, Link]：リンクIDをキーとするリンクオブジェクトの辞書。

  **データ構造**

- Node
  - node_id: int
  - buffer: Queue[Packet]
  - adjacent_links: List[int]：隣接リンクのIDリスト。
  - virtual_weights: Dict[int, float]：リンクIDをキーとする仮想重み。

- Link
  - link_id: int
  - capacity: float：最大帯域幅（bps）。
  - current_load: float：現在の帯域使用量。
  - delay: float：遅延時間（秒）。
  - jitter: float：ジッター値（秒）。
  - status: str："active" または "failed"。
  - connected_nodes: Tuple[int, int]：リンクで接続されているノードIDのタプル。

---

### 3. フロー管理モジュール

  **概要**：通信要求（フロー）の生成、追跡、再送制御を行います。

- **主要クラス/モジュール**
  - FlowManager

  **関数・メソッド**

- generate_flows(flow_scenario: Optional[str]): フローの生成。シナリオが指定されていればそれを使用。
- track_flow(flow_id: int): フローの状態を追跡。
- handle_flow_completion(flow_id: int): フローの完了処理。

  **変数**

- flows: Dict[int, Flow]：フローIDをキーとするフローオブジェクトの辞書。

  **データ構造**

- Flow
  - flow_id: int
  - service_type: str：サービスの種類（例："video", "voice", "data"）。
  - flow_size: int：フロー全体のサイズ（バイト）。
  - packet_count: int：パケット数。
  - source_node: int：送信元ノードID。
  - destination_node: int：送信先ノードID。
  - packets: List[Packet]：パケットオブジェクトのリスト。
  - status: str："active", "completed", "failed"。

---

### 4. パケット管理モジュール

**概要**：フローを構成するパケットの生成、転送、再送を管理します。

- **主要クラス/モジュール**
  - PacketManager

  **関数・メソッド**

- create_packets(flow: Flow) -> List[Packet]: フローからパケットを生成。
- send_packet(packet: Packet, current_node: Node): パケットを送信。
- receive_packet(packet: Packet, current_node: Node): パケットを受信。
- retransmit_packet(packet: Packet): 送信失敗したパケットの再送。

  **変数**

- packets_in_transit: List[Packet]：転送中のパケットリスト。

  **データ構造**

- Packet
  - packet_id: int
  - flow_id: int
  - size: int：パケットサイズ（バイト）。
  - route: List[int]：通過予定ノードIDのリスト。
  - current_node_index: int：ルート上の現在のノードのインデックス。
  - status: str："in_transit", "delivered", "lost"。

---

### 5. ノード管理モジュール

**概要**：ノードの動作、バッファ管理、キューイング、障害処理を行います。

- **主要クラス/モジュール**
  - Node

  **関数・メソッド**

- enqueue_packet(packet: Packet): パケットをバッファに追加。
- dequeue_packet() -> Optional[Packet]: パケットをバッファから取り出し。
- process_buffer(): バッファ内のパケットを処理。
- fail_node(duration: float): ノードを障害状態に変更。
- recover_node(): ノードを正常状態に復帰。

  **変数**

- buffer_size: int：バッファの最大容量（バイト）。
- buffer_occupancy: int：現在のバッファ使用量。
- status: str："active" または "failed"。

---

### 6. リンク管理モジュール

**概要**：リンクの動作、帯域幅管理、遅延、ジッター、障害処理を行います。

- **主要クラス/モジュール**
  - Link

  **関数・メソッド**

- transmit_packet(packet: Packet): パケットをリンク経由で転送。
- update_load(packet_size: int, operation: str): 帯域使用量を更新。operationは"add"または"remove"。
- fail_link(duration: float): リンクを障害状態に変更。
- recover_link(): リンクを正常状態に復帰。

  **変数**

- capacity: float：最大帯域幅（bps）。
- current_load: float：現在の帯域使用量。
- status: str："active" または "failed"。

---

### 7. 中央コントローラモジュール

**概要**：ルーティングアルゴリズムの実行と仮想重みの計算・配信を行います。

- **主要クラス/モジュール**
  - CentralController

  **関数・メソッド**

- calculate_virtual_weights(algorithm: str): 指定されたアルゴリズムで仮想重みを計算。
- distribute_virtual_weights(): 仮想重みを各ノードに配信。
- update_network_state(): ノードとリンクの状態を更新。
- notify_failure(failure_type: str, element_id: int): 障害情報を受信し処理。

  **変数**

- algorithm: str：使用中のルーティングアルゴリズム。
- network_state: Dict：ノードおよびリンクの状態情報。
  - node_statuses: Dict[int, str]：ノードIDをキーとする状態（"active"または"failed"）。
  - link_statuses: Dict[int, str]：リンクIDをキーとする状態。
  - link_bandwidths: Dict[int, float]：リンクIDをキーとする帯域幅。
  - node_buffers: Dict[int, int]：ノードIDをキーとするバッファ使用量。
  - link_delays: Dict[int, float]：リンクIDをキーとする遅延。
  - link_jitters: Dict[int, float]：リンクIDをキーとするジッター。

---

### 8. 障害管理モジュール

**概要**：ノードおよびリンクの障害発生と復旧を管理します。

- **主要クラス/モジュール**
  - FailureManager

  **関数・メソッド**

- schedule_failures(failure_rate: float, failure_distribution: str): 障害のスケジューリング。
- execute_failure(): 障害を実行。
- recover_element(element_type: str, element_id: int): 障害要素の復旧。

  **変数**

- failure_events: List[FailureEvent]：障害イベントのリスト。

  **データ構造**

- FailureEvent
  - event_time: float
  - element_type: str："node"または"link"。
  - element_id: int
  - duration: float：障害継続時間。

---

### 9. メトリクス収集モジュール

**概要**：シミュレーション中の各種メトリクスを収集し、時系列データとして保存します。

- **主要クラス/モジュール**
  - MetricsCollector

  **関数・メソッド**

- record_flow_metrics(flow: Flow): フローごとのメトリクスを記録。
- record_network_metrics(): ネットワーク全体のメトリクスを記録。
- export_metrics_csv(file_path: str): メトリクスをCSV形式でエクスポート。

  **変数**

- flow_metrics: List[FlowMetric]：フローメトリクスのリスト。
- network_metrics: List[NetworkMetric]：ネットワークメトリクスのリスト。

  **データ構造**

- FlowMetric
  - timestamp: float
  - flow_id: int
  - throughput: float：bps。
  - delay: float：秒。
  - packet_loss_rate: float：パーセンテージ。
  - jitter: float：秒。

- NetworkMetric
  - timestamp: float
  - average_throughput: float
  - average_delay: float
  - average_packet_loss_rate: float
  - average_jitter: float

---

### 10. 可視化・インターフェースモジュール

**概要**：シミュレーション結果の可視化とユーザー設定のインターフェースを提供します。

- **主要クラス/モジュール**
  - VisualizationInterface

  **関数・メソッド**

- display_metrics(metrics_data: Dict): メトリクスをグラフや表で表示。
- update_visualization(): シミュレーション中の可視化を更新。
- get_user_settings() -> Dict: ユーザーからの設定入力を取得。

  **変数**

- metrics_history: Dict[str, List[float]]：メトリクス名をキーとする時系列データ。

---

### 11. 設定・データエクスポートモジュール

**概要**：シミュレーションの設定管理とデータのエクスポートを行います。

- **主要クラス/モジュール**
  - ConfigurationManager
  - DataExporter

  **関数・メソッド**

- load_configuration(config_file: str): 設定ファイルからシミュレーションパラメータを読み込む。
- save_flow_scenario(yaml_file: str): フローシナリオをYAML形式で保存。
- export_simulation_data(format: str, file_path: str): シミュレーションデータを指定された形式でエクスポート。

  **変数**

- simulation_parameters: Dict：シミュレーション全体のパラメータ。
- flow_scenario: Dict：フロー生成に関する設定。

---

### 変数とデータ型の詳細

- **基本データ型**
  - int: 整数型。
  - float: 浮動小数点数型。
  - str: 文字列型。
  - bool: ブール型。
  - List[T]: 型Tのリスト。
  - Dict[K, V]: キーが型K、値が型Vの辞書。
  - Tuple[T1, T2]: 型T1とT2のタプル。
  - Callable: 呼び出し可能な関数オブジェクト。

- **配列構造と想定される値**

  - event_queue: List[Event]
    - 時間順にソートされたイベントのリスト。
    - 各Eventはevent_timeとevent_functionを持つ。

  - nodes: Dict[int, Node]
    - キー：ノードID（例：1, 2, ..., 20）
    - 値：Nodeオブジェクト。

  - links: Dict[int, Link]
    - キー：リンクID（例：1, 2, ..., 60）
    - 値：Linkオブジェクト。

  - flows: Dict[int, Flow]
    - キー：フローID（例：1001, 1002, ...）
    - 値：Flowオブジェクト。

  - packets_in_transit: List[Packet]
    - 現在ネットワーク上を転送中のパケットリスト。

  - metrics_history: Dict[str, List[float]]
    - キー：メトリクス名（例："throughput", "delay", "packet_loss_rate", "jitter"）
    - 値：各メトリクスの時系列データリスト。

---

### イベントの非同期・並列処理

- 同一時間単位に発生するイベントは、イベントキューから取り出した後、非同期処理（例：スレッド、コルーチン）を使用して並列に実行します。

  **非同期処理のためのデータ構造**

- asyncio.Taskまたはスレッドプールを利用してイベントを並列に処理。

---

### 障害発生のスケジューリング

- 障害発生の頻度と分布は以下の変数で指定。

  **変数**

- failure_rate: float：障害発生率（例：0.01は1%の確率）。
- failure_distribution: str：障害継続時間の分布（例："uniform", "exponential"）。
- default_failure_duration_range: Tuple[float, float]：デフォルトの障害継続時間の範囲（例：(0, 100)）。

---

### ルーティングアルゴリズムの選択と動作

- **アルゴリズムの種類**
  - "dijkstra"：ダイクストラ法。
  - "dqn"：Deep Q-Network。
  - "ddpg"：Deep Deterministic Policy Gradient。

  **アルゴリズムによる動作の違い**

- **ダイクストラ法の場合**
  - 障害発生時に仮想重みを再計算し、最短経路を更新。

- **DQN/DDPGの場合**
  - 障害発生したリンクの帯域幅を0に設定し、その状態でエージェントを更新。

---

### シナリオの再現性

- フロー生成時に記録されたYAMLファイルを次回の実行時に読み込むことで、同一の通信要求シナリオを再現可能。

  **関数**

- load_flow_scenario(yaml_file: str): フローシナリオを読み込む。
- save_flow_scenario(yaml_file: str): フローシナリオを保存。

---

### 最終的なデータエクスポート

- シミュレーション終了後、以下のデータをエクスポート。

  **エクスポートされるデータ**

- metrics.csv: メトリクスの時系列データ。
- flow_scenario.yaml: 通信要求の履歴と情報。
- network_state.csv: ネットワーク状態の時系列データ（中央コントローラの保持情報）。

---
