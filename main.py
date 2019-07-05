import time
from hq_agent import HqAgent
from radar_agent import RadarAgent
from missile_agent import MissileAgent
import util


geo = {
    'hq': {'x': 0, 'y': 0},
    'radar1': {'x': 25, 'y': 25, 'range': 100},
    'radar2': {'x': -100, 'y': 100, 'range': 100},
    'missile1': {'x': 50, 'y': 50, 'range': 75},
    'missile2': {'x': -50, 'y': -50, 'range': 75},
}


class Timeline:
    def __init__(self):
        self.data = [
            {'id': 1, 'object': 'plane', 'type': 'enemy', 'x': -20, 'y': -20},
            {'id': 2, 'object': 'missile', 'type': 'enemy', 'x': -20, 'y': -20},
            {'id': 3, 'object': 'plane', 'type': 'enemy', 'x': 40, 'y': 40},
        ]
        self.time = 0

    def next(self):
        if len(self.data) == self.time:
            return False

        instance = self.data[self.time]
        self.time += 1

        return instance


if __name__ == "__main__":
    timeline = Timeline()

    hq = HqAgent('hq', geo)
    hq_future = hq.start()
    util.start_web(hq)

    m1 = MissileAgent('missile1')
    m1_future = m1.start()
    util.start_web(m1)

    m2 = MissileAgent('missile2')
    m2_future = m2.start()
    util.start_web(m2)

    # Wait for hq & missiles to be prepared
    hq_future.result()
    m1_future.result()
    m2_future.result()

    r1 = RadarAgent('radar1', timeline)
    r1.start()
    util.start_web(r1)

    r2 = RadarAgent('radar2', timeline)
    r2.start()
    util.start_web(r2)

    print("Wait until user interrupts with ctrl+C")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    hq.stop()
    m1.stop()
    m2.stop()
    r1.stop()
    r2.stop()
