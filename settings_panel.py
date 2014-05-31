# -*- coding: utf-8 -*-
import wx
from attributeredis import AttributeRedis

class RedisData(AttributeRedis):
    pass

class SettingsPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        self._lock = False
        self._parent = parent
        self._redis_connect_button = wx.Button(self, -1, u'接続', (360, 15))

        self.st_host = wx.StaticText(self, -1, "Host Name:", pos=(20,20))
        self._host_name_box = wx.TextCtrl(self, wx.ID_ANY, 'localhost', pos=(100, 20))

        self.st_port = wx.StaticText(self, -1, "Port:", pos=(210,20))
        self._port_box  = wx.TextCtrl(self, wx.ID_ANY, '6379', pos=(245, 20))

        #検索用パーツ
        self.st_host = wx.StaticText(self, -1, u"Key検索:", pos=(20,58))
        self._search_key_box = wx.TextCtrl(self, wx.ID_ANY, '', pos=(100, 55))
        self._search_button = wx.Button(self, -1, u'検索', (360, 55))


        self._bind()

    def _bind(self):
        self.Bind(wx.EVT_BUTTON, self.redis_connect, id=self._redis_connect_button.GetId())
        self.Bind(wx.EVT_BUTTON, self.redis_connect, id=self._search_button.GetId())
    
    def search_by_key(self, event):
        if not self._parent.GetParent().get_redis_connection():
           wx.MessageBox('Redis Can Not Be Found', 'Warning')
           return

        if self._search_key_box.IsEmpty():
           return

        key = self._search_key_box.GetValue()

    def redis_connect(self, event):
        if self._lock:
            wx.MessageBox('Please wait! It is generated in the data grid.', 'Warning')
            return

        #TODO バリデーション
        if self._port_box.IsEmpty() or self._host_name_box.IsEmpty():
            wx.MessageBox('Host Name or Port Number is Empty.', 'Error')
            return

        port_number = self._port_box.GetValue()
        host_name = self._host_name_box.GetValue()

        redis = RedisData(host_name, int(port_number), class_name=False)
        #TODO 親にインスタンスを投げて、親からredisパネルに渡すようにする
        self._parent.GetParent().redis_data_panel.generate_redis_data_grid(redis)

    def update_lock_flag(self, value):
        self._lock = value

