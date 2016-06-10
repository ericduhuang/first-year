def initialize():
#reset all values, activate the card and assume the buyer has made no purchases\
#yet (basically a new card).
    global cur_balance_owing_intst, cur_balance_owing_recent, active
    global last_update_day, last_update_month
    global last_country, last_country2
    
    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0
    active = True
    
    last_update_day, last_update_month = 1, 1
    
    last_country = None
    last_country2 = None
    
    MONTHLY_INTEREST_RATE = 0.05

def date_same_or_later(day1, month1, day2, month2):
# Assume dates given are valid integers in 2016. First compares whether the
#current month is after the previous one. If the months are the same, the
#function compares the days. If the day is before the last saved day, False is
#returned
    if month1 > month2:
        return True
    elif month1 == month2:
        if day1 >= day2:
            return True
        else:
            return False
    elif month1 < month2:
        return False
    
def all_three_different(c1, c2, c3):
#compare the three values, return true when they are all different. Needs to take
#into account when initialize() is used, thus the None comaprison lines are needed.
    if c1 != c2 and c2 != c3 and c1 != c3:
        if c2 == None or c3 == None:
            return False
        else: 
            return True
    else:
        return False
        
def purchase(amount, day, month, country):
#Assume amount is greater than zero, that country is a valid country and that
# day and month are valid integers in the year 2016. Determine whether the card
# is active, then determine whether date is valid; return error if these are not
#true. Compare all date cases, and add interest to balances based on whether the
#month is after last_update_month. Then add amount spent to 
#cur_balance_owing_recent. Update last_update_month, last_update_day, 
#last_country and last_country2 based on parameters in this function. 
    global cur_balance_owing_intst, cur_balance_owing_recent, active
    global last_update_day, last_update_month
    global last_country, last_country2
    if all_three_different(country, last_country, last_country2) == True:
        active = False
    if date_same_or_later(day, month, last_update_day, last_update_month) ==\
        False or active == False:
        return "error"
    if month == last_update_month:
        cur_balance_owing_recent += amount
    elif month > last_update_month:
        cur_balance_owing_intst = cur_balance_owing_recent * ((1.05) ** \
        (month - last_update_month - 1)) + cur_balance_owing_intst * ((1.05) **\
        (month - last_update_month))
        cur_balance_owing_recent = amount
    last_update_month = month
    last_update_day = day
    last_country2 = last_country
    last_country = country
    return
    
def amount_owed(day, month):
#Assume a valid date in 2016 is given. Compare the inputted date to the last 
#date; return false if the inputted date is before. Compare the months and add 
#compound interest as necessary if the input month is greater than 
#last_update_month. Return the total amount owed 
#(which includes the interest balance and the recent balance). 
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    if date_same_or_later(day, month, last_update_day, last_update_month) ==\
        False:
        return "error"
    elif month == last_update_month:
        total = cur_balance_owing_intst + cur_balance_owing_recent
    elif month > last_update_month:
        cur_balance_owing_intst = cur_balance_owing_recent * ((1.05) ** \
        (month - last_update_month - 1)) + cur_balance_owing_intst * ((1.05) **\
        (month - last_update_month))
        cur_balance_owing_recent = 0
        total = cur_balance_owing_intst
    last_update_day = day
    last_update_month = month
    return total
    
    
def pay_bill(amount, day, month):
#Assume amount is a valid integer and that the date is a valid date in 2016. 
#Compare the input date with the last update date and return error if it is 
#after. Calculate the interest based on what month it is. If the payment is 
#greater than the owed amount return "too much". Subtract the payment amount 
#from the total owed, but first from the interest amount. If the amount is 
#greater than the interest amount, then subtract the remainder from the recent 
#balance. Set the last update date to the current date.
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    if date_same_or_later(day, month, last_update_day, last_update_month) == \
        False:
        return "error"
    else: 
        if month == last_update_month:
            total = cur_balance_owing_intst + cur_balance_owing_recent
            if amount > total:
                return "Paying too much"
            if total >= amount:
                cur_balance_owing_intst -= amount
                if cur_balance_owing_intst < 0:
                    cur_balance_owing_recent += cur_balance_owing_intst
                    cur_balance_owing_intst = 0
        elif month > last_update_month:
            cur_balance_owing_intst = cur_balance_owing_recent * ((1.05) ** \
            (month - last_update_month - 1)) + cur_balance_owing_intst * ((1.05)\
             ** (month - last_update_month))
            cur_balance_owing_recent = 0
            if amount > cur_balance_owing_intst :
                return "too much"
            else:
                cur_balance_owing_intst -= amount
    last_update_day = day
    last_update_month = month
    return
    
initialize()

if __name__ == '__main__':
#Starter test code
    initialize()
    purchase(80, 8, 1, "Canada")
    print("Now owing:", amount_owed(8, 1))      #80.0
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      #30.0     (=80-50)
    print("Now owing:", amount_owed(6, 3))      #31.5     (=30*1.05)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3))      #71.5     (=31.5+40)
    pay_bill(30, 7, 3)
    print("Now owing:", amount_owed(7, 3))      #41.5     (=71.5-30)
    print("Now owing:", amount_owed(1, 5))      #43.65375 (=1.5*1.05*1.05+40*1.05)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5))      #83.65375 
    print(purchase(50, 3, 5, "United States"))  #error    (3 diff. countries in 
                                                #          a row)
                                                
    print("Now owing:", amount_owed(3, 5))      #83.65375 (no change, purchase
                                                #          declined)
    print(purchase(150, 3, 5, "Canada"))        #error    (card disabled)
    print("Now owing:", amount_owed(1, 6))      #85.8364375 
                                                #(43.65375*1.05+40)
                                            
#testing purchases in same month
    initialize()
    purchase(10, 1, 1,"CAN")                    #10.0
    print ("Now owing:", amount_owed(1,1))
    pay_bill(5, 2, 1)                           #10 - 5 = 5
    print ("Now owing:", amount_owed(2,1))       
    print(purchase(20, 1, 1, "CAN"))            #N/A, error
    print ("Now owing:", amount_owed(2,1))      
#testing compound interest
    initialize()
    purchase(100, 1, 1, "CAN")                  #100.0
    print ("Now owing:", amount_owed(1,1))
    print ("Now owing:", amount_owed(1,2))      #100 is moved to balance-intst
    print ("Now owing:", amount_owed(1,3))      #100*1.05
    print ("Now owing:", amount_owed(1,5))      #105 * (1.05^(5-3)) = 115.7625
    print ("Now owing:", amount_owed(1,12))     #115.7625* (1.05^(12-5)) = 162.8894627
#testing movement of recent balance to interest balance
    initialize()
    purchase (100, 1, 1, "CAN")                  #100
    print ("Now owing:", amount_owed(1,2))
#testing date_same_or_later
    initialize()
    purchase(10,3,1,"CAN")
    print(amount_owed(1,1))                     #error
#testing deactivation
    initialize()
    purchase(10,3,1,"CAN")                      #10.0
    print ("Now owing:", amount_owed(3,1))
    purchase(10, 4, 1, "CHINA")                 #10 + 10
    print ("Now owing:", amount_owed(4,1))      
    print (purchase(10,4,1,"USA"))              #error because 3 different countries
#testing pay bill
    initialize()
    purchase(80,1,1,"CAN")                      #80
    print("Now owing:", amount_owed(1,1))        
    pay_bill(40, 1, 1)                          #80 - 40 = 40
    print("Now owing:", amount_owed(1,1))
    purchase(30,1,3,"CAN")                      
    print("Now owing:", amount_owed(1,3))       # 40 * 1.05 + 30 = 72
    pay_bill(40, 1, 3)                         
    print("Current interest balance is:", cur_balance_owing_intst)#40*1.05 - 40 = 2
    print("Current recent balance is:", cur_balance_owing_recent) # 30
    print("Now owing:", amount_owed(1,4))       #30 + 2*1.05 = 32.1
    print (pay_bill(50, 1, 4))                  #Paying too much
    
    
    