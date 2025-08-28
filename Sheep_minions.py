import requests
from collections import Counter
NPC_SELL = {'WOOL':2,'ENCHANTED_WOOL':320,
            'MUTTON':5,'ENCHANTED_MUTTON':800,
            'DIAMOND':8,'ENCHANTED_DIAMOND':1,
            'LUSH_BERBERIS':3,'ENCHANTED_LUSH_BERBERIS':480,
            'SULPHUR_ORE':10,'ENCHANTED_SULPHUR':1600,
            'CORRUPTED_FRAGMENT':1}
def value(products:dict,mode,offer=True):
    "mode can be 'NPC','BZ' or 'BEST'. making a bz offer is True by default (offer=True)"
    api = "https://api.hypixel.net/skyblock/bazaar"
    bz = requests.get(api).json()
    if bz.get('success') != True:
        return {"Error fetching api":"Error fetching api"}
    values = {}
    if mode == 'NPC':
        for item in products:
            # hopper tax multiplies value by 0.9
            values[item] = 0.9*products[item]*(NPC_SELL[item] if NPC_SELL.get(item) != None else bz['products'][item]['quick_status']['sellPrice' if offer else 'buyPrice'])
    elif mode == 'BZ':
        for item in products:
            values[item] = products[item]*(NPC_SELL[item] if bz['products'].get(item) == None else bz['products'][item]['quick_status']['sellPrice' if not offer else 'buyPrice'])
    else:  # take best price from either npc or bz
        for item in products:
            values[item] = products[item]*max(NPC_SELL.get(item,0), bz['products'].get(item,{}).get('quick_status',{}).get('sellPrice' if not offer else 'buyPrice',0))
    return values
class Sheep():
    def __init__(self,tier):
        self.__tier = int(tier)
        self.__BaseSpeed = [None,24,24,22,22,20,20,18,18,16,16,12,9][self.__tier]
        self.__BonusSpeed = 100
        self.__Products = {'WOOL':1,        # products generated per kill
                           'MUTTON':1}
        self.__HourlyCost = {} # items consumed per hour (eg, using tasty cheese would have a hourly cost of 1 tasty cheese)
        self.__HourlyBonus = {} # extra items produced per hour (eg, berberis would produce 12 lush berberis per hour)
        self.__MinimumPriority = 0
    def __repr__(self):
        return f"Tier {self.__tier} sheep minion, with a {self.__BaseSpeed*100/self.__BonusSpeed}s action speed"
    # Follow the priority of the functions in ascending order. Eg must add diamond spreading(2) before sc3k(3)
    def PriorityCheck(self,priority):
        if self.__MinimumPriority > priority:
            raise ValueError(f"Cannot perform method of priority {priority} when minimum priority is {self.__MinimumPriority}")
        else:
            self.__MinimumPriority = priority
    def Add_Infusion(self):
        "Priority: 1"
        Priority = 1
        self.PriorityCheck(Priority)
        self.__BonusSpeed += 10
    def Add_Beacon(self,tier,minions):
        "Priority: 1 (specify number of minions to split power crystal cost)"
        Priority = 1
        self.PriorityCheck(Priority)
        self.__BonusSpeed += int(tier)*2
        self.__HourlyCost['POWER_CRYSTAL'] = 1/(48*int(minions))
    def Add_Postcard(self):
        "Priority: 1"
        Priority = 1
        self.PriorityCheck(Priority)
        self.__BonusSpeed += 5
    def Add_Lava_Bucket(self,tier):
        "Priority:1 (t1 is ench lava, t2 is magma, t3 is plasma)"
        Priority = 1
        self.PriorityCheck(Priority)
        self.__BonusSpeed += 20 + int(tier)*5
    def Add_Berberis_Injector(self):
        "Priority: 1"
        Priority = 1
        self.PriorityCheck(Priority)
        self.__BonusSpeed += 15
        self.__HourlyBonus['LUSH_BERBERIS'] = 12  # 1 berberis every 5 minutes
    def Add_Corrupted_Soil(self):
        "Priority: 1"
        Priority = 1
        self.PriorityCheck(Priority)
        self.__Products['CORRUPTED_FRAGMENT'] = 1
        self.__Products['SULPHUR_ORE'] = 1  # for some reason SULPHUR is gunpowder according to bz api?!
    def Add_Dia_Spreading(self): 
        "Priority: 2"
        Priority = 2
        self.PriorityCheck(Priority)
        self.__Products['DIAMOND'] = 0.1*sum(self.__Products.values())
        self.__HourlyBonus['DIAMOND'] = 0.1*sum(self.__HourlyBonus.values())
    def Add_Cheese(self):
        "Priority: 3"
        Priority = 3
        self.PriorityCheck(Priority)
        self.__HourlyCost['CHEESE_FUEL'] = 1
        for item in self.__Products:
            self.__Products[item] *= 2
        for item in self.__HourlyBonus:
            self.__HourlyBonus[item] *= 2
    def Add_SC3K(self):    
        "Priority: 3" 
        Priority = 3
        self.PriorityCheck(Priority)     
        for product in self.__Products.copy():
            amount = self.__Products.pop(product)
            if product == 'CORRUPTED_FRAGMENT':
                continue
            else:
                if product == 'SULPHUR_ORE':
                    self.__Products['ENCHANTED_SULPHUR'] = amount/160
                else:
                    self.__Products['ENCHANTED_'+product] = amount/160
    def Products(self,hours):
        actionSpeed = self.__BaseSpeed*100/self.__BonusSpeed
        Hourlyactions = 1800/actionSpeed
        result = {}
        for item in self.__Products|self.__HourlyBonus|self.__HourlyCost:
            result[item] = hours*(Hourlyactions*self.__Products.get(item,0) + self.__HourlyBonus.get(item,0) - self.__HourlyCost.get(item,0))
        return result



