# tests/test_configuration_manager.py

import unittest
from configuration_manager import ConfigurationManager
import os

class TestConfigurationManager(unittest.TestCase):
    """
    ConfigurationManagerクラスのユニットテストクラス
    """

    def setUp(self):
        self.config_manager = ConfigurationManager()
        # テスト用の設定ファイルを作成
        self.test_config_file = 'tests/test_config.yaml'
        with open(self.test_config_file, 'w') as f:
            f.write('''
simulation_parameters:
  simulation_time: 500.0
  failure_rate: 0.02
  failure_distribution: "exponential"
  algorithm: "dqn"
''')

    def test_load_configuration(self):
        """
        load_configurationメソッドのテスト
        """
        self.config_manager.load_configuration(self.test_config_file)
        self.assertEqual(self.config_manager.simulation_parameters['simulation_time'], 500.0)
        self.assertEqual(self.config_manager.simulation_parameters['algorithm'], "dqn")

    def tearDown(self):
        # テスト用の設定ファイルを削除
        os.remove(self.test_config_file)

if __name__ == '__main__':
    unittest.main()
