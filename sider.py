# -*- coding: utf-8 -*-
from attributeredis import AttributeRedis
import wx
import wx.grid
import wx.lib.gridmovers

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

        self._bind()

    def _bind(self):
        self.Bind(wx.EVT_BUTTON, self.redis_connect, id=self._redis_connect_button.GetId())

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
        self._parent.GetParent().redis_data_panel.generate_redis_data_grid(redis)

    def update_lock_flag(self, value):
        self._lock = value

class RedisDataGrid(wx.grid.Grid):

    def __init__(self, parent, id):
        wx.grid.Grid.__init__(self, parent, id, size=(1000, 500))
        self._redis = None
        self._data = None
        self._last_line = 1

        self.CreateGrid(2,3)
        self.SetColLabelSize(0)
        self.SetRowLabelSize(0)
        self.SetCellValue(0, 0, "Key")
        self.SetCellValue(0, 1, "Data Type")
        self.SetCellValue(0, 2, "Value")

    def generate_redis_data_grid(self, redis, callback=None):
        self._redis = redis
        self._data = self._redis.get_all(key=True)

        for redis_data in self._data:
            key = redis_data[0]
            value = redis_data[1]
            data_type = type(value).__name__
            try:
                self.SetCellValue(self._last_line, 0, key)
                self.SetCellValue(self._last_line, 1, data_type)
                self.SetCellValue(self._last_line, 2, value)
            except wx._core.PyAssertionError:
                print redis_data
                pass
            else:
                self._update_last_line()
                self.AppendRows(self._last_line)

        if callback:
            callback()

    def _update_last_line(self):
        self._last_line += 1

    def clear_data(self):
        self.ClearGrid()

class RedisDataPanel(wx.Panel):
    def __init__(self, parent, id):
        self._parent = parent
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        self._rgrid = RedisDataGrid(self, -1)
        grid.Add(self._rgrid, pos=(0,0))
        self.SetSizerAndFit(grid)

    def generate_redis_data_grid(self, redis):
        self._parent.GetParent().settings_panel.update_lock_flag(True)
        self._rgrid.generate_redis_data_grid(redis, lambda: self._parent.GetParent().settings_panel.update_lock_flag(False))

class Sider(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title=title, style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN, size=(1000, 800), pos=wx.DefaultPosition)
        self._redis = None

        panel = wx.Panel(self, -1)
        self.settings_panel = SettingsPanel(panel, -1)
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
