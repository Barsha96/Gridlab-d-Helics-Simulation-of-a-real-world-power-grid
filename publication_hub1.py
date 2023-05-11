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
                # For loads in building NBN and others that consume power
                powera = "{b}/{m}/powerA".format(b=building, m=meter)
                pubid7 = h.helicsFederateRegisterGlobalTypePublication(self.fed, powera, "complex", "")
                pubs["{b}/{m}/powerA".format(b=building, m=meter)] = pubid7
                powerb = "{b}/{m}/powerB".format(b=building, m=meter)
                pubid8 = h.helicsFederateRegisterGlobalTypePublication(self.fed, powerb, "double" , "")
                pubs["{b}/{m}/powerB".format(b=building, m=meter)] = pubid8
                powerc = "{b}/{m}/powerC".format(b=building, m=meter)
                pubid9 = h.helicsFederateRegisterGlobalTypePublication(self.fed, powerc, "double", "")
                pubs["{b}/{m}/powerC".format(b=building, m=meter)] = pubid9
                
        return pubs

    def register_subscription(self, building, meters, subs):
        
        # config_file = "r1config.json"
        #for node 125
        subid1 = h.helicsFederateRegisterSubscription(self.fed, "R1/nef8_2/voltage_A", "")
        subs["R1/nef8_2/voltage_A"] = subid1
        # self.add_publication_to_json(config_file, "nef8_2/voltage_A", "complex", "volts", "nef8_2", "voltage_A")

        subid2 = h.helicsFederateRegisterSubscription(self.fed, "R1/nef8_2/voltage_B", "")
        subs["R1/nef8_2/voltage_B"] = subid2
        # self.add_publication_to_json(config_file, "nef8_2/voltage_A", "complex", "volts", "nef8_2", "voltage_A")

        subid3 = h.helicsFederateRegisterSubscription(self.fed, "R1/nef8_2/voltage_C", "")
        subs["R1/nef8_2/voltage_C"] = subid3
        
        return subs

           

    def manage_publication_register(self, buildings, pubs):
        #assigning publication to necessary loops and buildings
        for key, value in buildings.items():
            pubs = self.register_publication(key, value, pubs)

        return pubs

    def manage_subscription_register(self, buildings, subs):
        #assigning subscriptions for required outputs
        for key, value in buildings.items():
            subs = self.register_subscription(key, value, subs)
        return subs
        
 





        