from Sheep_minions import *

def display(products,sell,hours,dp=1):
    "change dp to specify number of decimal places to round to (1 by default)"
    print(f"In {hours} hours, it will produce: ",end='')
    for item in products:
        print(f"{products[item]:.{dp}f} {item} ({sell[item]/1000:.{dp}f}k coins)",end=', ')
    print(f'for a total of {sum(sell.values())/1000:.{dp}f}k coins')

hours = 24

A = Sheep(12)
A.Add_Infusion()
A.Add_Postcard()

A.Add_Lava_Bucket(3)
#A.Add_Beacon(5,29)

A.Add_Corrupted_Soil()
#A.Add_Berberis_Injector()
#A.Add_Dia_Spreading()

A.Add_SC3K()
#A.Add_Cheese()

products = A.Products(hours)
sell = value(products,mode='BEST')
display(products,sell,hours)

