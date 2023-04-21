import helics as h
import pandas as pd
import numpy as np
import datetime
import timeit

class PubHub:
    def __init__(self, fed):
        self.fed = fed

    def register_publication(self, building, meters, pubs):
        
        for meter in meters: 
            if building == "NSU":
                # For substation volatges
                voltavg = "{b}/{m}/positive_sequence_voltage".format(b=building, m=meter)
                pubid1 = h.helicsFederateRegisterGlobalTypePublication(self.fed, voltavg, "complex", "")
                currA = "{b}/{m}/current_A".format(b=building, m=meter)
                pubid2 = h.helicsFederateRegisterGlobalTypePublication(self.fed, currA, "complex", "")
                currB = "{b}/{m}/current_B".format(b=building, m=meter)
                pubid3 = h.helicsFederateRegisterGlobalTypePublication(self.fed, currB, "complex", "")
                currC = "{b}/{m}/current_C".format(b=building, m=meter)
                pubid4 = h.helicsFederateRegisterGlobalTypePublication(self.fed, currC, "complex", "")
                pubs[voltavg] = pubid1
                pubs[currA] = pubid2
                pubs[currB] = pubid3
                pubs[currC] = pubid4

            else: 
                # For loads in building NBN
                powera = "{b}/{m}/powerA".format(b=building, m=meter)
                pubid7 = h.helicsFederateRegisterGlobalTypePublication(self.fed, powera, "complex", "")
                pubs["{b}/{m}/constantPowerA".format(b=building, m=meter)] = pubid7
                powerb = "{b}/{m}/powerB".format(b=building, m=meter)
                pubid8 = h.helicsFederateRegisterGlobalTypePublication(self.fed, powerb, "double" , "")
                pubs["{b}/{m}/constantPowerB".format(b=building, m=meter)] = pubid8
                powerc = "{b}/{m}/powerC".format(b=building, m=meter)
                pubid9 = h.helicsFederateRegisterGlobalTypePublication(self.fed, powerc, "double", "")
                pubs["{b}/{m}/constantPowerC".format(b=building, m=meter)] = pubid9
                
        return pubs

    def register_subscription(self, subs):
        subid1 = h.helicsFederateRegisterSubscription(self.fed, "R1/n125/voltage_A", "")
        subs["R1/n125/voltage_A"] = subid1
        
        subid2 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/monthly_fee", "")
        subs["R1/m_t11/monthly_fee"] = subid2

        subid3 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/monthly_energy", "")
        subs["R1/m_t11/monthly_energy"] = subid3

        return subs
             

    def manage_publication_register(self, buildings, pubs):
        #assigning publication to necessary loops and buildings
        for key, value in buildings.items():
            pubs = self.register_publication(key, value, pubs)

        return pubs

    def manage_subscription_register(self, subs):
        #assigning subscriptions for required outputs
        subs = self.register_subscription(subs)
        return subs
        
 





        