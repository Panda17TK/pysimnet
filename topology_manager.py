# topology_manager.py

import yaml
from typing import Dict, List, Optional
from node import Node
from link import Link

class TopologyManager:
    """
    ネットワークトポロジ管理クラス

    Attributes:
        nodes (Dict[int, Node]): ノードIDをキーとするノードの辞書
        links (Dict[int, Link]): リンクIDをキーとするリンクの辞書
    """

    def __init__(self):
        """
        トポロジマネージャの初期化
        """
        self.nodes: Dict[int, Node] = {}
        self.links: Dict[int, Link] = {}

    def load_topology(self, yaml_file: str):
        """
        YAMLファイルからトポロジを読み込む

        Args:
            yaml_file (str): トポロジ定義のYAMLファイルパス
        """
        with open(yaml_file, 'r', encoding='utf-8') as file:
            topology_data = yaml.safe_load(file)

        # ノードの読み込み
        for node_data in topology_data.get('nodes', []):
            node = Node(node_id=node_data['id'])
            self.nodes[node.node_id] = node

        # リンクの読み込み
        for link_data in topology_data.get('links', []):
            link = Link(
                link_id=link_data['id'],
                capacity=link_data['capacity'],
                delay=link_data['delay'],
                jitter=link_data['jitter'],
                connected_nodes=(link_data['node1'], link_data['node2'])
            )
            self.links[link.link_id] = link

            # 隣接リンクの設定
            self.nodes[link.connected_nodes[0]].adjacent_links.append(link.link_id)
            self.nodes[link.connected_nodes[1]].adjacent_links.append(link.link_id)

    def get_node(self, node_id: int) -> Optional[Node]:
        """
        ノードIDからノードを取得

        Args:
            node_id (int): ノードID

        Returns:
            Optional[Node]: ノードオブジェクトまたはNone
        """
        return self.nodes.get(node_id)

    def get_link(self, link_id: int) -> Optional[Link]:
        """
        リンクIDからリンクを取得

        Args:
            link_id (int): リンクID

        Returns:
            Optional[Link]: リンクオブジェクトまたはNone
        """
        return self.links.get(link_id)
