import time
import random
from hq_agent import HqAgent
from radar_agent import RadarAgent
from missile_agent import MissileAgent
import util
import settings


class Timeline:
    def __init__(self):
        self.data = [
            {'id': 10, 'object': 'plane', 'type': 'enemy', 'x': 320, 'y': 320},
            {'id': 20, 'object': 'missile', 'type': 'enemy', 'x': 420, 'y': 420},
            {'id': 33, 'object': 'plane', 'type': 'enemy', 'x': 400, 'y': 400},
            {'id': 50, 'object': 'missile', 'type': 'enemy', 'x': settings.agents['hq']['x'], 'y': settings.agents['hq']['y']},
        ]
        self.time = 0

        objects = ['plane', 'bird', 'missile']
        types = ['enemy', 'friend']

        for i in range(100):
            obj = random.choice(objects)
            typ = random.choice(types)
            if obj == 'bird':
                typ = 'neutral'

            x = random.randint(10, 840)
            y = random.randint(10, 540)

            item = {'id': 100 + i, 'object': obj, 'type': typ, 'x': x, 'y': y}
            self.data.append(item)

    def next(self):
        if len(self.data) == self.time:
            return False

        instance = self.data[self.time]
        self.time += 1

        return instance


if __name__ == "__main__":
    timeline = Timeline()

    hq = HqAgent('hq', settings.agents)
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

    r1 = RadarAgent('radar1', timeline, hq, settings.agents)
    r1.start()
    util.start_web(r1)

    r2 = RadarAgent('radar2', timeline, hq, settings.agents)
    r2.start()
    util.start_web(r2)

    util.mas_print_info("Wait until user interrupts with ctrl+C")
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
