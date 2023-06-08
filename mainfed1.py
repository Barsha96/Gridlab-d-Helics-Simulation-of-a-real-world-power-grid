# -*- coding: utf-8 -*-
import time
import pandas as pd
import numpy as np
import helics as h
from math import pi
import random
from publication_hub1 import PubHub
from data_bridge import DataBridge
from anomaly_generator import Anomaly
import random
from datetime import datetime, timedelta

def create_federate():
    fedinitstring = "--federates=1"
    deltat = 300

    helicsversion = h.helicsGetVersion()
    print("PI SENDER: Helics version = {}".format(helicsversion))

    # Create Federate Info object that describes the federate properties #
    fedinfo = h.helicsCreateFederateInfo()

    # Set Federate name #
    h.helicsFederateInfoSetCoreName(fedinfo, "FedA")

    # Set core type from string #
    h.helicsFederateInfoSetCoreTypeFromString(fedinfo, "zmq")

    # Federate init string #
    h.helicsFederateInfoSetCoreInitString(fedinfo, fedinitstring)

    # Set the message interval (timedelta) for federate. Note th#
    # HELICS minimum message time interval is 1 ns and by default
    # it uses a time delta of 1 second. What is provided to the
    # setTimedelta routine is a multiplier for the default timedelta.

    # Set one second message interval #
    h.helicsFederateInfoSetTimeProperty(fedinfo, h.helics_property_time_delta, deltat)

    # Create vavscodlue federate #
    vfed = h.helicsCreateValueFederate("publisher", fedinfo)
    print("PI SENDER: Value federate created")

    return vfed


def generate_input(buildings, data, anms):
    for building, meters in buildings.items():
        for meter in meters:
            if meter in anms:
                bldg = data.collector(building, meter, True)
                filename = "inputs/{}ANM_input.csv".format(meter)
                bldg.to_csv(filename, index = False)
                print("-----------------------")
            else:
                bldg = data.collector(building, meter, False)
                filename = "inputs/{}_input.csv".format(meter)
                bldg.to_csv(filename, index = False)
                print("-----------------------")

def assign_publication(fed, buildings, pubs, subs, anms):
    building_datas = []
    #the publication Ids are stored in a dictionary called pubs where using the keys, those pubIds can be obtained using the keys  
    for building, meters in buildings.items():
        if building == "NSU":
            for meter in meters:
                psv = pubs["{b}/{m}/positive_sequence_voltage".format(b=building, m=meter)]
                cA = pubs["{b}/{m}/current_A".format(b=building, m=meter)]
                cB = pubs["{b}/{m}/current_B".format(b=building, m=meter)]
                cC = pubs["{b}/{m}/current_C".format(b=building, m=meter)]
                path1 = "inputs/{}_input.csv".format(meter)
                substation_data = pd.read_csv(path1)
        else:
            for meter in meters:
                if meter in anms:
                    path2 = "inputs/{}ANM_input.csv".format(meter)
                    bldg = pd.read_csv(path2)
                    anm_mark = bldg[["time", "anomaly"]]
                    building_datas.append(bldg)
                else:
                    path2 = "inputs/{}_input.csv".format(meter)
                    bldg = pd.read_csv(path2)
                    building_datas.append(bldg)                   
                   
    
    simulation_time = substation_data["time"]
    currenttime = 0
    
    columns = ["time","building", "gld_object", "property", "complex_value", "double_value", "anomaly"]
    output = pd.DataFrame(columns = columns)

    col1 = ["average_voltage","current_A","current_B","current_C"]
    voltcurr_input = pd.DataFrame(columns = col1)

    col2 = ["power_A","power_B","power_C"]
    power_input = pd.DataFrame(columns = col2)

    for t in simulation_time:
        if t > "2022-08-10 19:05:00":
            currenttime = h.helicsFederateRequestTime(fed, currenttime + 20)
            inputdata = substation_data[substation_data["time"] == t]
            timee = inputdata['time'].iloc[0]
            building_name = inputdata['building'].iloc[0]
            isanm = anm_mark[anm_mark["time"] == t]
            isanm = isanm["anomaly"].iloc[0]
            #This publishes positive_sequence_voltage and current to substation which takes value of type complex in gridlabd
            if building_name == "NSU":
                avgvoltage = inputdata['avgVoltage'].iloc[0]
                currentA = inputdata['currentA'].iloc[0]
                currentB = inputdata['currentB'].iloc[0]
                currentC = inputdata['currentC'].iloc[0]
                pubids = [psv, cA, cB, cC]
                pub_values = [avgvoltage, currentA, currentB, currentC]
                publish_voltage_current(pubids, pub_values, timee, voltcurr_input)
                # voltcurr_input.to_csv("input_current_voltage.csv", index=False)
            
            if len(building_datas) != 0:
                for building_data in building_datas:
                    dat = building_data[building_data["time"] == t]
                    building_name = dat["building"].iloc[0]
                    meter_name = dat["meter"].iloc[0]
                    powerA = dat["powerA"].iloc[0]
                    powerB = dat["powerB"].iloc[0]
                    powerC = dat["powerC"].iloc[0]
                    pAid = pubs["{b}/{m}/powerA".format(b=building_name, m=meter_name)]
                    pBid = pubs["{b}/{m}/powerB".format(b=building_name, m=meter_name)]
                    pCid = pubs["{b}/{m}/powerC".format(b=building_name, m=meter_name)]
                    
                    power_pubvalues = [powerA, powerB, powerC]
                    power_pubid = [pAid, pBid, pCid]

                    #This publishes load power consumption values which takes value of type complex in gridlabd
                    publish_power(power_pubid, power_pubvalues, timee, power_input)
        
            #This is to make the time sleep for 1 second
            time.sleep(1)

        #outputs
        #for node n125
        output = get_subscriptions(subs, timee, output, "main", "msource", "measured_voltage_A", "complex", isanm)
        output = get_subscriptions(subs, timee, output, "main", "msource", "measured_voltage_B", "complex", isanm)
        output = get_subscriptions(subs, timee, output, "main", "msource", "measured_voltage_C", "complex", isanm)  
        output = get_subscriptions(subs, timee, output, "main", "msource", "measured_current_A", "complex", isanm)
        output = get_subscriptions(subs, timee, output, "main", "msource", "measured_current_B", "complex", isanm)
        output = get_subscriptions(subs, timee, output, "main", "msource", "measured_current_C", "complex", isanm)         
        output = get_subscriptions(subs, timee, output, "main", "msource", "measured_power_A", "complex", isanm)
        output = get_subscriptions(subs, timee, output, "main", "msource", "measured_power_B", "complex", isanm)
        output = get_subscriptions(subs, timee, output, "main", "msource", "measured_power_C", "complex", isanm)  
        # output = get_subscriptions(subs, timee, output, "R1", "n125", "current_A", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "n125", "current_B", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "n125", "current_C", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "n125", "power_A", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "n125", "power_B", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "n125", "power_C", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "n125", "maximum_voltage_error", "double")

        #for load l131
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "measured_voltage_A", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "measured_voltage_B", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "measured_voltage_C", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "constant_power_A", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "constant_power_B", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "constant_power_C", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "constant_impedance_A", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "constant_impedance_B", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "constant_impedance_C", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "constant_current_A", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "constant_current_B", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "constant_current_C", "complex")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "power_pf_A", "double")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "power_pf_B", "double")
        # output = get_subscriptions(subs, timee, output, "R1", "l131", "power_pf_C", "double")

        output.to_csv("output.csv", index=False)
            
def publish_voltage_current(pubid, pub_values, time, voltcurr_input):
    
    h.helicsPublicationPublishComplex(pubid[0], pub_values[0], 0)
    # print("sending averagevoltage for substation as positive_sequence_voltage {} at time {} to R1.glm".format(pub_values[0], time))
    
    #current
    h.helicsPublicationPublishComplex(pubid[1], pub_values[1], 0)
    # print("sending currentA {} at time {} to R1.glm".format(complex(pub_values[1], 0), time))
    

    h.helicsPublicationPublishComplex(pubid[2], pub_values[2], -120.0)
    # print("sending currentB {} at time {} to R1.glm".format(complex(pub_values[2], -120.0), time))
    
    
    h.helicsPublicationPublishComplex(pubid[3], pub_values[3], +120.0)
    # print("sending currentC {} at time {} to R1.glm".format(complex(pub_values[3], +120.0), time))

    
    inp = {"average_voltage":complex(pub_values[0], 0), "current_A":complex(pub_values[1], 0), "current_B":complex(pub_values[2], -120), "current_C":complex(pub_values[3], +120)}
    voltcurr_input.loc[len(voltcurr_input)] = inp


def publish_power(pubids, values, time, power_input):
    values = [complex(x) for x in values]
    h.helicsPublicationPublishComplex(pubids[0], values[0].real, values[0].imag)

    # print("sending powerA {} at time {} to R1.glm".format(values[0], time))
    
    h.helicsPublicationPublishComplex(pubids[1], values[1].real, values[1].imag)
    # print("sending powerB {} at time {} to R1.glm".format(values[1], time))

    h.helicsPublicationPublishComplex(pubids[2], values[2].real, values[2].imag)
    # print("sending powerC {} at time {} to R1.glm".format(values[2], time))

    inp = {"power_A":complex(values[0].real, values[0].imag), "power_B":complex(values[1].real, values[1].imag),"power_C":complex(values[2].real, values[2].imag)}
    power_input.loc[len(power_input)] = inp


def get_subscriptions(subs, timee, output, bldg, object, property, datatype, isanm):
    if datatype == "complex":
        v = h.helicsInputGetComplex(subs["{}/{}/{}".format(bldg, object, property)])
        input = {"time":timee, "building":bldg, "gld_object":object, "property":property, "complex_value":v, "double_value":"N/A", "anomaly":isanm}
        
    elif datatype == "double":
        v = h.helicsInputGetDouble(subs["{}/{}/{}".format(bldg, object, property)])
        input = {"time":timee, "building":bldg, "gld_object":object, "property":property, "double_value":v, "complex_value":"N/A", "anomaly":isanm}
    
    output.loc[len(output)] = input
    return output

def main():
    fed = create_federate()
    # Register the publication #
    pubs = {}
    subs = {}
    print("fed is set up.. going into publication")
    pubhub = PubHub(fed)
    buildings = {
        "NSU":["NSU09"], 
        "NBN":["NBN01"],
        "NBM":["NBM01","NBM02"],
        "NAM":["NAM01"],
        "NBP":["NBP01"],
        "NAK":["NAK02"],
        "NAG":["NAG02"]
    }
    pubs = pubhub.manage_publication_register(buildings, pubs)
    print("fed: Publication registered")

    subs = pubhub.manage_subscription_register(buildings, subs)
    print("fed: Subscriptions registered")

    #If you want to introduce anomalies in the simulation, list the buildings you want the anomalies in 
    anms = ["NBM02"]

    #Extract the processed data which comes from dataset
    #We dont want to extract everything at once so passing this data object into assign_publication so that it extracts only the  data it needs at the moment
    data = DataBridge()

    
    # Enter execution mode 
    h.helicsFederateEnterExecutingMode(fed)
    print("PI SENDER: Entering execution mode")

    # generate_input(buildings, data, anms)

    assign_publication(fed, buildings, pubs, subs, anms)

    h.helicsFederateFinalize(fed)
    print("PI SENDER: Federate finalized")

    h.helicsFederateDisconnect(fed)


if __name__ == "__main__":
    main()