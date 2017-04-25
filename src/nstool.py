#!/usr/bin/env python

import dns.resolver
import dns.reversename
import wx

class nsTool(wx.Frame):
    
    # Constructor 
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self,parent, id, 'nsTool', size=(500,350))
        panel = wx.Panel(self)   
  
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)  
        font.SetPointSize(9)      

        button = wx.Button(panel, 10, label='Check')
        buttonClear = wx.Button(panel, 11, label='Clear')    
        buttonHelp = wx.Button(panel, 12, label='Help')
   
        self.outputBox = wx.TextCtrl(panel, style=wx.VSCROLL|wx.TE_MULTILINE)
                
        self.Bind(wx.EVT_BUTTON, self.lookUp, button)  
        self.Bind(wx.EVT_BUTTON, self.OnClear, buttonClear)
        self.Bind(wx.EVT_BUTTON, self.OnHelp, buttonHelp)
        wx.EVT_TEXT_ENTER(panel, 200, self.lookUp)
        
        self.userInput = wx.TextCtrl(panel, 200, style=wx.TE_PROCESS_ENTER)
        self.userInput.SetMaxLength(100)
        
        self.A = wx.RadioButton(panel, 1, 'A')        
        self.NS = wx.RadioButton(panel, 2, 'NS')        
        self.CNAME = wx.RadioButton(panel, 3, 'CNAME')
        self.MX = wx.RadioButton(panel, 4, 'MX')
        self.PTR = wx.RadioButton(panel, 4, 'PTR')
        self.A.SetFont(font)
        self.NS.SetFont(font)
        self.CNAME.SetFont(font)
        self.MX.SetFont(font)
        self.PTR.SetFont(font)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        st1 = wx.StaticText(panel, label='Check:')
        st1.SetFont(font)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        hbox1.Add(self.userInput, proportion=1)               
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        vbox.Add((-1, 10))
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.A)
        hbox2.Add(self.CNAME)
        hbox2.Add(self.NS)
        hbox2.Add(self.MX)    
        hbox2.Add(self.PTR)    
        vbox.Add(hbox2, flag=wx.CENTER, border=10)
        
        vbox.Add((-1, 10))
        
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(button, flag=wx.LEFT|wx.BOTTOM, border=5)
        hbox3.Add(buttonClear, flag=wx.LEFT|wx.BOTTOM, border=5)
        hbox3.Add(buttonHelp, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER|wx.CENTER, border=10)
        
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='Results:')
        st2.SetFont(font)
        hbox4.Add(st2)
        vbox.Add(hbox4, flag=wx.LEFT | wx.TOP, border=10)
        
        vbox.Add((-1, 5))
             
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5.Add(self.outputBox, proportion=1, flag=wx.EXPAND)
        self.outputBox.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.LIGHT, face='Fixedsys'))
        self.outputBox.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.outputBox.SetForegroundColour(wx.Colour(255, 255, 255))
        
        vbox.Add(hbox5, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)
        
        vbox.Add((-1, 10))    
            
        panel.SetSizer(vbox)
        
    # Methods
                   
    def lookUp(self, event):
              
        self.outputBox.Clear()
        input = self.userInput.GetValue()
        
        if self.A.GetValue():
            try:
                resp = dns.resolver.query(input,rdtype='A')
                if str(resp.canonical_name) != str(resp.qname):
                    message = 'WARNING, there is a CNAME on ' + input + ': \n' + str(resp.rrset)
                else:
                    message = str(resp.rrset)
                self.outputBox.SetValue(message)
            except:
                error = 'NXDOMAIN, non-existing domain!'
                self.outputBox.SetValue(error)
        elif self.NS.GetValue(): 
            try:
                resp = dns.resolver.query(input, rdtype='NS')
                message = str(resp.rrset)
                self.outputBox.SetValue(message)
            except:
                error = 'Error in NS-record lookup!'
                self.outputBox.SetValue(error)
        elif self.CNAME.GetValue():        
            try:
                resp = dns.resolver.query(input, rdtype='CNAME')
                message = str(resp.rrset)
                self.outputBox.SetValue(message)
            except:
                error = 'Error in CNAME-record lookup!'
                self.outputBox.SetValue(error)
        elif self.MX.GetValue():
            try:
                resp = dns.resolver.query(input, rdtype='MX') 
                message = str(resp.rrset)
                self.outputBox.SetValue(message)
            except:                
                error = 'Error in MX lookup!'
                self.outputBox.SetValue(error)
        elif self.PTR.GetValue():
            try:
                resp = dns.resolver.query(dns.reversename.from_address(input), 'PTR')
                message = str(resp.rrset)
                self.outputBox.SetValue(message)
            except:
                error = 'Error in PTR lookup!'
                self.outputBox.SetValue(error)
        else:
            message = 'Please try again!'
            self.outputBox.SetValue(message)
            
    def OnClear(self, event):
        self.outputBox.Clear()
        self.userInput.Clear()

    def OnQuit(self, event):
        self.Close()
    
    def OnHelp(self, event):
        mess = """
        A small NS-tool!
        
        Version: 0.1
        """
        
        box = wx.MessageDialog(None, mess,'Help',wx.OK)
        box.ShowModal()
        box.Destroy()
                                         
if __name__=='__main__':
    app = wx.App()
    frame = nsTool(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
