import json

class DataHandler:
    def __init__(self):
        self.AllDataArray = []
        self.dataHeaders = []
        self.missingData = []
        self.lowerTimeLimitForTrends = 0
        self.higherTimeLimitForTrends = 0
        self.trendStatistics = {"acceleration" : {}, "velocity": {}, "spatial_data": {}, "time_data": []}

    def initTrendStats(self):
        labels = ["acceleration", "velocity"]
        sublabels = ["max","Q1", "Q2", "Q3", "std","mean"]
        for label in labels:
            for sublabel in sublabels:
                self.trendStatistics[label][sublabel] = {"data": [], "mean": {}}


    def checkAndGetMissingData(self, headersStr):
        toremove = "listresult"
        LEN = len(toremove)
        headersStr = headersStr[LEN:]
        headersList = headersStr.split(",")

        missingData = []

        for header in headersList:
            if not header in self.dataHeaders:
                missingData.append(header)

        self.missingData = missingData
        return missingData.count != 0

    def updateMissingData(self, header):
        try:
            indx = self.missingData.index(header)
            del self.missingData[indx]
            if not header in self.dataHeaders:
                self.dataHeaders.append(header)
        except:
            print("Index not found on missing data")

    def newDataHandle(self, dataStr):
        toremove = "dataresultMS"
        LEN = len(toremove)
        dataStr = dataStr[LEN:]
        data = json.loads(dataStr)
        self.AllDataArray.append(data)
        self.updateMissingData(data["time"])

    def getDataByMs(self, stringMS):
        result = next((item for item in self.AllDataArray if item["time"] == stringMS), None)
        return result

    def getOldestAndNewestDataDates(self):
        if len(self.AllDataArray) != 0:
            oldest = self.AllDataArray[0]["time"]
            newest = self.AllDataArray[0]["time"]
            for item in self.AllDataArray:
                if item["time"] > newest:
                    newest = item["time"]
                if item["time"] < oldest:
                    oldest = item["time"]

        return oldest, newest

    def getDataBetweenDates(self):
        lower = self.lowerTimeLimitForTrends
        higher = self.higherTimeLimitForTrends

        array = self.AllDataArray

        result = []

        for item in array:
            time = item["time"]
            time = time.replace(",",".")
            time = float(time)
            if time > lower and time < higher:
                result.append(item)

        return result

    def setTrendStatistics(self):
        trendTimeData = self.getDataBetweenDates()
        self.initTrendStats()

        cat_labels = ["acceleration", "velocity"]
        sublabels = ["max","Q1", "Q2", "Q3", "std","mean"]

        for item in trendTimeData:
            stats = item["statistics"]
            time = item["time"]
            self.trendStatistics["time_data"].append(time)
            for c_label in cat_labels:
                head_data = stats[c_label]
                for label in sublabels:
                    value = head_data[label]
                    self.trendStatistics[c_label][label]["data"].append(value)


        for label in cat_labels:
            for sublabel in sublabels:
                valueArray = self.trendStatistics[label][sublabel]["data"]
                count = 0
                total = 0
                for value in valueArray:
                    count = count + 1
                    total = total + value

                if count == 0:
                    self.trendStatistics[label][sublabel]["mean"] = -9999999
                else:
                    self.trendStatistics[label][sublabel]["mean"] = total/count

