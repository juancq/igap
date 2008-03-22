import wx
import gui.feedbackpanel as feedbackpanel
from iga.gacommon import gaParams

class BlockMaker(feedbackpanel.FeedbackPanel):
    def __init__(self, parent, ID=wx.NewId(), dimensions=[], description=[], transf = [], pos=wx.DefaultPosition, size=(220,260)):
        feedbackpanel.FeedbackPanel.__init__(self,parent,ID,size)

        self.parent = parent
        self.SetBackgroundColour(wx.WHITE)
        self.dimensions=dimensions
        self.description=description
        self.transf = transf
        self.SetMinSize(size)
        self.max_val = 0.3
        self.min_val = -0.3


        appVar = gaParams.getVar('application')
        self.width = appVar['plotSizeX']
        self.height = appVar['plotSizeY']
        self.canvas = wx.Panel(self, size =(self.width, self.height))
        self.canvas.Bind(wx.EVT_PAINT, self.draw)
        
        vsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer.AddSpacer((20,10))
        vsizer.Add(self.canvas)
        self.sizer.Add(vsizer)


#-------------------------------------------#
    def getRoom(self, room_type, x, y):
        '''
        Return a bitmap corresponding to the room type.
        '''
        tmp_room = self.rooms[room_type].Copy()
        tmp_room.Rescale(x, y)

        return tmp_room.ConvertToBitmap()


#-------------------------------------------#
    def getRoomDesc(self):
        coordinates = []
        roomsizes = []
        #xoffset = 25.0
        #yoffset = 40.0
        xoffset = 0.0
        yoffset = 0.0

        for i in xrange(0, len(self.dimensions)):
            coordinates.append(float(self.dimensions[i][0])+xoffset)
            coordinates.append(float(self.dimensions[i][1])+yoffset)
            roomsizes.append(float(self.dimensions[i][2])-float(self.dimensions[i][0]))
            roomsizes.append(float(self.dimensions[i][3])-float(self.dimensions[i][1]))

        return coordinates, roomsizes

#-------------------------------------------#
    def draw(self, event):
        '''
        Draw the document with various shapes, but no overlap (ignore x and y
        deformation values).
        '''
        #dc = wx.PaintDC(self)
        dc = wx.PaintDC(self.canvas)
        coordinates, roomsizes = self.getRoomDesc()

        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        i = 0

        transf = self.transf
        max_val = self.max_val
        min_val = self.min_val

        #dc.SetPen(wx.Pen("black",8))
        #dc.DrawRectangle(coordinates[0], coordinates[1], self.width, self.height)
        dc.SetPen(wx.Pen("black",1))

        for j in xrange(0, len(self.dimensions)):
            if self.description[j] == 'S':
                dc.SetBrush(wx.Brush('white'))

            # RST - Restroom, BTH - Bathroom : FIREBRICK
            elif self.description[j] == 'RST' or self.description[j] == 'BTH':
                dc.SetBrush(wx.Brush('firebrick'))        

            # KTH - Kitchen, DIN - Dining Room : GREEN
            elif self.description[j] == 'KTH' or self.description[j] == 'DIN':
                dc.SetBrush(wx.Brush('green'))            

            # LIV - Living Room, LBK - Living/Bed/Kitchen Combo, LKT - Living/Kitchen Combo : RED
            elif self.description[j] == 'LIV' or self.description[j] == 'LBK' or self.description[j] == 'LKT':
                dc.SetBrush(wx.Brush('red'))              

            # BED - Bed Room : YELLOW
            elif self.description[j] == 'MBR' or self.description[j] == 'GBR' or self.description[j] == 'BED': 
                dc.SetBrush(wx.Brush('yellow'))           

            # Other rooms
            else:
                dc.SetBrush(wx.Brush('dim gray'))         

            # if not a blank space
            shape = transf[j][-1]
            if shape:
                xdiff =  transf[j][0] * (max_val-min_val) + min_val
                ydiff =  transf[j][1] * (max_val-min_val) + min_val
                l = roomsizes[i] - coordinates[i]
                w = roomsizes[i+1] - coordinates[i+1]
                l = float(l) * xdiff * 0.5
                w = float(w) * ydiff * 0.5
                if shape == 1:
                    dc.DrawRectangle(coordinates[i]+l, coordinates[i+1]+w, roomsizes[i]+l, roomsizes[i+1]+w)
                elif shape == 2:
                    dc.DrawRoundedRectangle(coordinates[i]+l, coordinates[i+1]+w, roomsizes[i]+l, roomsizes[i+1]+w, 5.)
                elif shape == 3:
                    dc.DrawEllipse(coordinates[i]+l, coordinates[i+1]+w, roomsizes[i]+l, roomsizes[i+1]+w)

            i += 2

        dc.SetPen(wx.Pen("black",4))
        dc.DrawLineList([(coordinates[0], coordinates[1], self.width, coordinates[1]), 
                (self.width, coordinates[1], self.width, self.height),
                (self.width, self.height, coordinates[0], self.height),
                (coordinates[0], self.height, coordinates[0], coordinates[1])]
                )

#-------------------------------------------#
    def drawNoOverlap(self, event):
        '''
        Draw the document with various shapes, but no overlap (ignore x and y
        deformation values).
        '''
        dc = wx.PaintDC(self)
        coordinates, roomsizes = self.getRoomDesc()

        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        dc.SetPen(wx.Pen("black",2))
        dc.DrawRectangle(coordinates[0], coordinates[1], self.width, self.height)

        transf = self.transf
        max_val = 5.
        min_val = -5.
        i = 0

        dc.SetPen(wx.Pen("black",1))

        for j in xrange(0, len(self.dimensions)):
            if self.description[j] == 'S':
                dc.SetBrush(wx.Brush('white'))

            # RST - Restroom, BTH - Bathroom : FIREBRICK
            elif self.description[j] == 'RST' or self.description[j] == 'BTH':
                dc.SetBrush(wx.Brush('firebrick'))        

            # KTH - Kitchen, DIN - Dining Room : GREEN
            elif self.description[j] == 'KTH' or self.description[j] == 'DIN':
                dc.SetBrush(wx.Brush('green'))            

            # LIV - Living Room, LBK - Living/Bed/Kitchen Combo, LKT - Living/Kitchen Combo : RED
            elif self.description[j] == 'LIV' or self.description[j] == 'LBK' or self.description[j] == 'LKT':
                dc.SetBrush(wx.Brush('red'))              

            # BED - Bed Room : YELLOW
            elif self.description[j] == 'MBR' or self.description[j] == 'GBR' or self.description[j] == 'BED': 
                dc.SetBrush(wx.Brush('yellow'))           

            # Other rooms
            else:
                dc.SetBrush(wx.Brush('dim gray'))         

            # if not a blank space
            shape = transf[j][-1]
            if shape:
                xdiff =  transf[j][0] * (max_val-min_val) + min_val
                ydiff =  transf[j][1] * (max_val-min_val) + min_val
                if shape == 1:
                    dc.DrawRectangle(coordinates[i], coordinates[i+1], roomsizes[i], roomsizes[i+1])
                elif shape == 2:
                    dc.DrawRoundedRectangle(coordinates[i], coordinates[i+1], roomsizes[i], roomsizes[i+1], 5.)
                elif shape == 3:
                    dc.DrawEllipse(coordinates[i], coordinates[i+1], roomsizes[i], roomsizes[i+1])

            i += 2

#-------------------------------------------#
