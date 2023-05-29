import helics as h
import pandas as pd
import numpy as np
import json


class PubHub:
    def __init__(self, fed):
        self.fed = fed

    # def add_publication_to_json(self, json_file, key, data_type, unit, obj, prop):
    #     with open(json_file, 'r+') as file:
    #         json_data = json.load(file)

    #         # Check if the publication already exists
    #         for publication in json_data['publications']:
    #             if publication['key'] == key:
    #                 print(f"Publication with key {key} already exists!")
    #                 return

    #         # Add the new publication to the list
    #         new_publication = {
    #             "global": False,
    #             "key": key,
    #             "type": data_type,
    #             "unit": unit,
    #             "info": {
    #                 "object": obj,
    #                 "property": prop
    #             }
    #         }
    #         json_data['publications'].append(new_publication)

    #         # Write the updated JSON data back to the file
    #         file.seek(0)
    #         json.dump(json_data, file, indent=4)
    #         file.truncate()

    # def add_subscription_to_json(self, json_file, key, data_type, unit, obj, prop):
    #     with open(json_file, 'r+') as file:
    #         json_data = json.load(file)

    #         # Check if the subscription already exists
    #         for subscription in json_data['subscriptions']:
    #             if subscription['key'] == key:
    #                 print(f"Subscription with key {key} already exists!")
    #                 return

    #         # Add the new subscription to the list
    #         new_subscription = {
    #             "key": key,
    #             "type": data_type,
    #             "unit": unit,
    #             "info": {
    #                 "object": obj,
    #                 "property": prop
    #             }
    #         }
    #         json_data['subscriptions'].append(new_subscription)

    #         # Write the updated JSON data back to the file
    #         file.seek(0)
    #         json.dump(json_data, file, indent=4)
    #         file.truncate() 

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
                pubs["{b}/{m}/powerA".format(b=building, m=meter)] = pubid7
                powerb = "{b}/{m}/powerB".format(b=building, m=meter)
                pubid8 = h.helicsFederateRegisterGlobalTypePublication(self.fed, powerb, "complex" , "")
                pubs["{b}/{m}/powerB".format(b=building, m=meter)] = pubid8
                powerc = "{b}/{m}/powerC".format(b=building, m=meter)
                pubid9 = h.helicsFederateRegisterGlobalTypePublication(self.fed, powerc, "complex", "")
                pubs["{b}/{m}/powerC".format(b=building, m=meter)] = pubid9
                
        return pubs

    def register_subscription(self, subs):
        
        # config_file = "r1config.json"
        #for node 125
        subid1 = h.helicsFederateRegisterSubscription(self.fed, "R1/n125/voltage_A", "")
        subs["R1/n125/voltage_A"] = subid1
        # self.add_publication_to_json(config_file, "n125/voltage_A", "complex", "volts", "n125", "voltage_A")

        subid2 = h.helicsFederateRegisterSubscription(self.fed, "R1/n125/voltage_B", "")
        subs["R1/n125/voltage_B"] = subid2
        # self.add_publication_to_json(config_file, "n125/voltage_A", "complex", "volts", "n125", "voltage_A")

        subid3 = h.helicsFederateRegisterSubscription(self.fed, "R1/n125/voltage_C", "")
        subs["R1/n125/voltage_C"] = subid3

        subid4 = h.helicsFederateRegisterSubscription(self.fed, "R1/n125/current_A", "")
        subs["R1/n125/current_A"] = subid4

        subid5 = h.helicsFederateRegisterSubscription(self.fed, "R1/n125/current_B", "")
        subs["R1/n125/current_B"] = subid5

        subid6 = h.helicsFederateRegisterSubscription(self.fed, "R1/n125/current_C", "")
        subs["R1/n125/current_C"] = subid6

        subid7 = h.helicsFederateRegisterSubscription(self.fed, "R1/n125/power_A", "")
        subs["R1/n125/power_A"] = subid7

        subid8 = h.helicsFederateRegisterSubscription(self.fed, "R1/n125/power_B", "")
        subs["R1/n125/power_B"] = subid8

        subid9 = h.helicsFederateRegisterSubscription(self.fed, "R1/n125/power_C", "")
        subs["R1/n125/power_C"] = subid9

        subid10 = h.helicsFederateRegisterSubscription(self.fed, "R1/n125/maximum_voltage_error", "")
        subs["R1/n125/maximum_voltage_error"] = subid10

        #for load l131
        subid11 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/measured_voltage_A", "")
        subs["R1/l131/measured_voltage_A"] = subid11

        subid12 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/measured_voltage_B", "")
        subs["R1/l131/measured_voltage_B"] = subid12

        subid13 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/measured_voltage_C", "")
        subs["R1/l131/measured_voltage_C"] = subid13

        subid13 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/constant_power_A", "")
        subs["R1/l131/constant_power_A"] = subid13

        subid14 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/constant_power_B", "")
        subs["R1/l131/constant_power_B"] = subid14

        subid15 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/constant_power_C", "")
        subs["R1/l131/constant_power_C"] = subid15

        subid16 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/constant_impedance_A", "")
        subs["R1/l131/constant_impedance_A"] = subid16

        subid17 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/constant_impedance_B", "")
        subs["R1/l131/constant_impedance_B"] = subid17

        subid18 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/constant_impedance_C", "")
        subs["R1/l131/constant_impedance_C"] = subid18

        subid19 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/constant_current_A", "")
        subs["R1/l131/constant_current_A"] = subid19

        subid20 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/constant_current_B", "")
        subs["R1/l131/constant_current_B"] = subid20

        subid21 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/constant_current_C", "")
        subs["R1/l131/constant_current_C"] = subid21

        subid22 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/power_pf_A", "")
        subs["R1/l131/power_pf_A"] = subid22

        subid23 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/power_pf_B", "")
        subs["R1/l131/power_pf_B"] = subid23

        subid24 = h.helicsFederateRegisterSubscription(self.fed, "R1/l131/power_pf_C", "")
        subs["R1/l131/power_pf_C"] = subid24
        
        #for meter m_t11
        subid25 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/measured_real_energy", "")
        subs["R1/m_t11/measured_real_energy"] = subid25

        subid26 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/measured_reactive_energy", "")
        subs["R1/m_t11/measured_reactive_energy"] = subid26

        subid27 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/measured_power", "")
        subs["R1/m_t11/measured_power"] = subid27

        subid28 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/measured_real_power", "")
        subs["R1/m_t11/measured_real_power"] = subid28

        subid29 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/measured_reactive_power", "")
        subs["R1/m_t11/measured_reactive_power"] = subid29

        subid30 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/measured_voltage_A", "")
        subs["R1/m_t11/measured_voltage_A"] = subid30

        subid31 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/measured_voltage_B", "")
        subs["R1/m_t11/measured_voltage_B"] = subid31

        subid32 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/measured_voltage_C", "")
        subs["R1/m_t11/measured_voltage_C"] = subid32

        subid33 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/measured_current_A", "")
        subs["R1/m_t11/measured_current_A"] = subid33

        subid34 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/measured_current_B", "")
        subs["R1/m_t11/measured_current_B"] = subid34

        subid35 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/measured_current_C", "")
        subs["R1/m_t11/measured_current_C"] = subid35

        subid36 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/monthly_bill", "")
        subs["R1/m_t11/monthly_bill"] = subid36

        subid37 = h.helicsFederateRegisterSubscription(self.fed, "R1/m_t11/monthly_energy", "")
        subs["R1/m_t11/monthly_energy"] = subid37

        subid38 = h.helicsFederateRegisterSubscription(self.fed, "R1/s_01/measured_current_A", "")
        subs["R1/s_01/measured_current_A"] = subid38

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
        
 





        