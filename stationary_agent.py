from spade.agent import Agent
import util


class StationaryAgent(Agent):
    aid = ''

    def __init__(self, aid):
        super(StationaryAgent, self).__init__(util.jid(aid), 'secret1231')
        self.aid = aid
