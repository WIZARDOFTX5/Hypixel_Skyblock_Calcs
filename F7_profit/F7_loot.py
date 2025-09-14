import requests
from random import choices

# CONFIG

sell_offer = False   # sell method for loot, True for sell offer, False for sell instantly

TREASURE_BONUS = 1.03  # 1.03 for Treasure artifact, 1.02 for Ring, 1.01 for Talisman, 1.00 for None

BOSS_LUCK_BONUS = 10  # 10 for Boss Luck 4, 5 for level 3, 3 for level 2, 1 for level 1, 0 for None

# END OF CONFIG










# CONSTANTS

SELL_TYPE = 'buyPrice' if sell_offer else 'sellPrice'

SCORE_BONUS = 1.05  # quality bonus from S+ runs

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
# Also i didnt implement music disc replacing essence drops

class Loot():
    TOTAL_WEIGHT = 13706   # base total weight of f7 bedrock chest. Note that items not from bedrock cannot have rng meter on it
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
        "returns True if item is guaranteed due to rng meter"
        self.weight = self.__base_weight*(1+min(runs*self.__base_weight*2/self.TOTAL_WEIGHT,2))
        if runs*self.__base_weight > self.TOTAL_WEIGHT:
            return True
    def apply_paul(self):  # does not take into account the base cost. remember to account for that in later calculations
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


OBSIDIAN_LOOT = [Loot('WITHER_CHESTPLATE',9000000,1,310),
                Loot('ENCHANTMENT_ULTIMATE_ONE_FOR_ALL_1',1000000,1,290),
                Loot('RECOMBOBULATOR_3000',5000000,2,250),
                Loot('WITHER_LEGGINGS',5000000,4,250),
                Loot('WITHER_CLOAK',3500000,6,230),
                Loot('WITHER_HELMET',3000000,6,210),
                Loot('WITHER_BLOOD',1500000,6,210),
                Loot('ENCHANTMENT_ULTIMATE_SOUL_EATER_1',0,14,180),
                Loot('FUMING_POTATO_BOOK',0,14,175),
                Loot('WITHER_BOOTS',1500000,14,170),
                Loot('WITHER_CATALYST',0,14,160),
                Loot('HOT_POTATO_BOOK',0,10,160),
                Loot('PRECURSOR_GEAR',0,16,140),
                Loot('ENCHANTMENT_ULTIMATE_NO_PAIN_NO_GAIN_1',0,10,120),
                Loot('ENCHANTMENT_ULTIMATE_COMBO_1',0,32,120),
                Loot('ENCHANTMENT_ULTIMATE_BANK_2',0,15,100),
                Loot('ENCHANTMENT_REJUVENATE_2',0,50,100),
                Loot('ENCHANTMENT_ULTIMATE_WISDOM_1',0,15,100),
                Loot('ENCHANTMENT_ULTIMATE_LAST_STAND_1',0,30,100),
                Loot('ENCHANTMENT_ULTIMATE_WISE_1',0,40,100),
                Loot('ENCHANTMENT_ULTIMATE_JERRY_2',0,8,100),
                Loot('ESSENCE_WITHER',0,1,10),
                Loot('ESSENCE_UNDEAD',0,0,1)]


EMERALD_LOOT =  [Loot('WITHER_LEGGINGS',5500000,1,250),
                Loot('WITHER_CLOAK',4000000,1,230),
                Loot('WITHER_HELMET',3500000,2,210),
                Loot('WITHER_BLOOD',2000000,2,210),
                Loot('ENCHANTMENT_ULTIMATE_SOUL_EATER_1',500000,6,180),
                Loot('WITHER_BOOTS',2000000,4,170),
                Loot('ENCHANTMENT_ULTIMATE_NO_PAIN_NO_GAIN_1',0,5,160),
                Loot('WITHER_CATALYST',500000,5,160),
                Loot('HOT_POTATO_BOOK',0,5,160),
                Loot('PRECURSOR_GEAR',0,7,140),
                Loot('ENCHANTMENT_INFINITE_QUIVER_6',0,16,120),
                Loot('ENCHANTMENT_ULTIMATE_COMBO_1',0,16,120),
                Loot('ENCHANTMENT_ULTIMATE_BANK_1',0,10,100),
                Loot('ENCHANTMENT_ULTIMATE_WISDOM_1',0,10,100),
                Loot('ENCHANTMENT_ULTIMATE_LAST_STAND_1',0,10,100),
                Loot('ENCHANTMENT_ULTIMATE_WISE_1',0,20,100),
                Loot('ENCHANTMENT_FEATHER_FALLING_6',0,20,80),
                Loot('ENCHANTMENT_REJUVENATE_2',0,25,80),
                Loot('ENCHANTMENT_ULTIMATE_JERRY_2',0,10,80),
                Loot('ESSENCE_WITHER',0,1,10),
                Loot('ESSENCE_UNDEAD',0,0,1)]


DIAMOND_LOOT =  [Loot('WITHER_HELMET',3750000,1,210),
                Loot('ENCHANTMENT_ULTIMATE_SOUL_EATER_1',750000,2,180),
                Loot('WITHER_BOOTS',2250000,2,170),
                Loot('WITHER_CATALYST',750000,5,160),
                Loot('HOT_POTATO_BOOK',0,5,160),
                Loot('PRECURSOR_GEAR',250000,8,140),
                Loot('ENCHANTMENT_ULTIMATE_NO_PAIN_NO_GAIN_1',0,16,120),
                Loot('ENCHANTMENT_ULTIMATE_COMBO_1',0,16,120),
                Loot('ENCHANTMENT_ULTIMATE_BANK_1',0,15,100),
                Loot('ENCHANTMENT_ULTIMATE_WISDOM_1',0,15,100),
                Loot('ENCHANTMENT_ULTIMATE_WISE_1',0,20,100),
                Loot('ENCHANTMENT_ULTIMATE_JERRY_2',0,1,100),
                Loot('ENCHANTMENT_INFINITE_QUIVER_6',0,20,80),
                Loot('ENCHANTMENT_FEATHER_FALLING_6',0,25,80),
                Loot('ENCHANTMENT_REJUVENATE_1',0,40,80),
                Loot('ESSENCE_WITHER',0,1,10),
                Loot('ESSENCE_UNDEAD',0,1,1)]


GOLD_LOOT = [Loot('WITHER_BOOTS',2400000,2,170),
            Loot('WITHER_CATALYST',900000,5,160),
            Loot('HOT_POTATO_BOOK',0,5,160),
            Loot('PRECURSOR_GEAR',400000,7,140),
            Loot('ENCHANTMENT_ULTIMATE_NO_PAIN_NO_GAIN_1',0,16,120),
            Loot('ENCHANTMENT_ULTIMATE_COMBO_1',0,16,120),
            Loot('ENCHANTMENT_ULTIMATE_BANK_1',0,15,100),
            Loot('ENCHANTMENT_ULTIMATE_WISDOM_1',0,15,100),
            Loot('ENCHANTMENT_ULTIMATE_WISE_1',0,20,100),
            Loot('ENCHANTMENT_ULTIMATE_JERRY_1',0,1,100),
            Loot('ENCHANTMENT_INFINITE_QUIVER_6',0,20,80),
            Loot('ENCHANTMENT_FEATHER_FALLING_6',0,25,80),
            Loot('ENCHANTMENT_REJUVENATE_1',0,40,80),
            Loot('ESSENCE_WITHER',0,1,10),
            Loot('ESSENCE_UNDEAD',0,1,1)]


WOOD_LOOT = [Loot('ENCHANTMENT_ULTIMATE_BANK_1',0,20,100),
            Loot('ENCHANTMENT_ULTIMATE_JERRY_1',0,1,100),
            Loot('ENCHANTMENT_INFINITE_QUIVER_6',0,30,80),
            Loot('ENCHANTMENT_FEATHER_FALLING_6',0,35,80),
            Loot('ENCHANTMENT_REJUVENATE_1',0,30,80),
            Loot('ESSENCE_WITHER',0,1,10),
            Loot('ESSENCE_UNDEAD',0,1,1)]


# chest functions

def weight(loot:Loot):
    return loot.weight

def profit(loot:Loot):
    return loot.profit

class Chest():
    meter_target = 'placeholder'
    runs = 0
    def __init__(self,loot_table:list[Loot],base_quality:int,base_wither_essence:int,base_undead_essence:int):
        self.__quality = round(round(round(base_quality*1.05)*TREASURE_BONUS+BOSS_LUCK_BONUS)*TREASURE_BONUS+BOSS_LUCK_BONUS)
        self.__loot_table = loot_table
        self.__base_wither_essence = base_wither_essence
        self.__base_undead_essence = base_undead_essence
    def roll(self):
        quality = self.__quality
        possible_drops = self.__loot_table.copy()
        drops = [Loot('ESSENCE_WITHER',0,1,10) for i in range(self.__base_wither_essence)] + [Loot('ESSENCE_UNDEAD',0,0,1) for i in range(self.__base_undead_essence)]

        for item in possible_drops:
            if item.id == self.meter_target:
                target = item
                break
        else:
            target = Loot('placeholder',0,0,0)
        
        if target.apply_meter(self.runs):
            quality -= target.quality
            drops.append(target)
            possible_drops.remove(target)

        while quality > 0:
            while possible_drops[0].quality > quality: 
                possible_drops.pop(0)
            if len(possible_drops) == 1:  # seperate check for undead essence (weight of 0 breaks random.choices)
                drops.append(possible_drops[0])
                quality -= possible_drops[0].quality 
                continue
            drop = choices(possible_drops,weights=list(map(weight,possible_drops)))[0]
            quality -= drop.quality
            drops.append(drop)
            if 'ESSENCE_' not in drop.id:
                possible_drops.remove(drop)

        target.reset_weight()

        return drops


bedrock_chest = Chest(BEDROCK_LOOT,370,50,70)  # 2m base cost
obsidian_chest = Chest(OBSIDIAN_LOOT,330,35,55)  # 1m base cost
emerald_chest = Chest(EMERALD_LOOT,260,28,40)  # 500k base cost
diamond_chest = Chest(DIAMOND_LOOT,220,21,30)  # 250k base cost
gold_chest = Chest(GOLD_LOOT,180,18,20)  # 100K base cost
wood_chest = Chest(WOOD_LOOT,125,15,10)  # no base cost

while True:
    loot = bedrock_chest.roll()
    print([item for item in loot if 'ESSENCE_' not in item.id])
    print(sum(map(profit,loot))/1000000-0.250)
    input()