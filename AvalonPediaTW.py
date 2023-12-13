import wx
import datetime
import random

class RoleAssignmentApp(wx.App):
    def OnInit(self):
        self.frame = RoleAssignmentFrame(None, title="角色分配")
        self.frame.SetIcon(wx.Icon('hsin.ico'))
        self.SetTopWindow(self.frame)
        self.frame.Show()        
        return True

class RoleAssignmentFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        super(RoleAssignmentFrame, self).__init__(parent, id, title, pos, size, style)

        self.panel = wx.Panel(self)
        self.text_ctrl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE|wx.TE_READONLY)

        self.assign_roles()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND)
        self.panel.SetSizer(sizer)
        
        self.reset_button = wx.Button(self.panel, label="重新產生")
        sizer.Add(self.reset_button, flag=wx.ALIGN_LEFT)
        
        self.save_button = wx.Button(self.panel, label="保存結果")
        sizer.Add(self.save_button, flag=wx.ALIGN_RIGHT)
        
        self.Bind(wx.EVT_BUTTON, self.on_reset_button_click, self.reset_button)
        self.Bind(wx.EVT_BUTTON, self.on_save_button_click, self.save_button)        

    def assign_roles(self):
        now = datetime.datetime.now()
        timestamp = now.strftime("%m%d_%H%M%S")
        filename_txt = timestamp + '_output.txt'
    
        players = ['梅林', '雜魚', '雜魚', '莫德雷德', '奧伯倫', '魔甘娜', '雜魚', '雜魚', '派西維爾', '刺客']
        num_players = len(players)
        random.shuffle(players)
    
        player_indices = {player: i + 1 for i, player in enumerate(players)}
    
        red_information = {
            '莫德雷德': [player_indices['刺客'], player_indices['魔甘娜']],
            '刺客': [player_indices['莫德雷德'], player_indices['魔甘娜']],
            '魔甘娜': [player_indices['刺客'], player_indices['莫德雷德']]
        }
    
        merlin_information = {
            '梅林': [player_indices['奧伯倫'], player_indices['刺客'], player_indices['魔甘娜']]
        }
    
        percival_information = {
            '派西維爾': [player_indices['梅林'], player_indices['魔甘娜']]
        }
    
        role_information = {
            **red_information,
            **merlin_information,
            **percival_information
        }
    
        output_lines = []
        for i in range(num_players):
            player = players[i]
            player_num = i + 1 if i != 9 else 0
            role_info = role_information.get(player, [])
            if 0 in role_info:
                role_info.remove(0)
                role_info.append(player_indices['魔甘娜'])
            role_info = sorted(role_info)  # 將數字排序
            role_info_str = f"[{', '.join(map(lambda x: '0' if x == 10 else str(x), role_info))}]" if role_info else ""
            output_line = f"玩家{player_num}: {player}{role_info_str}"
            output_lines.append(output_line)
    
        self.text_ctrl.SetValue('\n'.join(output_lines))
        self.filename_txt = filename_txt

    def on_reset_button_click(self, event):
        self.text_ctrl.SetValue("")
        self.assign_roles()
    
    def on_save_button_click(self, event):
        with open(self.filename_txt, 'w') as f:
            f.write(self.text_ctrl.GetValue())
        wx.MessageBox("結果已保存到文件中！", "保存成功", wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = RoleAssignmentApp()
    app.MainLoop()
