import math as m
import numpy as np
import pandas as pd


class DataBridge:

    def calculateInput(self, data):
        
        timestamp = data["ts"].iloc[0]
        meter = data["meter_no"].iloc[0]
        bldg = data["building_name"].iloc[0]
        newRow = {"time":timestamp, "building":bldg, "meter":meter}
    

        if bldg == "NSU":
            #calculation of average voltage
            vAN = data.loc[data["topic_name"] == "VoltagePhaseAtoNeutral", "value_string"].iloc[0]
            vBN = data.loc[data["topic_name"] == "VoltagePhaseBtoNeutral", "value_string"].iloc[0]
            vCN = data.loc[data["topic_name"] == "VoltagePhaseCtoNeutral", "value_string"].iloc[0]
            #average voltage 

            #calculate positive sequence voltage
            newRow["avgVoltage"] = (vAN + vBN + vCN)/3 * m.sqrt(3)
            
            #calculation of current values for substation
            newRow["currentA"] = data.loc[data["topic_name"] == "CurrentPhaseA", "value_string"].iloc[0]
            newRow["currentB"] = data.loc[data["topic_name"] == "CurrentPhaseB", "value_string"].iloc[0]
            newRow["currentC"] = data.loc[data["topic_name"] == "CurrentPhaseC", "value_string"].iloc[0]

        else:
            realPowerA = data.loc[data["topic_name"] == "RealPowerPhaseA", "value_string"].iloc[0]
            realPowerB = data.loc[data["topic_name"] == "RealPowerPhaseB", "value_string"].iloc[0]
            realPowerC = data.loc[data["topic_name"] == "RealPowerPhaseC", "value_string"].iloc[0]
            
            reactivePowerA = data.loc[data["topic_name"] == "ReactivePowerPhaseA", "value_string"].iloc[0]
            reactivePowerB = data.loc[data["topic_name"] == "ReactivePowerPhaseB", "value_string"].iloc[0]
            reactivePowerC = data.loc[data["topic_name"] == "ReactivePowerPhaseC", "value_string"].iloc[0]
            
            newRow["powerA"] = complex(realPowerA, reactivePowerA)
            newRow["powerB"] = complex(realPowerB, reactivePowerB)
            newRow["powerC"] = complex(realPowerC, reactivePowerC)
        
        return newRow
        
    def requiredData(self, data): #The plan is to calculate the complex voltage and complex power here
    
        #inst is the dataFrame where we put all the data that goes into the simulation fo a single instance of time
        columns = ["time","building", "meter", "avgVoltage", "currentA", "currentB", "currentC", "powerA", "powerB", "powerC"]
        # columns = ["Time","building", "meter", "avgVoltage", "Power"]
        timestamps = data.ts.unique().tolist()
        inst = pd.DataFrame(columns = columns)
        for time in timestamps:
            instance = data[data["ts"]==time]
            input = self.calculateInput(instance)
            inst.loc[len(inst)] = input
        
        #we need to feed the power consumption data as a daily parameter of per hour consumption
        inst['time'] = pd.to_datetime(inst['time'])
        return inst

    def collector(self, building, meter):
        path = "../../dataset/{bldg}/{metername}_5M.csv".format( bldg = building, metername = meter)
        data = pd.read_csv(path)
        reqdata = self.requiredData(data)
        return reqdata    


