import time
import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from hq_agent import HqAgent
from radar_agent import RadarAgent
from missile_agent import MissileAgent
import util


geo = {
    'hq': {'x': 0, 'y': 0},
    'missile1': {'x': 50, 'y': 50, 'range': 75},
    'missile2': {'x': -50, 'y': -50, 'range': 75},
}


if __name__ == "__main__":
    hq = HqAgent('hq', geo)
    hq.start()
    util.start_web(hq)

    r1 = RadarAgent('radar1')
    r1.start()
    util.start_web(r1)

    m1 = MissileAgent('missile1')
    m1.start()
    util.start_web(m1)

    print("Wait until user interrupts with ctrl+C")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    # r1.stop()
    # m1.stop()
