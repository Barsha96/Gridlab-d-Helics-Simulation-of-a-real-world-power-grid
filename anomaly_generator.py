import pandas as pd
import random
from datetime import datetime, timedelta


class Anomaly:
    def assign_zeros(self, df, sequence_length):
        #if the sum of the column "Anomaly" of length sequence from the index chosen is less than the sequence length, then there are zeros in it 
        #having zeros in the range will disqualify the index and choose the next index 
        sum_data = 0
        
        while sum_data != sequence_length:
            first_index = random.randint(0, len(df) - sequence_length)
            last_index = first_index + sequence_length - 1
            sum_data = df.loc[first_index:last_index, 'Anomaly'].sum()
            
        # Assign a value to column 'A' within the specified range
        print([first_index, last_index])
        df.loc[first_index:last_index, 'Anomaly'] = 0

    def anm_index_generator(self):
        # Define the start and end timestamps
        start_timestamp = datetime(2022, 8, 10)
        end_timestamp = datetime(2022, 10, 4)

        # Define the time interval between timestamps
        interval = timedelta(minutes=5)

        # Generate a list of timestamps at the specified interval
        timestamps = pd.date_range(start=start_timestamp, end=end_timestamp, freq=interval)

        # Create a dataframe with the "Timestamp" column
        df = pd.DataFrame({'Timestamp': timestamps})
        
        df['Anomaly'] = 1

        # The Specifications
        num_zeros = int(len(df) * 0.2)
        min_sequence_length = 10
        max_sequence_length = 144
        sequence_length_sum = 0

        while sequence_length_sum <= num_zeros:
            
            sequence_length = random.randint(min_sequence_length, max_sequence_length)
            self.assign_zeros(df, sequence_length)
            sequence_length_sum = sequence_length_sum + sequence_length

        return df
        # Create a list of indices to distribute the zeros