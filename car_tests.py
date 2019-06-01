from Income_Data import Income_Data
from car import Car

# Test on_ramp
global on_ramps_south
global on_ramps_north
global inc
on_ramps_south = ['I5 North', 'I5 South1','I5 South2', 'Canyon Park', \
                  'WA_522']                  
on_ramps_north = ['Bellevue 4th St', 'Redmond Way', 'Central Way', \
                  'WA 527']
inc = Income_Data() 

def car_tests(): 
    onramp_test()
    city_test()
    income_test()
    offramp_test()

def onramp_test():  
    global on_ramps_south
    global on_ramps_north  
    onramp_error_count = 0
    print("Testing On-Ramp")            
    for i in range(100):
        sc = Car(direction='South')
        nc = Car(direction='North')
        if sc.on_ramp not in on_ramps_south:
            print("Error: Bad On Ramp")
            print(sc.on_ramp)
            onramp_error_count += 1
        elif nc.on_ramp not in on_ramps_north:
            print("Error: Bad On Ramp")
            print(nc.on_ramp)
            onramp_error_count += 1
    if onramp_error_count == 0:    
        print("On-Ramp Test successful")
        
def city_test():
    global on_ramps_south
    global on_ramps_north
    city_error = 0
    print("Testing Cities")
    for i in range(100):
        sc = Car(direction='South')
        nc = Car(direction='North')
        if sc.city != inc.on_ramps_south[sc.on_ramp]:
            print("Error: Bad City")
            print(sc.city)
            city_error += 1 
        elif nc.city != inc.on_ramps_north[nc.on_ramp]:
            print("Error: Bad City")
            print(nc.city)
            city_error += 1         
    if city_error == 0:
        print("City Test successful")
            
def income_test():
    global inc
    income_error = 0    
    print("Testing Income")
    incs = ['low', 'low mid', 'mid', 'upper mid', 'upper']
    for e in incs:
        for i in range(100):
            sc = Car(direction='South')
            nc = Car(direction='North')
            if sc.city == 'Everett':
                if sc.income_class == e:
                    e_inc = inc.everett_income[e]
                    if sc.income < e_inc[0] or sc.income > e_inc[1]:
                        print("Error: Bad income")
                        print(sc.city)
                        print(sc.income_class)
                        print(sc.income)
                        income_error += 1
            elif sc.city == 'Lynnwood':
                if sc.income_class == e:
                    l_inc = inc.lynnwood_income[e]
                    if sc.income < l_inc[0] or sc.income > l_inc[1]:
                        print("Error: Bad income")
                        print(sc.city)
                        print(sc.income_class)
                        print(sc.income)
                        income_error += 1
            elif sc.city == 'Mountlake Terrace':
                if sc.income_class == e:
                    m_inc = inc.mterrace_income[e]
                    if sc.income < m_inc[0] or sc.income > m_inc[1]:
                        print("Error: Bad income")
                        print(sc.city)
                        print(sc.income_class)
                        print(sc.income)
                        income_error += 1
            elif sc.city == 'Bothell':
                if sc.income_class == e:
                    bo_inc = inc.bothell_income[e]
                    if sc.income < bo_inc[0] or sc.income > bo_inc[1]:
                        print("Error: Bad income")
                        print(sc.city)
                        print(sc.income_class)
                        print(sc.income)
                        income_error += 1
            elif nc.city == 'Bothell':
                if nc.income_class == e:
                    bo_inc = inc.bothell_income[e]
                    if nc.income < bo_inc[0] or nc.income > bo_inc[1]:
                        print("Error: Bad income")
                        print(nc.city)
                        print(nc.income_class)
                        print(nc.income)
                        income_error += 1
            elif nc.city == 'Bellevue':
                if nc.income_class == e:
                    be_inc = inc.bellevue_income[e]
                    if nc.income < be_inc[0] or nc.income > be_inc[1]:
                        print("Error: Bad income")
                        print(sc.city)
                        print(sc.income_class)
                        print(sc.income)
                        income_error += 1
            elif nc.city == 'Redmond':
                if nc.income_class == e:
                    r_inc = inc.redmond_income[e]
                    if nc.income < r_inc[0] or nc.income > r_inc[1]:
                        print("Error: Bad income")
                        print(sc.city)
                        print(sc.income_class)
                        print(sc.income)
                        income_error += 1
            elif nc.city == 'Kirkland':
                if nc.income_class == e:
                    k_inc = inc.bellevue_income[e]
                    if nc.income < k_inc[0] or nc.income > k_inc[1]:
                        print("Error: Bad income")
                        print(sc.city)
                        print(sc.income_class)
                        print(sc.income)
                        income_error += 1
    if income_error == 0:
        print("Income Test successful")
        
def offramp_test():
    # to be worked on
    print("Test not finished yet")
        
car_tests()
