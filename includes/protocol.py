import re

class Protocol:
    # actions
    DISCONNECT   = 0
    SIGN_IN      = 10
    SIGN_OUT     = 20
    REGISTER     = 30
    CHAT         = 40

    # data types
    PLAIN_TEXT  = 1
    JSON        = 2
    XML         = 3
    BINARY      = 4

    def send(self, action, type, message):
        data = '{} {} {}'.format(action, type, message)
        return bytes(data, 'utf-8')

    def receive(self, data):
        try:
            matches = re.search('^([0-9]+)\s([0-9]+)\s(.*?)$', str(data, 'utf-8')).groups()
        except Exception:
            matches = (0, 0, str(data, 'utf-8'))

        return {
            'action':  int(matches[0]),
            'type':    int(matches[1]),
            'message': matches[2]
        }