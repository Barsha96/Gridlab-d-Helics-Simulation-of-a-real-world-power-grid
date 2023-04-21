# -*- coding: utf-8 -*-
import time
import pandas as pd
import numpy as np
import helics as h
from math import pi
import random
from publication_hub import PubHub
from data_bridge import DataBridge

def create_federate():
    fedinitstring = "--federates=1"
    deltat = 1.0

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

def assign_publication(fed, buildings, pubs, data, subs):

    #the publication Ids are stored in a dictionary called pubs where using the keys, those pubIds can be obtained using the keys  
    building_datas = []
    for building, meters in buildings.items():
        if building == "NSU":
            for meter in meters:
                psv = pubs["{b}/{m}/positive_sequence_voltage".format(b=building, m=meter)]
                cA = pubs["{b}/{m}/current_A".format(b=building, m=meter)]
                cB = pubs["{b}/{m}/current_B".format(b=building, m=meter)]
                cC = pubs["{b}/{m}/current_C".format(b=building, m=meter)]
                substation_data = data.collector(building, meter)
                print(substation_data)
                print("-----------------------")
        else:
            for meter in meters:
                bldg = data.collector(building, meter)
                building_datas.append(bldg)
                print("-----------------------")
                
      
    simulation_time = substation_data["Time"]
    currenttime = 0
    day = 12343334
    

    for t in simulation_time:
        currenttime = h.helicsFederateRequestTime(fed, currenttime + 20)
        inputdata = substation_data[substation_data["Time"] == t]
        current_day = inputdata['day'].iloc[0]
        avgvoltage = inputdata['avgVoltage'].iloc[0]
        currentA = inputdata['CurrentPhaseA'].iloc[0]
        currentB = inputdata['CurrentPhaseB'].iloc[0]
        currentC = inputdata['CurrentPhaseC'].iloc[0]
        timee = inputdata['Time'].iloc[0]

        
        if len(building_datas) != 0: 
            for building_data in building_datas:
                if day != current_day:
                #generate daily profile csv for each building being played in simulation
                    daily = building_data[building_data["day"] == current_day]
                    print(daily)
                    
                    daily = daily[["Time", "Power"]]
                    daily['Time'] = pd.to_datetime(daily['Time'])
                    daily = daily.groupby(pd.Grouper(key='Time', freq='1H'))['Power'].mean().reset_index()
                    daily["Time"] = daily["Time"].dt.hour
                    filename = "{}_dailyLoad.csv".format(building_data["building"].iloc[0])
                    daily.to_csv(filename, index=False)
                    day = current_day
                    

        #This publishes nominal_voltage to substation which takes value of type double in gridlabd

        h.helicsPublicationPublishComplex(psv, avgvoltage, 0)
        print("sending averagevoltage for substation as positive_sequence_voltage {} at time {} to R1.glm".format(avgvoltage, timee))
        h.helicsPublicationPublishComplex(cA, currentA, 0)
        print("sending currentA {} at time {} to R1.glm".format(complex(currentA, 0), timee))
        h.helicsPublicationPublishComplex(cB, currentB, -120.0)
        print("sending currentB {} at time {} to R1.glm".format(complex(currentB, -120.0), timee))
        h.helicsPublicationPublishComplex(cC, currentC, +120.0)
        print("sending currentC {} at time {} to R1.glm".format(complex(currentC, +120.0), timee))
        time.sleep(1)

        #This subscribes to current_A value for node 125 which is obtained in complex value 
        value1 = h.helicsInputGetComplex(subs["R1/n125/voltage_A"])
        print("At {} time the voltage value for node n125 in complex is {}".format(timee,value1))
        value2 = h.helicsInputGetDouble(subs["R1/m_t11/monthly_fee"])
        print("At {} time the monthly fee for a meter is {}".format(timee,value2))
        value3 = h.helicsInputGetDouble(subs["R1/m_t11/monthly_energy"])
        print("At {} time the energy for meter is {}".format(timee,value3))
        print("------------------------------------------------------------------------------------")


def main():
    fed = create_federate()
    # Register the publication #
    pubs = {}
    subs = {}
    print("fed is set up.. going into publication..")
    pubhub = PubHub(fed)
    r1 = {
        "NSU":["NSU01"], 
        "NBN":["NBN01"] #continue ... adding NBN is giving error
    }
    pubs = pubhub.manage_publication_register(r1, pubs)
    print("fed: Publication registered")

    subs = pubhub.manage_subscription_register(subs)
    print("fed: Subscriptions registered")


    #Extract the processed data which comes from dataset
    #We dont want to extract everything at once so passing this data object into assign_publication so that it extracts only the  data it needs at the moment
    data = DataBridge()

    # Enter execution mode 
    h.helicsFederateEnterExecutingMode(fed)
    print("PI SENDER: Entering execution mode")


    assign_publication(fed, r1 , pubs, data, subs)

    h.helicsFederateFinalize(fed)
    print("PI SENDER: Federate finalized")

    h.helicsFederateDisconnect(fed)


if __name__ == "__main__":
    main()