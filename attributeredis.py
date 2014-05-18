# -*- coding: utf-8 -*-
import redis

class AttributeRedis(object):
    """
    class Test(AttributeRedis):
        pass

    t = Test()
    t.attr_name = 1
    print t.attr_name
    
    """

    BASE_KEY = None
    ATTRIBUTES = {
        'hoge': 1,
        'fuga': 2,
    }

    def __init__(self, host="localhost", port=6379, db=0, class_name=True):
        self.__dict__['_r']  = redis.Redis(host=host, port=port, db=db)
        #keyにclass名やBASE_KEYを使用しない
        self.__dict__['_class_name'] = class_name

        for k,v in self.ATTRIBUTES.items():
            tmp = self._get(k)
            ##既にkeyが存在している場合はpass
            if not tmp:
                setattr(self, k, v) 

    def __setattr__(self, name, value):
        self._set(name, value)

    def __getattr__(self, name):
        return self._get(name)
    
    def get_all_keys(self):
        return self._r.keys('*')

    def _get_key(self, key):

        if not self._class_name:
            return key

        if self.BASE_KEY:
            key = "%s:%s:%s" % (self.BASE_KEY, self.__class__.__name__, key)
        else:
            key = "%s:%s" % (self.__class__.__name__, key)

        return key

    def _set(self, key, value):
        key = self._get_key(key)
        self._r.set(key, value)

    def _get(self, key):
        key = self._get_key(key)
        val = self._r.get(key)
        return val

class Test(AttributeRedis):
    pass

if __name__ == "__main__":
    t = Test()
    t.fugafuga = [i for i in range(10)]
    print t.fugafuga
    t.aaaa = "1"
    print t.aaaa
    t.bbbb = 12
    print t.bbbb
