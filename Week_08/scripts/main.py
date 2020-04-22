from simulate import Supermarket

if __name__ == '__main__':
    # Operational Constants
    INIT_CUSTOMER_STATES = ['dairy', 'drinks', 'fruit','spices']
    CUSTOMER_STATE_KEY = ['checkout','dairy', 'drinks', 'fruit','spices']
    CUST_STATE_VAL = [0,1,2,3,4]
    CUST_STATE_DICT = dict(zip(CUSTOMER_STATE_KEY, CUST_STATE_VAL))


    rewe = Supermarket(5, CUST_STATE_DICT, CUSTOMER_STATE_KEY, INIT_CUSTOMER_STATES, corona = True)
    a = rewe.shop()
    print(a)
