import cmath

# Given voltages
voltage_A = 7057.84615
voltage_B = 7062.84615
voltage_C = 7012.85714

# Calculate positive sequence voltage
positive_sequence_voltage = (voltage_A + voltage_B*cmath.exp(2*cmath.pi/3*1j) + voltage_C*cmath.exp(-2*cmath.pi/3*1j))/3

# Print result
print("Positive Sequence Voltage: {} volts".format(positive_sequence_voltage))