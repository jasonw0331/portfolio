import math
from tabulate import tabulate

# lists to store the amortization schedule data
interest_list = []
principal_list = []
principal_paid_list = []
monthly_pay_list = []
period_list = []
beginning_principal = []

# function to calculate the number of periods (n) needed to pay off the loan
def calculate_periods(principal, monthly, annual_ir, extra_payment):
    # convert the annual interest rate to a monthly interest rate
    monthly_ir = annual_ir / 12
    numerator = math.log((monthly + extra_payment) / (monthly + extra_payment - monthly_ir * principal))
    denominator = math.log(1 + monthly_ir)
    n = numerator / denominator
    return n


def main():
    try:
        # user inputs, with error proofing
        principal = float(input('Enter the loan amount: '))
        if principal <= 0:
            print('Amount cannot be less than or equal to zero.')
            exit()
        annual_ir = float(input('Enter the annual interest rate (as decimal, e.g., 0.10 for 10%): '))
        if annual_ir > 1:
            yn = input(f'Are you sure annual principle is {annual_ir*100}%? (y for Yes, n for No)')
            if yn.lower() == 'n':
                print('Please enter value as decimal')
                exit()
            if yn.lower() != 'y' or 'n':
                print('Please confirm annual interest rate')
                exit()
        monthly_pay = float(input('Enter the monthly payment: '))
        if monthly_pay <= principal * (annual_ir / 12):
            print(f'Payment must be greater than the interest rate {round(principal * (annual_ir / 12),2)}')
            exit()

        extra_payment = float(input('Enter the extra payment amount: '))
        if extra_payment < 0:
            print('Payment must be greater or equal to zero')


        monthly_ir = annual_ir / 12
        period = int(calculate_periods(principal, monthly_pay, annual_ir, extra_payment))
        year = int(calculate_periods(principal, monthly_pay, annual_ir, extra_payment)+1) / 12

        #loop for calculating amortization
        for n in range(1,period+2):

            #appends into list of beginning principal
            beginning_principal.append(principal)

            interest_paid = principal * monthly_ir
            principal_paid = monthly_pay - interest_paid

            if n == period+1:
                monthly_pay = principal + interest_paid
                interest_paid = principal * monthly_ir
                principal_paid = monthly_pay - interest_paid

            # update remaining principal
            principal -= principal_paid

            # append calculated values to the respective lists
            interest_list.append(interest_paid)
            principal_list.append(principal)
            principal_paid_list.append(principal_paid)
            monthly_pay_list.append(monthly_pay)
            period_list.append(n)

    except ValueError:
        print('Please enter numeric values')
        exit()



    total_paid = sum(monthly_pay_list)
    total_interest = sum(interest_list)
    total_principal = sum(principal_paid_list)

    amortization_schedule = list(zip(period_list, beginning_principal,monthly_pay_list,interest_list,principal_paid_list,principal_list))

    # table with tabulate
    print(tabulate(amortization_schedule, headers=['Period','Beginning','Payments', 'Interest', 'Principal Paid', 'Principal']))
    # summary
    print(f'Years: {round(year,2)}')
    print(f'Sum of all payments: {round(total_paid,2)}')
    print(f'Interest Total: {round(total_interest,2)}')
    print(f'Principal Total: {round(total_principal,2)}')

main()