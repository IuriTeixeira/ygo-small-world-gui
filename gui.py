import wx
from ygo_small_world import small_world_bridge_generator as sw
from ygo_small_world import graph_adjacency_visualizer as gav
from ygo_small_world import fetch_card_data as fcd

import wx
import wx.grid

class TableInverse(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self, parent, -1, title="Bridges (Inverted)", size=(1000,720))

        #self.SetIcon(wx.Icon("resources/icon.ico"))

        self.tabela = wx.grid.Grid(self)
        self.tabela.CreateGrid(1000, 8)
        self.tabela.UseNativeColHeader(True)
        self.tabela.EnableDragColSize(True)
        self.tabela.SetColLabelValue(0,"Bridge Score")
        self.tabela.SetColLabelValue(1,"Number of Connections")
        self.tabela.SetColLabelValue(2,"Name")
        self.tabela.SetColLabelValue(3,"Type")
        self.tabela.SetColLabelValue(4,"Attribute")
        self.tabela.SetColLabelValue(5,"Level")
        self.tabela.SetColLabelValue(6,"ATK")
        self.tabela.SetColLabelValue(7,"DEF")
        self.tabela.AutoSize()

        #clears table
        for i in range(1000):
            for j in range(8):
                self.tabela.SetCellValue(i,j,'')
        
        #fills table
        bridges = sw.find_best_bridges_from_ydk(parent.deck, top=1000)
        for i in range(0,1000):
            for j in range(0,8):
                self.tabela.SetCellValue(999-i,j,str(bridges.iloc[i,j]))
        self.tabela.AutoSize()
        
class Table(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self, parent, -1, title="Bridges", size=(1000,720))

        #self.SetIcon(wx.Icon("resources/icon.ico"))

        self.tabela = wx.grid.Grid(self)
        self.tabela.CreateGrid(1000, 8)
        self.tabela.UseNativeColHeader(True)
        self.tabela.EnableDragColSize(True)
        self.tabela.SetColLabelValue(0,"Bridge Score")
        self.tabela.SetColLabelValue(1,"Number of Connections")
        self.tabela.SetColLabelValue(2,"Name")
        self.tabela.SetColLabelValue(3,"Type")
        self.tabela.SetColLabelValue(4,"Attribute")
        self.tabela.SetColLabelValue(5,"Level")
        self.tabela.SetColLabelValue(6,"ATK")
        self.tabela.SetColLabelValue(7,"DEF")
        self.tabela.AutoSize()

        #clears table
        for i in range(1000):
            for j in range(8):
                self.tabela.SetCellValue(i,j,'')
        
        #fills table
        bridges = sw.find_best_bridges_from_ydk(parent.deck, top=1000)
        for i in range(0,1000):
            for j in range(0,8):
                self.tabela.SetCellValue(i,j,str(bridges.iloc[i,j]))
        self.tabela.AutoSize()

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, title="Yu-Gi-Oh! Small World tool", size=(100,100))

        #self.SetIcon(wx.Icon("resources/icon.ico"))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.deck = None
        self.buttonDeck = wx.Button(self, label='Select Deck')
        grid.Add(self.buttonDeck,pos=(1,0))
        self.Bind(wx.EVT_BUTTON, self.onButtonDeck, self.buttonDeck)
        
        self.buttonBridges = wx.Button(self, label='Show Bridges')
        grid.Add(self.buttonBridges,pos=(1,1))
        self.Bind(wx.EVT_BUTTON, self.onButtonBridges, self.buttonBridges)

        self.buttonBridgesInverse = wx.Button(self, label='Show Bridges (Invert Order)')
        grid.Add(self.buttonBridgesInverse,pos=(1,2))
        self.Bind(wx.EVT_BUTTON, self.onButtonBridgesInverse, self.buttonBridgesInverse)

        self.buttonGraph = wx.Button(self, label="Graph")
        grid.Add(self.buttonGraph,pos=(1,3))
        self.Bind(wx.EVT_BUTTON, self.onButtonGraph, self.buttonGraph)

        self.buttonUpdate = wx.Button(self, label="Update Data")
        grid.Add(self.buttonUpdate,pos=(1,4))
        self.Bind(wx.EVT_BUTTON, self.onButtonUpdate, self.buttonUpdate)

        self.dirname = ''
        self.lblDeckMissing = wx.StaticText(self,-1, "Please select a .ydk deck file")
        self.lblDeckMissing.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        self.lblDeckMissing.SetForegroundColour(wx.Colour(200,0,0))
        grid.Add(self.lblDeckMissing,pos=(3,0),span=(1,5))

        self.lblUpdate = wx.StaticText(self,-1,"")
        self.lblUpdate.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        grid.Add(self.lblUpdate,pos=(2,0),span=(1,5))
        
        hSizer.Add(grid, 0, wx.ALIGN_LEFT, 10)
        mainSizer.Add(hSizer, 0, wx.ALIGN_TOP, 10)
        self.SetSizerAndFit(mainSizer)

        self.Show()

    def onButtonDeck(self, event):
        self.lblUpdate.SetLabel("")
        dlg = wx.FileDialog(self, "Choose a .ydk deck file", self.dirname, "", "*.ydk", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.deck = self.dirname + '\\' + self.filename
        dlg.Destroy()
        self.lblDeckMissing.SetLabel('')
    
    def onButtonBridges(self,event):
        self.lblUpdate.SetLabel("")
        if(self.deck):
            self.tabela = Table(self)
            self.tabela.Show()

    def onButtonBridgesInverse(self,event):
        self.lblUpdate.SetLabel("")
        if(self.deck):
            self.tabela = TableInverse(self)
            self.tabela.Show()
    
    def onButtonGraph(self, event):
        self.lblUpdate.SetLabel("")
        if(self.deck):
            #self.graph = Graph(self)
            self.graph = gav.ydk_to_graph(self.deck)
            gav.plot_graph(self.graph)
    
    def onButtonUpdate(self, event):
        fcd.fetch_card_data()
        self.lblUpdate.SetLabel("Card data updated!")
        
class Graph(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self, parent, -1, title="Small World Graph", size=(500,500))
        self.graph = gav.ydk_to_graph(self.deck)
        gav.plot_graph(self.graph)
        self.png = wx.StaticBitmap(self, -1, wx.Bitmap("graph_image.png", wx.BITMAP_TYPE_ANY))

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()