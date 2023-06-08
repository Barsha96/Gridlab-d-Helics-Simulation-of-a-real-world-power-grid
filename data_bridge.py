import math as m
import numpy as np
import pandas as pd


class DataBridge:

    def calculateInput(self, inst, isanm):
        
        timestamp = inst["ts"].iloc[0]
        meter = inst["meter_no"].iloc[0]
        bldg = inst["building_name"].iloc[0]
        newRow = {"time":timestamp, "building":bldg, "meter":meter}


        if bldg == "NSU":
            #calculation of average voltage
            vAN = inst.loc[inst["topic_name"] == "VoltagePhaseAtoNeutral", "value_string"].iloc[0]
            vBN = inst.loc[inst["topic_name"] == "VoltagePhaseBtoNeutral", "value_string"].iloc[0]
            vCN = inst.loc[inst["topic_name"] == "VoltagePhaseCtoNeutral", "value_string"].iloc[0]
            #average voltage 

            #calculate positive sequence voltage
            newRow["avgVoltage"] = (vAN + vBN + vCN)/3 * m.sqrt(3)
            
            #calculation of current values for substation
            newRow["currentA"] = inst.loc[inst["topic_name"] == "CurrentPhaseA", "value_string"].iloc[0]
            newRow["currentB"] = inst.loc[inst["topic_name"] == "CurrentPhaseB", "value_string"].iloc[0]
            newRow["currentC"] = inst.loc[inst["topic_name"] == "CurrentPhaseC", "value_string"].iloc[0]

        else:
            realPowerA = inst.loc[inst["topic_name"] == "RealPowerPhaseA", "value_string"].iloc[0]
            realPowerB = inst.loc[inst["topic_name"] == "RealPowerPhaseB", "value_string"].iloc[0]
            realPowerC = inst.loc[inst["topic_name"] == "RealPowerPhaseC", "value_string"].iloc[0]
            
            reactivePowerA = inst.loc[inst["topic_name"] == "ReactivePowerPhaseA", "value_string"].iloc[0]
            reactivePowerB = inst.loc[inst["topic_name"] == "ReactivePowerPhaseB", "value_string"].iloc[0]
            reactivePowerC = inst.loc[inst["topic_name"] == "ReactivePowerPhaseC", "value_string"].iloc[0]
            
            newRow["powerA"] = complex(realPowerA, reactivePowerA)
            newRow["powerB"] = complex(realPowerB, reactivePowerB)
            newRow["powerC"] = complex(realPowerC, reactivePowerC)

            if isanm:
                newRow["anomaly"] = inst["anomaly"].iloc[0]
        
        return newRow
        
    def requiredData(self, data, isanm): #The plan is to calculate the complex voltage and complex power here
    
        #inst is the dataFrame where we put all the data that goes into the simulation fo a single instance of time
        if isanm:
            columns = ["time","building", "meter", "avgVoltage", "currentA", "currentB", "currentC", "powerA", "powerB", "powerC","anomaly"]
        else:
            columns = ["time","building", "meter", "avgVoltage", "currentA", "currentB", "currentC", "powerA", "powerB", "powerC"]
        # columns = ["Time","building", "meter", "avgVoltage", "Power"]
        timestamps = data.ts.unique().tolist()
        inst = pd.DataFrame(columns = columns)
        for time in timestamps:
            instance = data[data["ts"]==time]
            input = self.calculateInput(instance, isanm)
            inst.loc[len(inst)] = input
        
        #we need to feed the power consumption data as a daily parameter of per hour consumption
        inst['time'] = pd.to_datetime(inst['time'])
        return inst

    def collector(self, building, meter, anm):
        if anm == True:
            path = "../../dataset/{bldg}/{metername}_ANM.csv".format( bldg = building, metername = meter)
            data = pd.read_csv(path)
            reqdata = self.requiredData(data, anm)
            return reqdata   
        else:
            path = "../../dataset/{bldg}/{metername}_5M.csv".format( bldg = building, metername = meter)
            data = pd.read_csv(path)
            reqdata = self.requiredData(data, anm)
            return reqdata   


