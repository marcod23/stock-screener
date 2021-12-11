
'''
This input would be used for the simpler model below

#eps = float(input("Enter current EPS: "))
#pe_ratio = float(input("Enter P/E Ratio: "))
#earning_growrate = float(input("Enter earnings growth rate: "))
'''

fcf_growrate = float(input("Enter free cash flow growth rate: "))
fcf = float(input("Enter starting free cash flow: "))
shares_outstanding = float(input("Enter shares outstanding: "))
discount_rate = float(input("Enter discount rate: "))
terminal_growrate = float(input("Enter terminal value growth rate: "))

'''
A simpler model to calculate fair price just using PE ratio and future projected EPS

future_eps = eps * (1 + earning_growrate)**10
future_share_price = pe_ratio * future_eps
fair_price = future_share_price / (1 + rate_of_return)**10
mos30 = fair_price * 0.7
mos50 = fair_price * 0.5

print(fair_price)
print(mos30)
print(mos50)
'''

 '''
 A discounted cash flow model using the input given by the user
 '''
present_value = 0
q_discount_rate = ((1 + discount_rate)**(0.25)) - 1
for x in range(10):
    fcf *= 1 + fcf_growrate
    q_fcf = fcf / 4
    for y in range(1, 5):
        present_value += q_fcf / (1 + q_discount_rate)**(4*x + y)

terminal_value = ((fcf * (1 + terminal_growrate)) / (discount_rate - terminal_growrate)) / (1 + discount_rate)**10

fair_value = present_value + terminal_value
dcf_fair_price = fair_value / shares_outstanding
dcf_mos30 = dcf_fair_price * 0.7
dcf_mos50 = dcf_fair_price * 0.5

print(fair_value)
print(dcf_fair_price)
print(dcf_mos30)
print(dcf_mos50)

