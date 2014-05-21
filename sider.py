# -*- coding: utf-8 -*-
import wx
import wx.grid
import wx.lib.gridmovers
from attributeredis import AttributeRedis
from settings_panel import SettingsPanel
from redis_data_panel import RedisDataPanel

class RedisData(AttributeRedis):
    pass

class Sider(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title=title, style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN, size=(1000, 800), pos=wx.DefaultPosition)
        self._redis = None

        panel = wx.Panel(self, -1)
        #Redisへの接続用パーツなど
        self.settings_panel = SettingsPanel(panel, -1)
        #Redisのデータを表示するパネル
        self.redis_data_panel = RedisDataPanel(panel, -1)

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.settings_panel, 1, wx.EXPAND | wx.ALL, 5)
        layout.Add(self.redis_data_panel, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(layout)

        self.Centre()
        self.Show(True)

    def set_redis_connection(self, redis):
        self._redis = redis

app = wx.App()
Sider(None, -1, 'Sider')
app.MainLoop()
