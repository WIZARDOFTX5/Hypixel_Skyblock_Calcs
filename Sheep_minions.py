class Sheep():
    def __init__(self,tier):
        self.__tier = int(tier)
        self.__BaseSpeed = [None,24,24,22,22,20,20,18,18,16,16,12,9][self.__tier]
        self.__BonusSpeed = 100
        self.__Products = {'WOOL':1,        # products generated per kill
                           'MUTTON':1}
        self.__HourlyCost = {} # items consumed per hour (eg, using tasty cheese would have a hourly cost of 1 tasty cheese)
        self.__HourlyBonus = {} # extra items produced per hour (eg, berberis would produce 12 lush berberis per hour)
    def __repr__(self):
        return f"Tier {self.__tier} sheep minion, with a {self.__BaseSpeed*100/self.__BonusSpeed}s action speed"
    # Follow the priority of the functions in ascending order. Eg must add diamond spreading(2) before sc3k(3)
    def Add_Infusion(self):
        "Priority: 1"
        self.__BonusSpeed += 10
    def Add_Beacon(self,tier,minions):
        "Priority: 1 (specify number of minions to split power crystal cost)"
        self.__BonusSpeed += int(tier)*2
        self.__HourlyCost['POWER_CRYSTAL'] = 1/(48*int(minions))
    def Add_Postcard(self):
        "Priority: 1"
        self.__BonusSpeed += 5
    def Add_Lava_Bucket(self,tier):
        "Priority:1 (t1 is ench lava, t2 is magma, t3 is plasma)"
        self.__BonusSpeed += 20 + int(tier)*5
    def Add_Berberis_Injector(self):
        "Priority: 1"
        self.__BonusSpeed += 15
        self.__HourlyBonus['LUSH_BERBERIS'] = 12  # 1 berberis every 5 minutes
    def Add_Corrupted_Soil(self):
        "Priority: 1"
        self.__Products['CORRUPTED_FRAGMENT'] = 1
        self.__Products['SULPHUR_ORE'] = 1  # for some reason SULPHUR is gunpowder according to bz api?!
    def Add_Dia_Spreading(self): 
        "Priority: 2"
        self.__Products['DIAMOND'] = 0.1*sum(self.__Products.values())
    def Add_SC3K(self):    
        "Priority: 3"      
        for product,amount in self.__Products:
            if product == 'CORRUPTED_FRAGMENT':
                continue
            else:
                if product == 'SULPHUR_ORE':
                    self.__Products['ENCHANTED_SULPHUR'] = amount//160
                    self.__Products[product] = amount%160
                else:
                    self.__Products['ENCHANTED_'+product] = amount//160
                    self.__Products[product] = amount%160
    def profit(self,hours):
        pass

A = Sheep(12)
A.Add_Infusion()
A.Add_Lava_Bucket(3)
A.Add_Postcard()
print(A)