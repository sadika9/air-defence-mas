import asyncio
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from stationary_agent import StationaryAgent
import util


class RecvBehav(CyclicBehaviour):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.destroyed_items = []

    async def run(self):
        msg = await self.receive(timeout=1)  # wait for a message for 10 seconds
        if msg:
            util.mas_print_info("[MISSILE] ({}) received message with content: {}".format(self.name, msg.body))
            parts = msg.body.split('|')

            if parts[2] == 'enemy' and not parts[1] in self.destroyed_items:
                self.destroyed_items.append(parts[1])
                util.mas_print_data('fire|{}|{}'.format(self.name, msg.body))
                util.mas_print_info("[MISSILE] ({}) Firing missile to enemy {} at ({}, {})".format(self.name, parts[0], parts[3], parts[4]))

        await asyncio.sleep(util.step_delay)


class MissileAgent(StationaryAgent):
    async def setup(self):
        util.mas_print_info("[MISSILE] ({}) starting...".format(self.aid))

        b = RecvBehav(self.aid)
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
