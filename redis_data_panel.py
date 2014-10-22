# -*- coding: utf-8 -*-
#import re
import wx

class RedisDataGrid(wx.grid.Grid):
    KEY_COL = 0
    DATA_TYPE_COL = 1
    VALUE_COL = 2

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
        self.SetCellValue(0, self.KEY_COL, "Key")
        self.SetCellValue(0, self.DATA_TYPE_COL, "Data Type")
        self.SetCellValue(0, self.VALUE_COL, "Value")

        self._bind()
    
    def _bind(self):        
        # セルの内容を変更
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self._onCellCange)
        
        # 右クリックでメニュー表示
        self.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self._on_right_up)
        self.Bind(wx.EVT_RIGHT_UP, self._on_right_up)
    
    def _on_right_up(self, evt):
        """
        右クリックメニュー
        """

        if not hasattr(self, "popup_id1"):
            self.popup_id1 = wx.NewId()
            self.Bind(wx.EVT_MENU, self._delete_data, id=self.popupID1)
        
        menu = wx.Menu()
        menu.Append(self.popup_id1, u"削除")
        self.PopupMenu(menu)
        menu.Destroy()

    def _delete_data(self, evt):
        print "delete event"
        pass

    def _onCellCange(self, evt):
        row = evt.GetRow()
        col = evt.GetCol()

        #TODO KEYが変更されたときの仕様
        value = self.GetCellValue(row, col)
        key = self.GetCellValue(row, self.KEY_COL)

        #list_match = re.compile('^\[[^\[|\]]*]$')

        setattr(self._redis, key, value)

    def generate_redis_data_grid(self, redis, callback=None):
        self._redis = redis
        self._data = self._redis.get_all(key=True)
        self._clear_grid(1)
        self._generate_redis_data_grid()

        if callback:
            callback()

    def _generate_redis_data_grid(self):
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

    def _clear_grid(self, num=None):
        self._update_last_line(num)
        self.ClearGrid()

    def search_key_result(self, key):
        if not self._redis:
            return

        keys = self._redis.keys(key)
        datas = self._redis.get_by_keys(keys)
        grid_data = []
        for i,data in enumerate(datas):
            grid_data.append([keys[i], data])

        self._data = grid_data
        self._clear_grid(1)
        self._generate_redis_data_grid()

    def _update_last_line(self, num=None):
        if num:
            self._last_line = num
        else:
            self._last_line += 1

    def clear_data(self):
        self.ClearGrid()

    def get_redis(self):
        return self._redis

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

    def search_key_result(self, key):
        self._rgrid.search_key_result(key)

    def get_redis(self):
        return self._rgrid.get_redis

