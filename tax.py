income = 25500

tax_nds = 25

tax_cash = 15

tax_dog = 3

outcome = income + 1

revenue = 10

while (outcome - outcome*tax_nds/100 - income*tax_cash/100 - outcome*tax_dog/100 - income*revenue/100) < income:
    outcome +=10

print(outcome)