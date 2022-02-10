import wx;
import ui_login;

class App(wx.App):
    def onInit(self):
        frame=ui_login.LoginWindow(parent=None,title='系统登录');
        frame.Show();
        frame.Centre();
        return True
if __name__ == '__main__':
   app=App()
   app.onInit();
   app.MainLoop();

