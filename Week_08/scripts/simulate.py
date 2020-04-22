from customer import SupermarketCustomer
from operational import cust_per_min, cust_per_min_corona, get_tpm, get_tpm_corona

import pandas as pd
import numpy as np

class Supermarket:
    def __init__(self, days, customer_state_dict, customer_state_key,
                initial_customer_states, corona = False):
        #self.cust_per_min = cust_per_min
        self.days = days
        self.customer_state_key = customer_state_key
        self.customer_state_dict = customer_state_dict
        self.initial_customer_states = initial_customer_states
        self.corona = corona
        if self.corona == True:
            self.cust_per_min = cust_per_min_corona()
            self.transition_prob_matrix = get_tpm_corona()
        else:
            self.cust_per_min = cust_per_min()
            self.transition_prob_matrix = get_tpm()




    def make_a_day_in_supermarket(self):
        """Simulates a day with number of people allowed in a supermarket - derived from the data"""
        customer_number = pd.DataFrame(columns = ['time','customer_no', 'locations'])
        cust_no = 0
        for i, row in self.cust_per_min.iterrows():
            nr_ppl = row['mean']
            std = row['stdev']
            upper = nr_ppl + std
            if nr_ppl > 0:
                random_nr = np.random.randint(nr_ppl, upper+1)
                for a in range(random_nr):
                    customer = SupermarketCustomer(self.customer_state_key, self.initial_customer_states, self.customer_state_dict, self.transition_prob_matrix)
                    traj = customer.simulate()
                    cust_no = cust_no + 1
                    customer_number = customer_number.append({'time': str(i), 'customer_no':cust_no, 'locations': traj}, ignore_index = True)
            else:
                pass
        return customer_number

    def shop(self):
        """Creates a shopping pattern for x number of days in a supermarket"""

        # Create all necessary duration distributions for each aisle
        dairyd = pd.read_csv('../data/dairy_duration.csv')
        fruitsd = pd.read_csv('../data/fruit_duration.csv')
        spicesd = pd.read_csv('../data/spices_duration.csv')
        drinksd = pd.read_csv('../data/drinks_duration.csv')
        checkoutd = pd.read_csv('../data/checkout_duration.csv')
        dairy_duration = dairyd['duration_min'].to_numpy()
        dairy_duration = np.delete(dairy_duration, np.where(dairy_duration == dairy_duration.max()))
        dairy_duration = np.delete(dairy_duration, np.where(dairy_duration == 0))
        fruit_duration = fruitsd['duration_min'].to_numpy()
        fruit_duration = np.delete(fruit_duration, np.where(fruit_duration == fruit_duration.max()))
        fruit_duration = np.delete(fruit_duration, np.where(fruit_duration == 0))
        spices_duration = spicesd['duration_min'].to_numpy()
        spices_duration = np.delete(spices_duration, np.where(spices_duration == 0))
        drinks_duration = drinksd['duration_min'].to_numpy()
        drinks_duration = np.delete(drinks_duration, np.where(drinks_duration == 0))

        # Loop over days to create several days worth of shopping history
        # Create the template dataframe to be appended
        final_cust = pd.DataFrame(columns=['date', 'time', 'customer_no', 'location', 'min_spent'])
        for day in range(0, self.days):
            # Create a new day variable for each loop
            date=pd.to_datetime('today') + pd.Timedelta(np.timedelta64(day, 'D'))

            # Simulate a day in a supermarket
            cust_df = self.make_a_day_in_supermarket()
            # Create the duration variable - will be overwritten by the aisle
            # Construct the dataframe
            dd = 0
            for i, row in cust_df.iterrows():
                initial_time = row['time']
                cust_id = row['customer_no']
                location_list = row['locations']
                for element in location_list:
                    if element == 'dairy':
                        dd = int(np.random.choice(dairy_duration))
                    if element == 'fruits':
                        dd = int(np.random.choice(fruit_duration))
                    if element == 'spices':
                        dd = int(np.random.choice(spices_duration))
                    if element == 'drinks':
                        dd = int(np.random.choice(drinks_duration))
                    if element == 'checkout':
                        dd = int(np.random.choice(5, 1))
                    final_cust = final_cust.append({'date': pd.to_datetime(date),
                                                    'time': initial_time, 'customer_no': cust_id,
                                                    'location': element, 'min_spent': pd.Timedelta(np.timedelta64(dd, 'm'))}, ignore_index = True)
                # Final dataframe aesthetics

                final_cust['d'] = final_cust['date'].dt.date
                final_cust['time'] = pd.to_datetime(final_cust['time'])
                final_cust['min_number'] = final_cust['min_spent'].dt.seconds/60
                final_cust['min_spent_cumul'] = final_cust.groupby('customer_no')['min_number'].cumsum()
                final_cust['min_spent_cumul'] = pd.to_timedelta(final_cust['min_spent_cumul'], unit = 'm')
                final_cust['timestamp_new'] = final_cust['time']+ final_cust['min_spent_cumul']
                final_cust['timestamp_new'] = final_cust['timestamp_new'].dt.time

        #Clean up the dataframe
        clean_final = final_cust[['d','timestamp_new', 'customer_no', 'location']]
        clean_final = clean_final.set_axis(['date', 'time', 'customer_no', 'location'], axis=1, inplace=False)
        clean_final = clean_final.sort_values(by = ['date', 'time'])
        clean_final = clean_final.reset_index(drop=True)
        if self.corona == True:
            clean_final.to_csv('../data/simulated_corona.csv', index = True, header = True)
        else:
            clean_final.to_csv('../data/simulated.csv', index = True, header = True)
        return clean_final
