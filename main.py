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


if __name__ == "__main__":
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

    r1 = RadarAgent('radar1')
    r1.start()
    util.start_web(r1)

    r2 = RadarAgent('radar2')
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
