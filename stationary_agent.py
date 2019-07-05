from spade.agent import Agent
import util


class StationaryAgent(Agent):
    aid = ''
    pos_x = 0
    pos_y = 0

    def __init__(self, aid):
        super(StationaryAgent, self).__init__(util.jid(aid), 'secret1231')
        self.aid = aid

    def set_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
