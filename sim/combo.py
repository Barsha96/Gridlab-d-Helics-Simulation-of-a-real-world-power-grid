import helics

# Create and configure federate info object
fedinfo = helics.helicsCreateFederateInfo()
helics.helicsFederateInfoSetCoreName(fedinfo, "TestCore")
helics.helicsFederateInfoSetCoreTypeFromString(fedinfo, "zmq")
helics.helicsFederateInfoSetTimeProperty(fedinfo, helics.helics_property_time_delta, 1.0)

# Create and configure federate
fed = helics.helicsCreateCombinationFederate("Publisher", fedinfo)

# Register a global type publication for complex numbers
pub = helics.helicsFederateRegisterGlobalTypePublication(fed, "Publication", helics.HELICS_DATA_TYPE_COMPLEX, "")

# Enter execution mode
helics.helicsFederateEnterExecutingMode(fed)

# Publish data to the publication
value = 3 + 4j
helics.helicsPublicationPublishComplex(pub, value.real, value.imag)

# Create and configure subscriber federate
sub_fed = helics.helicsCreateCombinationFederate("Subscriber", fedinfo)

# Subscribe to the publication from the other federate
sub = helics.helicsFederateRegisterSubscription(sub_fed, "Publication", "")

# Enter execution mode for the subscriber federate
helics.helicsFederateEnterExecutingMode(sub_fed)

# Wait for data to be received
while not helics.helicsInputIsUpdated(sub):
    current_time = helics.helicsFederateRequestTime(sub_fed, helics.HELICS_TIME_MAXTIME)

# Get the received value from the subscription
received_value_real, received_value_imag = helics.helicsInputGetComplex(sub)
received_value = complex(received_value_real, received_value_imag)
print(f"Received value: {received_value}")

# Finalize and clean up federates
helics.helicsFederateFinalize(fed)
helics.helicsFederateFinalize(sub_fed)
helics.helicsFederateFree(fed)
helics.helicsFederateFree(sub_fed)
helics.helicsFederateInfoFree(fedinfo)
helics.helicsCleanupLibrary()