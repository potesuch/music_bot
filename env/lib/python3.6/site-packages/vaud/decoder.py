class Decoder:  # DON'T SEE HERE!
    n = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN0PQRSTUVWXYZO123456789+/='
    uid = 0

    def __init__(self, user_id):
        if user_id < 1:
            raise AttributeError('Invalid uid!')
        self.uid = int(user_id)

    @staticmethod
    def _sort_object(e):
        items = sorted(e.items(), key=lambda a: a[0])
        return [i[1] for i in items]

    @staticmethod
    def v(e):
        return ''.join(list(e)[::-1])

    @classmethod
    def r(cls, e, t):
        e = list(e)
        o = cls.n * 2
        a = len(e)
        while a:
            a -= 1
            i = o.find(e[a])
            if ~i:
                e[a] = o[i - t]
        return ''.join(e)

    @classmethod
    def s(cls, e, t):
        e_length = len(e)
        if e_length:
            i = cls.decode_s(e, t)
            o = 1
            e = list(e)
            while o < e_length:
                _, e = cls.splice(e, i[e_length - 1 - o], 1, e[o])
                e[o] = _[0]
                o += 1
            e = ''.join(e)
        return e

    def i(self, e, t):
        try:
            return self.s(e, int(t) ^ self.uid)
        except ValueError:
            return e

    @staticmethod
    def x(e, t):
        data = ''
        t = ord(t[0])
        for i in e:
            data += chr(ord(i[0]) ^ t)
        return data

    @classmethod
    def splice(cls, a, b, c, *d):
        if isinstance(b, (tuple, list)):
            return cls.splice(a, b[0], b[1], c, *d)
        c += b
        cash = list(a)
        a = a[b:c]
        d = list(d)
        cash = cash[:b] + d + cash[c:]
        return a, cash

    @classmethod
    def decode_s(cls, e, t):
        e_length = len(e)
        i = {}
        if e_length:
            o = e_length
            t = abs(t)
            while o:
                o -= 1
                t = (e_length * (o + 1) ^ int(t) + o) % e_length
                i[o] = t

        return cls._sort_object(i)

    @classmethod
    def decode_r(cls, e):
        if not e or len(e) % 4 == 1:
            return False
        o = 0
        a = 0
        t = 0
        r = ''
        e_length = len(e)
        while a < e_length:
            i = cls.n.find(e[a])
            if ~i:
                t = 64 * t + i if o % 4 else i
                o += 1
                if (o-1) % 4:
                    c = chr(255 & t >> (-2 * o & 6))
                    if c != '\x00':
                        r += c
            a += 1
        return r

    def decode(self, url):
        if ~url.find('audio_api_unavailable'):
            t = url.split('?extra=')[1].split('#')
            n = '' if '' == t[1] else self.decode_r(t[1])
            t = self.decode_r(t[0])
            if not isinstance(n, str) or not t:
                return url
            n = n.split(chr(9)) if n else []
            len_n = len(n)
            while len_n:
                len_n -= 1
                s = n[len_n].split(chr(11))
                a, s = self.splice(s, 0, 1, t)
                _ = getattr(self, a[0], None)
                if not _ or len(s) < 2:
                    return url
                t = _(*s)
            if t[:4] == 'http':
                return t
        return url
