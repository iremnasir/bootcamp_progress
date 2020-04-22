import numpy as np
from operational import get_key, get_initial_proba, get_tpm

class SupermarketCustomer:


    """
    A class that can create a shopping trajectory for a single
    supermarket customer. It takes the possible initial and all state spaces,
    transition prob matrix, possible initial loc array
    """

    def __init__(self, state_space, initial_state_space, customer_state_dict, transition_prob_matrix,
                    inital_location_probabilities = get_initial_proba(), corona=False):
        self.state_space = state_space
        self.initial_state_space = initial_state_space
        self.transition_prob_matrix = transition_prob_matrix
        self.initial_location_probabilities = inital_location_probabilities
        self.state = np.random.choice(self.initial_state_space, p=self.initial_location_probabilities)
        self.customer_state_dict = customer_state_dict

        """
        Operating parameters:
        state_space = list of possible states in a supermarket
        initial_state_space = list of possible states at the beginning of a simulation
        transition_prob_matrix = DataFrame derived from EDA
        first_location_probabilities = array of probabilities of first location
        """


    def initial_state_vector(self):
        """
        Takes the initial state key
        Returns an initial state vector including checkout state
        """
        if self.state == 'checkout': # raise Exception
            return None
        shape_of_matrix = len(self.state_space)
        zero_vec = np.zeros(shape_of_matrix)
        init_val = self.customer_state_dict[self.state]
        zero_vec[init_val] = 1
        return zero_vec

    def move_next(self):
        """Takes the initial state vector
        Converts it to value and makes an initial state vector
        From this vector, generates the next_state_prob_vec
        with given transition_prob_matrix
        """
        zero_vec = self.initial_state_vector()
        next_state_prob_vec = zero_vec.dot(self.transition_prob_matrix)
        next_state_val = np.random.choice(range(len(self.state_space)), p=next_state_prob_vec)
        self.state = get_key(next_state_val, self.customer_state_dict)
        return self.state

#Check if it makes sense to have it here
    def simulate(self):
        """Simulate the customer behavior n times
        Exit when customer ends up in checkout"""
        customer_trajectory = [self.state]
        while True:
            customer_trajectory.append(self.move_next())
            if self.state == 'checkout':
                break
        return customer_trajectory
