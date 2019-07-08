import asyncio
import aioxmpp
import random
from stationary_agent import StationaryAgent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import util


class RecvBehav(CyclicBehaviour):

    def __init__(self, locations):
        super().__init__()
        self.locations = locations

    async def run(self):
        offline_prob = random.randint(0, 100) / 100
        if offline_prob < 0.2:
            self.presence.set_unavailable()
            util.mas_print_data('state|hq|offline')
            util.mas_print_info("HQ went offline")
        else:
            if not self.presence.is_available():
                self.presence.set_available(show=aioxmpp.PresenceShow.CHAT)
                util.mas_print_data('state|hq|online')
                util.mas_print_info("HQ back online")

        msg = await self.receive(timeout=1)  # wait for a message for 10 seconds
        if msg:
            util.mas_print_info("[HQ] received message with content: {}".format(msg.body))
            payload = msg.body.split('|')
            x = int(payload[3])
            y = int(payload[4])

            for agent, data in self.locations.items():
                if agent.startswith('missile') and util.circle_contains(data['x'], data['y'], data['range'], x, y):
                    to = agent + '@xmpp.test'
                    missile_msg = Message(to=to)  # Instantiate the message
                    missile_msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                    missile_msg.body = msg.body  # Set the message content

                    util.mas_print_data('msg|hq|{}|{}'.format(agent, msg.body))
                    util.mas_print_info("[HQ] forwarded message '{}' to [{}]".format(msg.body, agent))
                    await self.send(missile_msg)

        await asyncio.sleep(util.step_delay)


class HqAgent(StationaryAgent):

    def __init__(self, aid, locations):
        super().__init__(aid)
        self.locations = locations

    async def setup(self):
        util.mas_print_info("[HQ] {} starting...".format(self.aid))

        b = RecvBehav(self.locations)
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
        self.presence.set_available(show=aioxmpp.PresenceShow.CHAT)
        # self.presence.set_unavailable()
