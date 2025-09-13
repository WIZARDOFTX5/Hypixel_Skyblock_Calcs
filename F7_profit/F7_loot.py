import requests
from random import choices

# CONFIG

sell_offer = False   # sell method for loot, True for sell offer, False for sell instantly

TREASURE_BONUS = 1.03  # 1.03 for Treasure artifact, 1.02 for Ring, 1.01 for Talisman, 1.00 for None

BOSS_LUCK_BONUS = 10  # 10 for Boss Luck 4, 5 for level 3, 3 for level 2, 1 for level 1, 0 for None

# END OF CONFIG










# CONSTANTS

SELL_TYPE = 'buyPrice' if sell_offer else 'sellPrice'

SCORE_BONUS = 1.05

# AH PRICES (idk how use ah api) last updated on 13/9/2025
AH_PRICE = {'NECRON_HANDLE': 560000000,
            'AUTO_RECOMBOBULATOR': 10000000,
            'WITHER_CHESTPLATE': 10000000,
            'WITHER_LEGGINGS': 5600000,
            'WITHER_HELMET': 2000000,
            'WITHER_BOOTS': 1000000,
            'WITHER_CLOAK': 3200000,
            'STORM_THE_FISH': 0,
            'MAXOR_THE_FISH': 0,
            'GOLDOR_THE_FISH': 0,
            'placeholder': 0
            }



# BZ API

api = "https://api.hypixel.net/skyblock/bazaar"
bz = requests.get(api).json()
if bz['success'] != True:
    raise ValueError('Bz api didnt work :(')



# LOOT TABLE, all loot tables should be sorted in descending quality

class Loot():
    TOTAL_WEIGHT = 13706   # base total weight of bedrock chest. Note that items not from bedrock cannot have rng meter on it
    def __init__(self,id,cost,weight,quality):
        self.id = id
        self.__cost = cost
        self.__value = AH_PRICE.get(id,'not ah item')
        if self.__value == 'not ah item':
            self.__value = bz['products'][id]['quick_status'][SELL_TYPE]
        self.profit = self.__value - self.__cost
        self.__base_weight = weight
        self.weight = weight
        self.quality = quality
    def reset_weight(self):
        self.weight = self.__base_weight
    def apply_meter(self,runs):
        self.weight = self.__base_weight*(1+min(runs*self.__base_weight*2/self.TOTAL_WEIGHT,2))
    def apply_paul(self):  # does not take into account the 2mil base cost. remember to account for that in later calculations
        self.profit = self.__value - self.__cost*0.8
    def __repr__(self):
        return self.id

BEDROCK_LOOT = [Loot('NECRON_HANDLE',98000000,15,360),
                Loot('SHADOW_WARP_SCROLL',48000000,20,350),
                Loot('WITHER_SHIELD_SCROLL',48000000,20,350),
                Loot('IMPLOSION_SCROLL',48000000,20,350),
                Loot('AUTO_RECOMBOBULATOR',8000000,80,330),
                Loot('WITHER_CHESTPLATE',8000000,80,310),
                Loot('ENCHANTMENT_ULTIMATE_ONE_FOR_ALL_1',0,80,290),
                Loot('RECOMBOBULATOR_3000',4000000,400,250),
                Loot('WITHER_LEGGINGS',4000000,320,250),
                Loot('WITHER_CLOAK',2500000,480,230),
                Loot('WITHER_HELMET',2000000,480,210),
                Loot('WITHER_BLOOD',1000000,480,210),
                Loot('ENCHANTMENT_ULTIMATE_SOUL_EATER_1',0,800,180),
                Loot('FUMING_POTATO_BOOK',0,400,175),
                Loot('WITHER_BOOTS',500000,480,170),
                Loot('WITHER_CATALYST',0,400,160),
                Loot('HOT_POTATO_BOOK',0,800,160),
                Loot('PRECURSOR_GEAR',0,1200,140),
                Loot('ENCHANTMENT_ULTIMATE_NO_PAIN_NO_GAIN_2',0,400,120),
                Loot('ENCHANTMENT_ULTIMATE_COMBO_2',0,1000,120),
                Loot('ENCHANTMENT_REJUVENATE_3',0,1000,100),
                Loot('ENCHANTMENT_ULTIMATE_BANK_3',0,500,100),
                Loot('ENCHANTMENT_ULTIMATE_WISDOM_2',0,500,100),
                Loot('ENCHANTMENT_ULTIMATE_WISE_2',0,800,100),
                Loot('ENCHANTMENT_ULTIMATE_JERRY_3',0,600,100),
                Loot('ENCHANTMENT_ULTIMATE_LAST_STAND_2',0,1000,100),
                Loot('ENCHANTMENT_INFINITE_QUIVER_7',0,1000,80),
                Loot('ENCHANTMENT_FEATHER_FALLING_7',0,320,80),
                Loot('STORM_THE_FISH',0,10,61),
                Loot('MAXOR_THE_FISH',0,10,61),
                Loot('GOLDOR_THE_FISH',0,10,61),
                Loot('ESSENCE_WITHER',0,1,10),
                Loot('ESSENCE_UNDEAD',0,0,1)]


# chest functions

def weight(loot:Loot):
    return loot.weight

def profit(loot:Loot):
    return loot.profit
    
def bedrock_chest(meter_target,runs:int):
    quality = round(round(int(370*1.05)*TREASURE_BONUS+BOSS_LUCK_BONUS)*TREASURE_BONUS+BOSS_LUCK_BONUS)
    possible_drops = BEDROCK_LOOT.copy()
    drops = [Loot('ESSENCE_WITHER',0,1,10) for i in range(50)] + [Loot('ESSENCE_UNDEAD',0,0,1) for i in range(70)]

    for item in possible_drops:
        if item.id == meter_target:
            meter_target = item
            break
    else:
        meter_target = Loot('placeholder',0,0,0)
    
    meter_target.apply_meter(runs)

    while quality > 0:
        while possible_drops[0].quality > quality: 
            possible_drops.pop(0)
        if len(possible_drops) == 1:  # seperate check for wither essence (weight of 0 breaks random.choices)
            drops.append(possible_drops[0])
            quality -= possible_drops[0].quality 
            continue
        drop = choices(possible_drops,weights=list(map(weight,possible_drops)))[0]
        quality -= drop.quality
        drops.append(drop)
        possible_drops.remove(drop)

    meter_target.reset_weight()

    return drops


print(len(BEDROCK_LOOT),sum(map(weight,BEDROCK_LOOT)))

loot = bedrock_chest('123',0)
print([item for item in loot if 'ESSENCE_' not in item.id])
print(sum(map(profit,loot))/1000000-2)