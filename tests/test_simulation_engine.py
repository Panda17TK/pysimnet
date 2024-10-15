# tests/test_simulation_engine.py

import unittest
from simulation_engine import SimulationEngine, Event

class TestSimulationEngine(unittest.TestCase):
    """
    SimulationEngineクラスのユニットテストクラス
    """

    def setUp(self):
        """
        各テストメソッドの前に実行されるセットアップメソッド
        """
        self.engine = SimulationEngine()

    def test_initialize(self):
        """
        initializeメソッドのテスト
        """
        simulation_time = 100.0
        self.engine.initialize(simulation_time)
        self.assertEqual(self.engine.current_time, 0.0)
        self.assertEqual(self.engine.simulation_end_time, simulation_time)
        self.assertEqual(len(self.engine.event_queue), 0)

    def test_schedule_event(self):
        """
        schedule_eventメソッドのテスト
        """
        def dummy_event():
            pass

        self.engine.schedule_event(10.0, dummy_event)
        self.assertEqual(len(self.engine.event_queue), 1)
        event = self.engine.event_queue[0]
        self.assertEqual(event.event_time, 10.0)
        self.assertEqual(event.event_function, dummy_event)

    def test_run(self):
        """
        runメソッドのテスト
        """
        self.engine.initialize(50.0)
        event_times = []

        def dummy_event():
            event_times.append(self.engine.current_time)

        # 3つのイベントをスケジュール
        self.engine.schedule_event(10.0, dummy_event)
        self.engine.schedule_event(20.0, dummy_event)
        self.engine.schedule_event(30.0, dummy_event)

        self.engine.run()

        # イベントが正しい時間に実行されたか確認
        self.assertEqual(event_times, [10.0, 20.0, 30.0])
        self.assertEqual(self.engine.current_time, 30.0)

if __name__ == '__main__':
    unittest.main()
