password = 'secret1231'
step_delay = 2


def jid(username):
    return username + '@xmpp.test'


def start_web(agent):
    username = str(agent.jid).split('@')[0]

    if username == 'admin':
        port = "10000"
    elif username == 'hq':
        port = "20000"
    else:
        if username.startswith('missile'):
            n = int(username[7:]) + 200
        elif username.startswith('radar'):
            n = int(username[5:]) + 100
        else:
            n = username[1:]
        port = str(10000 + int(n))

    agent.web.start(hostname='127.0.0.1', port=port)


def circle_contains(center_x, center_y, radius, point_x, point_y):
    z = (point_x - center_x)**2 + (point_y - center_y)**2

    return z <= radius**2
