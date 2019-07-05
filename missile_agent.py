from spade.behaviour import CyclicBehaviour
from spade.template import Template
from stationary_agent import StationaryAgent


class RecvBehav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)  # wait for a message for 10 seconds
        if msg:
            print("Message received with content: {}".format(msg.body))
            parts = msg.body.split('|')

            if parts[2] == 'enemy':
                print("Firing missile to enemy {} at ({}, {})".format(parts[0], parts[3], parts[4]))


class MissileAgent(StationaryAgent):
    async def setup(self):
        print("MissileAgent {} starting...".format(self.aid))

        b = RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
