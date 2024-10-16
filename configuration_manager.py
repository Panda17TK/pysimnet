import os
if os.name == 'nt':
    import _locale
    _locale._getdefaultlocale_backup = _locale._getdefaultlocale
    _locale._getdefaultlocale = (lambda *args: (_locale._getdefaultlocale_backup()[0], 'UTF-8'))

import yaml
from typing import Dict

class ConfigurationManager:
    """
    設定管理クラス

    Attributes:
        simulation_parameters (Dict): シミュレーション全体のパラメータ
        flow_scenario (Dict): フロー生成に関する設定
    """

    def __init__(self):
        self.simulation_parameters = {}
        self.flow_scenario = {}

    def load_configuration(self, config_file: str):
        """
        設定ファイルからシミュレーションパラメータを読み込む

        Args:
            config_file (str): 設定ファイルパス
        """
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)
            self.simulation_parameters = config_data.get('simulation_parameters', {})
            self.flow_scenario = config_data.get('flow_scenario', {})

    def save_flow_scenario(self, yaml_file: str, flow_scenario: Dict):
        """
        フローシナリオをYAML形式で保存

        Args:
            yaml_file (str): 保存先のYAMLファイルパス
            flow_scenario (Dict): フローシナリオの辞書
        """
        with open(yaml_file, 'w') as file:
            yaml.dump({'flows': flow_scenario}, file)
