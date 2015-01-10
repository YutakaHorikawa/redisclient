# -*- coding: utf-8 -*-
import wx
import wx.grid
import wx.lib.gridmovers
from settings_panel import SettingsPanel
from redis_data_panel import RedisDataPanel

# 接続画面
STATUS_CONNECTION_WINDOW = 1

# ビュワーモード
STATUS_CONNECTION_VIEWER = 2

# 接続中
STATUS_CONNECTION = 3

class Sider(wx.Frame):
    """
    画面の状態を管理して表示を切り替える
    """

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title=title, style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN, size=(1000, 800), pos=wx.DefaultPosition)
        self._redis = None
        self._status = STATUS_CONNECTION_WINDOW
        self.Centre()
        self.draw()

    def set_redis_connection(self, redis):
        self._redis = redis

    def get_redis_connection(self):
        return self.redis_data_panel.get_redis()

    def draw(self):
        """
        GUIの描画statusによって画面が切り替わる
        """
        panel = wx.Panel(self, -1)
        #Redisへの接続用パーツなど
        self.settings_panel = SettingsPanel(panel, -1)
        #Redisのデータを表示するパネル
        self.redis_data_panel = RedisDataPanel(panel, -1)

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.settings_panel, 1, wx.EXPAND | wx.ALL, 5)
        layout.Add(self.redis_data_panel, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(layout)
        
        self.Show(True)

app = wx.App()
Sider(None, -1, 'Sider')
app.MainLoop()
