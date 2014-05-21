# -*- coding: utf-8 -*-
import wx

class RedisDataGrid(wx.grid.Grid):

    def __init__(self, parent, id):
        wx.grid.Grid.__init__(self, parent, id, size=(1000, 500))
        self._redis = None
        self._data = None
        self._last_line = 1

        self.CreateGrid(2,3)
        self.SetColLabelSize(0)
        self.SetRowLabelSize(0)
        
        #セルの横幅を指定
        self.SetColSize(0, 350)
        self.SetColSize(1, 350)
        self.SetColSize(2, 350)
        
        #ラベルの設定
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

