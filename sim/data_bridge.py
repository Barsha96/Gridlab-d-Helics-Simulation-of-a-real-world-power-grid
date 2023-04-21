import math as m
import numpy as np
import pandas as pd


class DataBridge:

    def calculateInput(self, data):

        timestamp = data["ts"].iloc[0]

        meter = data["meter_no"].iloc[0]
        bldg = data["building_name"].iloc[0]

        vAN = data.loc[data["topic_name"] == "VoltagePhaseAtoNeutral", "value_string"].iloc[0]
        vBN = data.loc[data["topic_name"] == "VoltagePhaseBtoNeutral", "value_string"].iloc[0]
        vCN = data.loc[data["topic_name"] == "VoltagePhaseCtoNeutral", "value_string"].iloc[0]

        vAvg = (vAN + vBN + vCN)/3 * m.sqrt(3)

        
        apparentPowerA = data.loc[data["topic_name"] == "ApparentPowerPhaseA", "value_string"].iloc[0]
        apparentPowerB = data.loc[data["topic_name"] == "ApparentPowerPhaseB", "value_string"].iloc[0]
        apparentPowerC = data.loc[data["topic_name"] == "ApparentPowerPhaseC", "value_string"].iloc[0]

        #total_apparent_power = m.sqrt(pow(int(float(apparentPowerA)),2)+pow(int(float(apparentPowerB)),2)+pow(int(float(apparentPowerC)),2))
        total_apparent_power = apparentPowerA + apparentPowerB + apparentPowerC
        
        newRow = {"Time":timestamp, "building":bldg, "meter":meter, "avgVoltage": vAvg, "Power":total_apparent_power}

        if bldg == "NSU":
            newRow["CurrentPhaseA"] = data.loc[data["topic_name"] == "CurrentPhaseA", "value_string"].iloc[0]
            newRow["CurrentPhaseB"] = data.loc[data["topic_name"] == "CurrentPhaseB", "value_string"].iloc[0]
            newRow["CurrentPhaseC"] = data.loc[data["topic_name"] == "CurrentPhaseC", "value_string"].iloc[0]

        return newRow
        
    def requiredData(self, data): #The plan is to calculate the complex voltage and complex power here
    
        #inst is the dataFrame where we put all the data that goes into the simulation fo a single instance of time
        columns = ["Time","building", "meter", "avgVoltage", "Power", "CurrentPhaseA", "CurrentPhaseB", "CurrentPhaseC"]
        # columns = ["Time","building", "meter", "avgVoltage", "Power"]
        timestamps = data.ts.unique().tolist()
        inst = pd.DataFrame(columns = columns)
        for time in timestamps:
            instance = data[data["ts"]==time]
            input = self.calculateInput(instance)
            inst.loc[len(inst)] = input
        
        #we need to feed the power consumption data as a daily parameter of per hour consumption
        inst['Time'] = pd.to_datetime(inst['Time'])
        inst['hour'] = inst['Time'].dt.hour
        inst['day'] = inst.groupby(inst["Time"].dt.date).ngroup()
        
        return inst

    def collector(self, building, meter):
        path = "../dataset/{bldg}/{metername}t.csv".format( bldg = building, metername = meter)
        data = pd.read_csv(path)
        reqdata = self.requiredData(data)
        return reqdata    


