import sys
import datetime
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QApplication, QLabel, QWidget, QVBoxLayout, QListWidget, QPushButton, QTabWidget
from PyQt5 import uic, QtCore, QtWebSockets, QtGui
from PyQt5.QtGui import QPalette, QFont
from loginDialog import CustomDialog
from threedeeplot import PyQtGraphContainer
from DataHandler import DataHandler


import pyqtgraph.examples # removing this line breaks the application .........
#pyqtgraph.examples.run()

url = "ws://127.0.0.1:3210" # server url hardcoded
connected = False

class AppDemo(QWidget):
    def  __init__(self):

        super().__init__()
        self.dataIndex = []
        uic.loadUi('serverConnection.ui', self)
        self.isPlotWindowOpen = False
        self.initUiSettings()
        self.username = ""
        self.password = ""
        self.datahandler = DataHandler()
        self.graphContainer = PyQtGraphContainer(self)
        self.listOfDataTitles = ListWidget(self)
        self.dataTitleList.setWidget(self.listOfDataTitles)
        #self.askCredentials()                                  # ask authentication. not fully implemented
        self.client = Client(self) 
        self.requestListBtn.clicked.connect(self.client.requestDataList)
        self.selectedData = {}
        self.listOfDataTitles.itemClicked.connect(self.dataListTitleClicked)
        self.graphTabWidget = GraphTableWidget(self)
        self.graphWidgetDock.setWidget(self.graphTabWidget)
        self.graphTabWidget.addNewTab("Graphs", self.graphContainer)



    def drawCurrentData(self):
        if self.selectedData != {}:
            print("draw x")
            drawTypeArray = [['spatial_data','3D'],['acceleration_data','scalar'],['spatial_data','scalar']]
            #drawTypeArray = [['acceleration_data','scalar']]
            self.graphContainer.drawPlots(self.selectedData, drawTypeArray)

    def drawTrendData(self, value, type):
        stats = self.datahandler.trendStatistics
        value_data = stats[value][type]["data"]
        time_data = stats["time_data"]
        data = (value_data, time_data)
        drawTypeItem = [value, type]
        self.graphContainer.drawTrendPlot(data, drawTypeItem)

    def receiveData(self, dataString):
        self.datahandler.newDataHandle(dataString)
        self.getMissingData()

    def updateDataList(self, dataString):
        missingData = self.datahandler.checkAndGetMissingData(dataString)
        if missingData:
            self.getMissingData()

    def getMissingData(self):
        if len(self.datahandler.missingData) != 0:
            self.client.requestDataByMillisecond(self.datahandler.missingData[0])
        else:
            self.updateDataListUI()
            self.updateDatePickerDates()

    


    def askCredentials(self):
        username, password, ok = CustomDialog.getUserPassword()
        print(username + " " + password)
        self.username = username
        self.password = password
        self.credentialsGiven = ok
        if self.credentialsGiven == False or self.username == "" or self.password == "":
           # sys.exit()
           return

    def checkCbox(self, box, bool):
        box.setCheckable(True)
        box.setChecked(bool)
        
    def msToDate(self, ms):
        dt = datetime.datetime.fromtimestamp(int(ms) / 1000.0, tz=None)
        date_time = dt.strftime("%d/%m/%Y, %H:%M:%S")
        return date_time

    def dataListTitleClicked(self):
        index = self.listOfDataTitles.currentRow()
        ms=self.dataIndex[index]
        self.updateChosenDataTable(ms)
        self.updateTrendUiStatsForCurrent()

    def updateDataListUI(self,):
        print("Update list ui")
        self.listOfDataTitles.emptyList()
        data = self.datahandler.dataHeaders
        for value in data:
            self.dataIndex.append(value)
            dt = datetime.datetime.fromtimestamp( int(round(float(value)) ) / 1000.0, tz=None)
            date_time = dt.strftime("%d/%m/%Y, %H:%M:%S")
            self.listOfDataTitles.addItem(date_time)
            print(date_time)

    def getTrendValuePrettified(self, value, average):

        value_difference = value - average
        result = ""
        if value_difference > 0:
            value_difference = str(round(value_difference,3))
            result = str(round(value,3)) + " (+" + value_difference+")"
        else:
            value_difference = str(round(value_difference,3))
            result = str(round(value,3)) + " (" + value_difference+")"
        return result

    def updateTrendUiStatsForCurrent(self):
        data = self.selectedData

        stats2 = self.datahandler.trendStatistics
        acc = stats2["acceleration"]
        vel = stats2["velocity"]

        stats = data["statistics"]
        acceleration = stats["acceleration"]
        velocity = stats["velocity"]
        

        self.trend_velocity_current_Q1.setText(self.getTrendValuePrettified(velocity["Q1"], vel["Q1"]["mean"]))
        self.trend_velocity_current_Q2.setText(self.getTrendValuePrettified(velocity["Q2"], vel["Q2"]["mean"]))
        self.trend_velocity_current_Q3.setText(self.getTrendValuePrettified(velocity["Q3"], vel["Q3"]["mean"]))
        self.trend_velocity_current_std.setText(self.getTrendValuePrettified(velocity["std"], vel["std"]["mean"]))
        self.trend_velocity_current_mean.setText(self.getTrendValuePrettified(velocity["mean"], vel["mean"]["mean"]))
        self.trend_velocity_current_max.setText(self.getTrendValuePrettified(velocity["max"], vel["max"]["mean"]))

        self.trend_acceleration_current_Q1.setText(self.getTrendValuePrettified(acceleration["Q1"], acc["Q1"]["mean"]))
        self.trend_acceleration_current_Q2.setText(self.getTrendValuePrettified(acceleration["Q2"], acc["Q2"]["mean"]))
        self.trend_acceleration_current_Q3.setText(self.getTrendValuePrettified(acceleration["Q3"], acc["Q3"]["mean"]))
        self.trend_acceleration_current_std.setText(self.getTrendValuePrettified(acceleration["std"], acc["std"]["mean"]))
        self.trend_acceleration_current_mean.setText(self.getTrendValuePrettified(acceleration["mean"], acc["mean"]["mean"]))
        self.trend_acceleration_current_max.setText(self.getTrendValuePrettified(acceleration["max"], acc["max"]["mean"]))

    def updateChosenDataTable(self, ms):
        data = self.datahandler.getDataByMs(ms)
        self.selectedData = data
        stats = data["statistics"]
        acceleration = stats["acceleration"]
        velocity = stats["velocity"]
        position = stats["position"]
        
        self.velocity_q1.setText(str(round(velocity["Q1"],3)))
        self.velocity_q2.setText(str(round(velocity["Q2"],3)))
        self.velocity_q3.setText(str(round(velocity["Q3"],3)))
        self.velocity_std.setText(str(round(velocity["std"],3)))
        self.velocity_mean.setText(str(round(velocity["mean"],3)))
        self.velocity_max.setText(str(round(velocity["max"],3)))

        self.acceleration_q1.setText(str(round(acceleration["Q1"],3)))
        self.acceleration_q2.setText(str(round(acceleration["Q2"],3)))
        self.acceleration_q3.setText(str(round(acceleration["Q3"],3)))
        self.acceleration_std.setText(str(round(acceleration["std"],3)))
        self.acceleration_mean.setText(str(round(acceleration["mean"],3)))
        self.acceleration_max.setText(str(round(acceleration["max"],3)))

        self.position_xmax.setText(str(round(position["xmax"],3)))
        self.position_xmin.setText(str(round(position["xmin"],3)))
        self.position_zmax.setText(str(round(position["zmax"],3)))
        self.position_zmin.setText(str(round(position["zmin"],3)))
    
    def updateTrendUiStats(self):
        stats = self.datahandler.trendStatistics
        acc = stats["acceleration"]
        vel = stats["velocity"]

        self.trend_acceleration_all_max.setText(str(round(acc["max"]["mean"],3)))
        self.trend_acceleration_all_Q1.setText(str(round(acc["Q1"]["mean"],3)))
        self.trend_acceleration_all_Q2.setText(str(round(acc["Q2"]["mean"],3)))
        self.trend_acceleration_all_Q3.setText(str(round(acc["Q3"]["mean"],3)))
        self.trend_acceleration_all_std.setText(str(round(acc["std"]["mean"],3)))
        self.trend_acceleration_all_mean.setText(str(round(acc["mean"]["mean"],3)))

        self.trend_velocity_all_max.setText(str(round(vel["max"]["mean"],3)))
        self.trend_velocity_all_Q1.setText(str(round(vel["Q1"]["mean"],3)))
        self.trend_velocity_all_Q2.setText(str(round(vel["Q2"]["mean"],3)))
        self.trend_velocity_all_Q3.setText(str(round(vel["Q3"]["mean"],3)))
        self.trend_velocity_all_std.setText(str(round(vel["std"]["mean"],3)))
        self.trend_velocity_all_mean.setText(str(round(vel["mean"]["mean"],3)))

    def updateDatePickerDates(self):
        oldest, newest = self.datahandler.getOldestAndNewestDataDates()
        lower_date = QtCore.QDateTime()
        higher_date = QtCore.QDateTime()
        QtCore.QDateTime.setMSecsSinceEpoch(lower_date, int(round(float(oldest))) )
        QtCore.QDateTime.setMSecsSinceEpoch(higher_date, int(round(float(newest))) )
        self.datePickerLower.setDateTime(lower_date)
        self.datePickerHigher.setDateTime(higher_date)
        self.updateDatePicked()
        
    def updateDatePicked(self):
        lower_day = self.datePickerLower.date().day()
        lower_month = self.datePickerLower.date().month()
        lower_year = self.datePickerLower.date().year()

        higher_day = self.datePickerHigher.date().day()+1
        higher_month = self.datePickerHigher.date().month()
        higher_year = self.datePickerHigher.date().year()

        lower_date = datetime.datetime(lower_year, lower_month, lower_day)
        higher_date = datetime.datetime(higher_year, higher_month, higher_day)

        epoch = datetime.datetime.utcfromtimestamp(0)

        lower_ms = (lower_date - epoch).total_seconds() * 1000
        higher_ms = (higher_date - epoch).total_seconds() * 1000

        self.datahandler.lowerTimeLimitForTrends = lower_ms
        self.datahandler.higherTimeLimitForTrends = higher_ms

        #self.datahandler.getDataBetweenDates()
        self.datahandler.setTrendStatistics()
        self.updateTrendUiStats()

    # long and winding method for ui init
    def initUiSettings(self):
        self.credentialsGiven = False

        self.connecting = QLabel(self)
        self.connecting.setText("<font color=red>Connecting to server</font>")
        self.connecting.setAutoFillBackground(True)
        self.connecting.move(200,200)
        self.connecting.setFont(QFont('Arial', 50))
        palette = QPalette()
        palette.setColor(QPalette.Window, QtCore.Qt.blue)
        self.connecting.setPalette(palette)
        self.connecting.setAlignment(QtCore.Qt.AlignCenter)
        self.setWindowTitle("Data app")

        myFont=QtGui.QFont()
        myFont.setBold(True)

        self.setDateBtn.clicked.connect(self.updateDatePicked)

        trendContainerLayout = QVBoxLayout(self)

        self.trendTabContainer = QTabWidget(self)

        self.acceleration_trend_container = QGroupBox()
        self.velocity_trend_container = QGroupBox()
        self.spatial_trend_container = QGroupBox()

        trend_layout_acceleration = QGridLayout()
        self.acceleration_trend_container.setLayout(trend_layout_acceleration)

        trend_layout_velocity = QGridLayout()
        self.velocity_trend_container.setLayout(trend_layout_velocity)

        trend_layout_spatial = QGridLayout()
        self.spatial_trend_container.setLayout(trend_layout_spatial)

        trendLayoutContainers = [trend_layout_acceleration, trend_layout_velocity, trend_layout_spatial]
        trendLabels = ["Maksimi","Q1","Q2","Q3","Std","K.a"]


        for item in trendLayoutContainers:
            idx = 1
            for label in trendLabels:
                label_widget = QLabel(label)
                label_widget.setFont(myFont)
                item.addWidget(label_widget,idx,0)
                idx = idx +1

            kalabel = QLabel("K.a")
            kalabel.setFont(myFont)
            chosenlabel = QLabel("Valittu")
            chosenlabel.setFont(myFont)
            item.addWidget(kalabel,0,1)
            item.addWidget(chosenlabel,0,2)
            item.addWidget(QLabel(""),0,3)

        self.trend_acceleration_all_max = QLabel("N/A")
        self.trend_acceleration_all_Q1 = QLabel("N/A")
        self.trend_acceleration_all_Q2 = QLabel("N/A")
        self.trend_acceleration_all_Q3 = QLabel("N/A")
        self.trend_acceleration_all_std = QLabel("N/A")
        self.trend_acceleration_all_mean = QLabel("N/A")

        self.trend_acceleration_current_max = QLabel("N/A")
        self.trend_acceleration_current_Q1 = QLabel("N/A")
        self.trend_acceleration_current_Q2 = QLabel("N/A")
        self.trend_acceleration_current_Q3 = QLabel("N/A")
        self.trend_acceleration_current_std = QLabel("N/A")
        self.trend_acceleration_current_mean = QLabel("N/A")

        self.trend_acceleration_max_draw = QPushButton("Piirrä")
        self.trend_acceleration_Q1_draw = QPushButton("Piirrä")
        self.trend_acceleration_Q2_draw = QPushButton("Piirrä")
        self.trend_acceleration_Q3_draw = QPushButton("Piirrä")
        self.trend_acceleration_std_draw = QPushButton("Piirrä")
        self.trend_acceleration_mean_draw = QPushButton("Piirrä")

        trend_layout_acceleration.addWidget(self.trend_acceleration_all_max, 1,1)
        trend_layout_acceleration.addWidget(self.trend_acceleration_all_Q1, 2,1)
        trend_layout_acceleration.addWidget(self.trend_acceleration_all_Q2, 3,1)
        trend_layout_acceleration.addWidget(self.trend_acceleration_all_Q3, 4,1)
        trend_layout_acceleration.addWidget(self.trend_acceleration_all_std, 5,1)
        trend_layout_acceleration.addWidget(self.trend_acceleration_all_mean, 6,1)

        trend_layout_acceleration.addWidget(self.trend_acceleration_current_max, 1,2)
        trend_layout_acceleration.addWidget(self.trend_acceleration_current_Q1, 2,2)
        trend_layout_acceleration.addWidget(self.trend_acceleration_current_Q2, 3,2)
        trend_layout_acceleration.addWidget(self.trend_acceleration_current_Q3, 4,2)
        trend_layout_acceleration.addWidget(self.trend_acceleration_current_std, 5,2)
        trend_layout_acceleration.addWidget(self.trend_acceleration_current_mean, 6,2)

        trend_layout_acceleration.addWidget(self.trend_acceleration_max_draw, 1,3)
        trend_layout_acceleration.addWidget(self.trend_acceleration_Q1_draw, 2,3)
        trend_layout_acceleration.addWidget(self.trend_acceleration_Q2_draw, 3,3)
        trend_layout_acceleration.addWidget(self.trend_acceleration_Q3_draw, 4,3)
        trend_layout_acceleration.addWidget(self.trend_acceleration_std_draw, 5,3)
        trend_layout_acceleration.addWidget(self.trend_acceleration_mean_draw, 6,3)

        self.trend_velocity_all_max = QLabel("N/A")
        self.trend_velocity_all_Q1 = QLabel("N/A")
        self.trend_velocity_all_Q2 = QLabel("N/A")
        self.trend_velocity_all_Q3 = QLabel("N/A")
        self.trend_velocity_all_std = QLabel("N/A")
        self.trend_velocity_all_mean = QLabel("N/A.a.")

        self.trend_velocity_current_max = QLabel("N/A")
        self.trend_velocity_current_Q1 = QLabel("N/A")
        self.trend_velocity_current_Q2 = QLabel("N/A")
        self.trend_velocity_current_Q3 = QLabel("N/A")
        self.trend_velocity_current_std = QLabel("N/A")
        self.trend_velocity_current_mean = QLabel("N/A")

        self.trend_velocity_max_draw = QPushButton("Piirrä")
        self.trend_velocity_Q1_draw = QPushButton("Piirrä")
        self.trend_velocity_Q2_draw = QPushButton("Piirrä")
        self.trend_velocity_Q3_draw = QPushButton("Piirrä")
        self.trend_velocity_std_draw = QPushButton("Piirrä")
        self.trend_velocity_mean_draw = QPushButton("Piirrä")

        self.trend_velocity_max_draw.clicked.connect(lambda: self.drawTrendData("velocity","max"))
        self.trend_velocity_Q1_draw.clicked.connect(lambda: self.drawTrendData("velocity","Q1"))
        self.trend_velocity_Q2_draw.clicked.connect(lambda: self.drawTrendData("velocity","Q2"))
        self.trend_velocity_Q3_draw.clicked.connect(lambda: self.drawTrendData("velocity","Q3"))
        self.trend_velocity_std_draw.clicked.connect(lambda: self.drawTrendData("velocity","std"))
        self.trend_velocity_mean_draw.clicked.connect(lambda: self.drawTrendData("velocity","mean"))

        self.trend_acceleration_max_draw.clicked.connect(lambda: self.drawTrendData("acceleration","max"))
        self.trend_acceleration_Q1_draw.clicked.connect(lambda: self.drawTrendData("acceleration","Q1"))
        self.trend_acceleration_Q2_draw.clicked.connect(lambda: self.drawTrendData("acceleration","Q2"))
        self.trend_acceleration_Q3_draw.clicked.connect(lambda: self.drawTrendData("acceleration","Q3"))
        self.trend_acceleration_std_draw.clicked.connect(lambda: self.drawTrendData("acceleration","std"))
        self.trend_acceleration_mean_draw.clicked.connect(lambda: self.drawTrendData("acceleration","mean"))

        trend_layout_velocity.addWidget(self.trend_velocity_all_max, 1,1)
        trend_layout_velocity.addWidget(self.trend_velocity_all_Q1, 2,1)
        trend_layout_velocity.addWidget(self.trend_velocity_all_Q2, 3,1)
        trend_layout_velocity.addWidget(self.trend_velocity_all_Q3, 4,1)
        trend_layout_velocity.addWidget(self.trend_velocity_all_std, 5,1)
        trend_layout_velocity.addWidget(self.trend_velocity_all_mean, 6,1)

        trend_layout_velocity.addWidget(self.trend_velocity_current_max, 1,2)
        trend_layout_velocity.addWidget(self.trend_velocity_current_Q1, 2,2)
        trend_layout_velocity.addWidget(self.trend_velocity_current_Q2, 3,2)
        trend_layout_velocity.addWidget(self.trend_velocity_current_Q3, 4,2)
        trend_layout_velocity.addWidget(self.trend_velocity_current_std, 5,2)
        trend_layout_velocity.addWidget(self.trend_velocity_current_mean, 6,2)

        trend_layout_velocity.addWidget(self.trend_velocity_max_draw, 1,3)
        trend_layout_velocity.addWidget(self.trend_velocity_Q1_draw, 2,3)
        trend_layout_velocity.addWidget(self.trend_velocity_Q2_draw, 3,3)
        trend_layout_velocity.addWidget(self.trend_velocity_Q3_draw, 4,3)
        trend_layout_velocity.addWidget(self.trend_velocity_std_draw, 5,3)
        trend_layout_velocity.addWidget(self.trend_velocity_mean_draw, 6,3)

        self.trendDataWrapper.setLayout(trendContainerLayout)
        trendContainerLayout.addWidget(self.trendTabContainer)
        self.trendTabContainer.addTab(self.acceleration_trend_container, "Kiihtyvyys")
        self.trendTabContainer.addTab(self.velocity_trend_container, "Nopeus")
        self.trendTabContainer.addTab(self.spatial_trend_container, "Sijainti")

        layout = QGridLayout()

        self.acceleration_label = QLabel("Kiihtyvyys")
        self.velocity_label = QLabel("Nopeus")
        self.X_label = QLabel("X (vasen / oikea)")
        self.Y_label = QLabel("Z (taakse / eteen)")
        self.XYZ_label = QLabel("XYZ")
        self.Q1_label = QLabel("Q1")
        self.Q2_label = QLabel("Q2")
        self.Q3_label = QLabel("Q3")
        self.mean_label = QLabel("K.a.")
        self.std_label = QLabel("Std")
        self.min_label =QLabel("Min")
        self.max_label = QLabel("Max")
        self.max_label2 = QLabel("Max")
        self.draw_label = QLabel("Piirrä")
        self.spacer = QLabel("")

        self.acceleration_draw = QPushButton("Piirrä")
        self.velocity_draw = QPushButton("Piirrä")
        self.XYZ_draw = QPushButton("Piirrä")
        self.X_draw = QPushButton("Piirrä")
        self.Z_draw = QPushButton("Piirrä")
        self.current_data_draw = QPushButton("Piirrä")

        self.acceleration_label.setFont(myFont)
        self.velocity_label.setFont(myFont)
        self.X_label.setFont(myFont)
        self.Y_label.setFont(myFont)
        self.XYZ_label.setFont(myFont)
        self.Q1_label.setFont(myFont)
        self.Q2_label.setFont(myFont)
        self.Q3_label.setFont(myFont)
        self.mean_label.setFont(myFont)
        self.std_label.setFont(myFont)
        self.min_label.setFont(myFont)
        self.max_label.setFont(myFont)
        self.max_label2.setFont(myFont)
        self.draw_label.setFont(myFont)
        
        layout.addWidget(self.Q1_label,0,2)
        layout.addWidget(self.Q2_label,0,3)
        layout.addWidget(self.Q3_label,0,4)
        layout.addWidget(self.mean_label,0,5)
        layout.addWidget(self.std_label, 0, 6)
        layout.addWidget(self.max_label2,0,7)
        layout.addWidget(self.min_label, 3, 2)
        layout.addWidget(self.max_label, 3, 3)

        layout.addWidget(self.spacer, 0, 1)

        layout.addWidget(self.acceleration_label,1,0)
        layout.addWidget(self.velocity_label, 2,0)

        layout.addWidget(self.current_data_draw,0,0)

        self.current_data_draw.clicked.connect(self.drawCurrentData)

        layout.addWidget(self.X_label, 4,0)
        layout.addWidget(self.Y_label, 5,0)
 
        self.chosenDataWrapper.setLayout(layout)

        self.acceleration_q1 = QLabel("N/A")
        self.acceleration_q2 = QLabel("N/A")
        self.acceleration_q3 = QLabel("N/A")
        self.acceleration_mean = QLabel("N/A")
        self.acceleration_std = QLabel("N/A")
        self.acceleration_max = QLabel("N/A")

        layout.addWidget(self.acceleration_q1, 1,2)
        layout.addWidget(self.acceleration_q2, 1,3)
        layout.addWidget(self.acceleration_q3, 1,4)
        layout.addWidget(self.acceleration_mean, 1,5)
        layout.addWidget(self.acceleration_std, 1,6)
        layout.addWidget(self.acceleration_max, 1,7)
 
        self.velocity_q1 = QLabel("N/A")
        self.velocity_q2 = QLabel("N/A")
        self.velocity_q3 = QLabel("N/A")
        self.velocity_mean = QLabel("N/A")
        self.velocity_std = QLabel("N/A")
        self.velocity_max = QLabel("N/A")

        layout.addWidget(self.velocity_q1, 2,2)
        layout.addWidget(self.velocity_q2, 2,3)
        layout.addWidget(self.velocity_q3, 2,4)
        layout.addWidget(self.velocity_mean, 2,5)
        layout.addWidget(self.velocity_std, 2,6)
        layout.addWidget(self.velocity_max, 2,7)

        self.position_xmax = QLabel("N/A")
        self.position_xmin = QLabel("N/A")
        self.position_zmax = QLabel("N/A")
        self.position_zmin = QLabel("N/A")
        
        layout.addWidget(self.position_xmax,4,2)
        layout.addWidget(self.position_xmin,4,3)
        layout.addWidget(self.position_zmax,5,2)
        layout.addWidget(self.position_zmin,5,3)
        

# Widget for tabs (has currently only 1 tab in program, which is Graphs)
class GraphTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        self.tabs.resize(300,200)
        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def addNewTab(self, title, widget):
        self.tabs.addTab(widget, title)
        
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

# Widget for lists (implemented on list of data records from server)
class ListWidget(QListWidget):
    def __init__(self, parent):
        super(ListWidget, self).__init__(parent)
        #self.itemDoubleClicked.connect(self.getItem)
        
    
    def emptyList(self):
        for i in range(self.count()):
            self.takeItem(0)
            

        
# Handles the websocket connection
class Client(QtCore.QObject):
    def __init__(self, parent):
        super(Client, self).__init__(parent)
       #self.parent = parent()
        self.client =  QtWebSockets.QWebSocket("",QtWebSockets.QWebSocketProtocol.Version13,None)

        self.client.error.connect(self.error)

        self.client.open(QtCore.QUrl(url))

        self.client.pong.connect(self.onPong)
        self.client.disconnected.connect(self.onDisconnect)
        self.client.connected.connect(self.onConnect)
        self.client.textMessageReceived.connect(self.onMessage)
        
        
    def requestDataList(self):
        print("Requesting data list")
        self.client.sendTextMessage("RequestDataList")

    def requestDataByMillisecond(self, ms):
        print("Requesting data of " +ms)
        self.client.sendTextMessage("RequestDataMs "+ms)

    def onConnect(self):
        print("Connected to server")
        self.setConnectionCheckbox(True)
        self.parent().connecting.hide()
        connected = True
        self.requestDataList()

    def onDisconnect(self):
        print("Connection disconnected")
        connected = False
        self.setConnectionCheckbox(False)

    def do_ping(self):
        print("client: do_ping")
        self.client.ping(b"foo")

    def send_message(self):
        print("client: send_message")
        self.client.sendTextMessage("asd")

    def onMessage(self, payload):
        print("Message received")
        if "listresult" in payload:
             self.parent().updateDataList(payload)
        elif "dataresultMS" in payload:
            self.parent().receiveData(payload)
        else:
             print(payload)


    def setConnectionCheckbox(self, bool):
        self.parent().checkCbox(self.parent().ch_check, bool)

    def onPong(self, elapsedTime, payload):
        print("onPong - time: {} ; payload: {}".format(elapsedTime, payload))
        
        #self.parent().checkCbox(self.parent().ch_check, True)
        connected = True

    def error(self, error_code):
        print("error code: {}".format(error_code))
        print(self.client.errorString())
        connected = False
        self.setConnectionCheckbox(False)
        self.attemptReconnect()

    def close(self):
        self.client.close()
        connected = False
        self.setConnectionCheckbox(False)

    def attemptReconnect(self):
        QtCore.QTimer().start(5000)
        print("Attempting reconnection..")
        self.client.open(QtCore.QUrl("ws://127.0.0.1:3210"))
        QtCore.QTimer().stop()

        

    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing window')