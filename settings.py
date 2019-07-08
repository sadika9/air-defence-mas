__password = 'secret1231'

xmpp_users = {
    'hq': {
        'username': 'hq',
        'password': __password
    },
    'radar1': {
        'username': 'radar1',
        'password': __password
    },
    'radar2': {
        'username': 'radar2',
        'password': __password
    },
    'missile1': {
        'username': 'missile1',
        'password': __password
    },
    'missile2': {
        'username': 'missile2',
        'password': __password
    },
}

print_data = True
print_info = False

geo = {
    'hq': {'x': 0, 'y': 0},
    'radar1': {'x': 25, 'y': 25, 'range': 100},
    'radar2': {'x': -100, 'y': 100, 'range': 100},
    'missile1': {'x': 50, 'y': 50, 'range': 300},
    'missile2': {'x': -50, 'y': -50, 'range': 250},
}
