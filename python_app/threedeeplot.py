from typing import OrderedDict
import matplotlib as plt
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import OpenGL.GL as ogl
from PyQt5 import  QtWidgets

pg.mkQApp()
plt.use('Qt5Agg')


class PyQtGraphContainer(QtWidgets.QFrame):
    def __init__(self, parent):
        super(PyQtGraphContainer, self).__init__()
        pg.setConfigOptions(antialias=True)
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.plotTitleTracker = []
        self.plotArray = []
        self.widgetArray = []
        self.gridIndexes = [0,-1]
        self.colors = [ (128, 0, 0), (0,0,0), (128,128,0), (0,128, 128), (0,0,128),  (230,25,75), (245,130,48) ]
        self.colors2 = [ (128, 0, 0,0.8), (0,0,0,0.8), (128,128,0,0.8), (0,128, 128,0.8), (0,0,128,0.8), (230,25,75,0.8), (245,130,48,0.8) ]

    def getGridIndexes(self):
        n = self.gridIndexes[0]
        m = self.gridIndexes[1]

        if m == 2:
            n = n + 1
            m = 0
        else:
            m = m +1
            if m == 1:
                    self.layout.setColumnStretch(0,1)
                    self.layout.setColumnStretch(1,1)
            if m == 2:
                self.layout.setColumnStretch(2,1)

        self.gridIndexes = [n,m]
        return self.gridIndexes

    def removeAll(self):
        print("Remove all")
        for widget in self.widgetArray:
            self.layout.removeWidget(widget)

        self.widgetArray = []
        self.plotTitleTracker = []
        self.plotArray = []
    
    def drawPlots(self, data, drawTypeArray):
        if (len(self.widgetArray) > 5):
            self.removeAll()
            return
        #print(data)
        for item in drawTypeArray:
            label = item[0]
            drawtype = item[1]
            plot = None
            indx = None

            if self.isDrawTypeIn(item):
                print("found")
                indx = self.plotTitleTracker.index(item)
                plot = self.plotArray[indx]

            else:
                print("not found")
            if drawtype == '3D':
                self.plot3D(data, plot = plot, drawtype = item, index = indx)
            elif drawtype == 'scalar':
                scalar_data = self.getScalars(data, label)
                draw_data = [data["time_data"], scalar_data]
                self.plot2D(draw_data, plot = plot, drawtype = item, index = indx)
                
    def drawTrendPlot(self, data, drawTypeItem):
        if (len(self.widgetArray) > 5):
            self.removeAll()
            return
        idx = None
        plot = None


        color_index = 0


        if self.isDrawTypeIn(drawTypeItem):
            print("yes")
            idx = self.plotTitleTracker.index(drawTypeItem)
            plot = self.plotArray[idx][0]
            color_index = self.plotArray[idx][1]+1
            self.plotArray[idx][1] = color_index
            
        
        else:
            print("no")
            wrapper = QtWidgets.QFrame()
            self.widgetArray.append(wrapper)
            lay = QtWidgets.QHBoxLayout()
            wrapper.setLayout(lay)

            container = pg.GraphicsLayoutWidget(show=False)
            container.setBackground('w')
            plot = container.addPlot(title=drawTypeItem[0]+ " "+drawTypeItem[1])
            self.plotArray.append([plot,0])
            container.sizeHint = lambda: pg.QtCore.QSize(100, 100)
            plot.showGrid(x=True)
            gridindex = self.getGridIndexes()
            lay.addWidget(container)
            self.layout.addWidget(wrapper,gridindex[0],gridindex[1])


        

        self.plotTitleTracker.append(drawTypeItem)
        time_data = data[1]
        value_data = data[0]
        print(data)
        data1array = []
        for i in range(len(data[0])):
            data1array.append(i)
        
        dArr = [data[0], data1array]
        draw_data= np.array((dArr))
        print(draw_data)
        plot.plot(draw_data[1], draw_data[0], pen = self.colors[color_index])
    

    def plot2D(self, data, plot = None, drawtype = None, title = "default", index = None):
        if plot == None:
            wrapper = QtWidgets.QFrame()
            self.widgetArray.append(wrapper)
            lay = QtWidgets.QHBoxLayout()
            wrapper.setLayout(lay)

            title = drawtype[0]
            container = pg.GraphicsLayoutWidget(show=False, title=title)
            container.setBackground('w')

            plot = container.addPlot(title=title)
            self.plotTitleTracker.append(drawtype)
            self.plotArray.append([plot,0])

            plot.showGrid(x=True)
            gridindex = self.getGridIndexes()
            container.sizeHint = lambda: pg.QtCore.QSize(100, 100)

            lay.addWidget(container)
            self.layout.addWidget(wrapper,gridindex[0],gridindex[1])

            data= np.array((data))
            plot.plot(data[0],data[1], pen=self.colors[0])
        else:
            color_index = self.plotArray[index][1]+1
            self.plotArray[index][1] = color_index
            plot[0].plot(data[0],data[1], pen = self.colors[color_index])
        
        


    def plot3D(self, data, plot = None, drawtype = None, title = "default", index = None):
        if plot == None:
            wrapper = QtWidgets.QFrame()
            self.widgetArray.append(wrapper)
            lay = QtWidgets.QHBoxLayout()
            wrapper.setLayout(lay)

            plot = Graph3D(self)
            self.plotTitleTracker.append(drawtype)
            self.plotArray.append([plot,0])
            plot.sizeHint = lambda: pg.QtCore.QSize(100, 100)
            gridindex = self.getGridIndexes()
            print(data[drawtype[0]])

            plot.plot(data[drawtype[0]], self.colors2[0])
            lay.addWidget(plot)
            self.layout.addWidget(wrapper,gridindex[0],gridindex[1])

        else:
            color_index = self.plotArray[index][1]+1
            self.plotArray[index][1] = color_index
            plot[0].plot(data[drawtype[0]], self.colors2[color_index])

    def isDrawTypeIn(self, drawTypeArray):
        for item in self.plotTitleTracker:
            if item[0] == drawTypeArray[0] and item[1] == drawTypeArray[1]:
                print(drawTypeArray[0], item[0], drawTypeArray[1], item[1])
                return True
        return False

    def getScalars(self, data, label):
        result = []
        for item in data[label]:
            x = np.array([item["x"],item["y"],item["z"]])
            value = np.linalg.norm(x)
            result.append(value)

        return result

class Graph3D(gl.GLViewWidget):
    def __init__(self, parent):
        super(Graph3D, self).__init__()

        self.allPlotsDictionary = OrderedDict()

        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()

        xgrid.setColor((200,200,200))
        ygrid.setColor((100,100,100))
        zgrid.setColor((100,100,100))

        self.addItem(xgrid)

        ygrid.rotate(90, 0, 1, 0)
        zgrid.rotate(90, 1, 0, 0)

        xgrid.setSize(2,2,2)
        ygrid.setSize(1,1,1)
        zgrid.setSize(1,1,1)

        xgrid.setSpacing(0.1, 0.1, 0.1)
        ygrid.setSpacing(0.1, 0.1, 0.1)
        zgrid.setSpacing(0.1, 0.1, 0.1)


        self.opts['distance'] = 3

        self.setBackgroundColor('w')
        axis = Custom3DAxis(self, color=(0.2,0.2,0.2,.6))
        self.addItem(axis)      
        
    
    def plot(self, data, color):
        print("color: ",color)
        posdata = self.getXYZFromData(data)
        self.scatter("Test", posdata, color, 1, 0.01)
        
    def getColorsArrayFromVelocity(self, velocity_array):
        colorList = []
        min_value, max_value = self.getMinAndMaxFromArray(velocity_array)
        print(min_value, max_value)
        for velocity in velocity_array:
            r,g,b = self.rgb(min_value, max_value, velocity)
            color = []
            color.append(r/255)
            color.append(g/255)
            color.append(b/255)
            color.append(1)
            print(color)
            colorList.append(color)

        return(colorList)

    def getMinAndMaxFromArray(self, data):
        return min(data), max(data)

    def getVelocityArray(self, data):

        arr_len = len(data)
        vel_list = []


        for i in range(0,arr_len):
            inst_velocity = self.getInstantaneousVelocity(data,i)
            vel_list.append(inst_velocity)
        vel_array = np.array(vel_list)

        return vel_array

    def rgb(self, minimum, maximum, value):
        minimum, maximum = float(minimum), float(maximum)
        ratio = 2 * (value-minimum) / (maximum - minimum)
        b = int(max(0, 255*(1 - ratio)))
        r = int(max(0, 255*(ratio - 1)))
        g = 255 - b - r
        return r, g, b

    def getInstantaneousVelocity(self, posArray, index):
        if len(posArray) == index+1:
            index = index-1
        
        posBefore = posArray[index]
        posAfter = posArray[index+1]

        timeBefore = posBefore[3]
        timeAfter = posAfter[3]
        time_delta = timeAfter-timeBefore

        distance = self.getDistance(posBefore, posAfter)
        velocity = distance/time_delta
        return(velocity)

    def getDistance(self, pos1, pos2):
        pos_1 = np.delete(pos1, 3)
        pos_2 = np.delete(pos2, 3)
        distance = np.linalg.norm(pos_1 - pos_2)
        return distance

    def scatter(self, name, points, colors=(1,1,1,.3), alphas=0.5,
                size=0.1, translucent=True):
            scatterPlot = gl.GLScatterPlotItem(pos=points, size=size, color=colors, pxMode=False)
            if translucent:
                scatterPlot.setGLOptions('translucent')
            self.addItem(scatterPlot)

    def getXYZFromData(self, data):
        arr = np.empty((0,3))
        for value in data:

            x_val = value["x"]

            y_val = value["y"]

            z_val = value["z"]

            point = [x_val, z_val, y_val] # position scale axis messed up changed axis
            arr = np.append(arr, np.array([point]), axis=0)

        #print(arr)
        return arr




class Custom3DAxis(gl.GLAxisItem):
    """Class defined to extend 'gl.GLAxisItem'."""
    def __init__(self, parent, color=(0,0,0,.6) ):
        gl.GLAxisItem.__init__(self)
        self.parent = parent
        self.c = color
        self.add_labels()
        self.add_tick_values()
        
        

    def add_labels(self):
        """Adds axes labels."""
        x,y,z = self.size()
        #X label
        self.xLabel = gl.GLTextItem(pos=((11/10)*x, 0, 0), text='X', color=(150,150,150, 255))
        self.parent.addItem(self.xLabel)

        #Y label
        self.yLabel = gl.GLTextItem(pos=(0, (11/10)*y, 0), text='Y', color=(150,150,150, 255))
        self.parent.addItem(self.yLabel)

        #Z label
        self.zLabel = gl.GLTextItem(pos=(0, 0.05, (1/2)*z), text='Z', color=(150,150,150, 255))
        self.parent.addItem(self.zLabel)

    def add_tick_values(self, xticks=[], yticks=[], zticks=[]):
        """Adds ticks values."""
        ticks = []
        for x in range (0,5):
            ticks.append(x*0.2)

        x,y,z = self.size()
        tpos = np.linspace(0, x, len(ticks))

        #X label ticks
        for i, t in enumerate(ticks):
            valx = gl.GLTextItem(pos=(tpos[i], -y/20, -z/20), text=str(round(t,1)), color=(150,150,150, 255))
            
            if i != 0:
                valy = gl.GLTextItem(pos=(-x/20, tpos[i]-0.05, -z/20), text=str(round(t,1)), color=(150,150,150, 255))
                self.parent.addItem(valy)

                valz = gl.GLTextItem(pos=(-x/20, -y/20, tpos[i]), text=str(round(t,1)), color=(150,150,150, 255))
                self.parent.addItem(valz)
            
            self.parent.addItem(valx)
            
        #Y label  ticks
        #for i, yt in enumerate(yticks):
            #val = CustomTextItem(X=-x/20, Y=ytpos[i], Z=-z/20, text=str(yt))
            #val.setGLViewWidget(self.parent)
           # self.parent.addItem(val)
        #Z label  ticks
        #for i, zt in enumerate(zticks):
            #val = CustomTextItem(X=-x/20, Y=-y/20, Z=ztpos[i], text=str(zt))
            #val.setGLViewWidget(self.parent)
            #self.parent.addItem(val)

    def paint(self):
        self.setupGLState()
        if self.antialias:
            ogl.glEnable(ogl.GL_LINE_SMOOTH)
            ogl.glHint(ogl.GL_LINE_SMOOTH_HINT, ogl.GL_NICEST)
        ogl.glLineWidth(2.0)
        ogl.glBegin(ogl.GL_LINES)
        
        x,y,z = self.size()
        #Draw Z
        ogl.glColor4f(self.c[0], self.c[1], self.c[2], self.c[3])
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(0, 0, z)
        #Draw Y
        ogl.glColor4f(self.c[0], self.c[1], self.c[2], self.c[3])
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(0, y, 0)
        #Draw X
        ogl.glColor4f(self.c[0], self.c[1], self.c[2], self.c[3])
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(x, 0, 0)
        ogl.glEnd()
        ogl.glLineWidth(1.0)