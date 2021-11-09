import random
import math
import os
import pandas as pd

#Toggle on to view debuging info
is_debug = False

__version__ = '0.6.1'

'''
---- Change Log: ----

Version 0.6.1
 + now uses pandas for monStats
 + updated to work in Python 3

Version 0.6.0  
 + added maxHP and maxMP stats
 * works in Python 2.7

---------------------

Planned features:
 * hero can level up
 * player can fight again without exiting
 * save functionality
'''

def dbg(message):
    print('DEBUG:: ' + message)

print('\n====================================\n')

mStats = pd.read_csv('monStats.csv')

defaultHeroName = 'Graham'

def statDbg():
    dbg("STATS")
    hero.getStats()
    mon.getStats()
    print('END STATS')

class Creature:
    def __init__(self):
        self.hpMax = 1
        self.hp = 1
        self.mpMax = 1
        self.mp = 1
        self.atk = 1
        self.mAtk = 1
        self.dfn = 1
        self.atkVar = 1
        self.atkMin = 1
        self.atkMax = 1
        self.name = ''
    def getStats(self):
        print('{0} stats:'.format(self.name))
        print('hp:  {0}/{1}'.format(self.hp, self.hpMax))
        print('mp:  {0}/{1}'.format(self.mp, self.mpMax))
        print('atk: {0} ~ {1}'.format(self.atkMin, self.atkMax))
        print('mAt: {}'.format(self.mAtk))
        print('dfn: {}'.format(self.dfn))
    def physAttack(self, enemDef):
        print('{} attacked!'.format(self.name))
        damage = random.randint(self.atkMin, self.atkMax) - enemDef
        if damage < 0:
            damage = 0
        return damage
    def healSelf(self):
        print('{} cast Heal!'.format(self.name))
        if self.mp >= 5 and self.hp < self.hpMax:
            regen = int(math.ceil(self.mAtk * 1.2))
            self.hp += regen
            if self.hp >= self.hpMax:
                self.hp = self.hpMax
            self.mp -= 5
            print("{0} recovered {1} hp!".format(self.name, regen))
        else:
            print('The spell failed...')
    def magAttack(self):
        print('{} cast Esper Punch!'.format(self.name))
        if self.mp >= 2:
            self.mp -= 2
            return self.mAtk
        else:
            print('The spell failed...')
            return 0

class Hero(Creature):
    def __init__(self):
        self.hpMax = random.randint(200, 500)
        self.hp = self.hpMax
        self.mpMax = random.randint(3, 7)
        self.mp = self.mpMax
        self.atk = random.randint(30, 100)
        self.mAtk = random.randint(40, 70)
        self.dfn = random.randint(0, 20)
        self.atkVar = random.randint(1, 3) / 10.0
        self.atkMin = round(self.atk * (1 - self.atkVar))
        self.atkMax = round(self.atk * (1 + self.atkVar))
        self.getHeroName()
    def getHeroName(self):
        newName = input("Enter a name for the hero: ")
        if newName == '':
            newName = defaultHeroName
        self.name = newName
        print("The hero, {}, has arrived!\n".format(self.name))
    def getAction(self):
        while True:
            print('1. Attack\n2. Magic Attack (2 mp)\n3. Heal (5 mp)\n4. Defend')
            choice = input("What will you do? ")
            if choice == '1' or choice == '2' or choice == '3' or choice == '4':
                print('')
                return int(choice)
            else:
                print('invalid input!! Please enter a number from the list.')

class Monster(Creature):
    def __init__(self, mID):    #update all instances to take mID instead of mStat
        self.race = mStats['race'][mID]
        self.name = self.nameGen()
        self.hpMax = self.genVstat('hp', 'hpVar', mID)
        self.hp = self.hpMax
        self.mpMax = self.genVstat('mp', 'mpVar', mID)
        self.mp = self.mpMax
        self.atk = mStats['atk'][mID]
        self.mAtk = self.genVstat('mAtk', 'mAtkVar', mID)
        self.dfn = self.genVstat('dfn', 'dfnVar', mID)
        self.atkVar = mStats['atkVar'][mID]
        self.atkMin = round(self.atk * (1 - self.atkVar))
        self.atkMax = round(self.atk * (1 + self.atkVar))
        print('{0} the {1} appears!\n'.format(self.name, self.race))
    def nameGen(self):
        loc = 'monNames' + os.sep + self.race + '.txt'
        nFile = open(loc, 'r')
        size = int(nFile.readline())
        choice = random.randint(1, size)
        for i in range(1, choice):
            nFile.readline()
        name = nFile.readline()
        name = name[:-1]
        nFile.close()
        return name
    def genVstat(self, stat, vStat, mID):
        upper = mStats[stat][mID] + mStats[vStat][mID]
        lower = mStats[stat][mID] - mStats[vStat][mID]
        return random.randint(lower, upper)
    def getAction(self):
        if self.mp < 2:
            if is_debug:
                dbg("{} not enough mp".format(self.name))
            return 0
        elif random.randint(0, 4) > (6 - self.mp):
            if is_debug:
                dbg("{} use magic".format(self.name))
            return 1
        else:
            if is_debug:
                dbg("{} not use magic".format(self.name))
            return 0

def getMonDamage(enemDef, monster):
    action = monster.getAction()
    if action == 0:
        return monster.physAttack(enemDef)
    elif action == 1:
        return monster.magAttack()
    else:
        print('{} tripped!'.format(self.name))

encounter = random.randint(1, 1000)
enemy = ''
if encounter == 1000:
    enemy = 4
elif encounter > 750:
    enemy = 2
elif encounter > 600:
    enemy = 3
else:
    enemy = 1
if is_debug:
    dbg('mStats[enemy] readout:')
    print(mStats[enemy])
hero = Hero()
mon = Monster(enemy)
if is_debug:
    statDbg()

print('====================================\n')

while (hero.hp > 0 and mon.hp > 0):
    print("hp: {}".format(hero.hp))
    print("mp: {}".format(hero.mp))
    if is_debug:
        dbg('mon.hp = {}'.format(mon.hp))
        dbg('mon.mp = {}'.format(mon.mp))
    print('')
    monAtk = 0
    heroAtk = 0
    heroDfn = hero.dfn
    heroAct = hero.getAction()
#hero actions: 1 = physAttack, 2 = magAttack, 3 = heal, 4 = defend
    if heroAct == 1:
        heroAtk = hero.physAttack(mon.dfn)
    elif heroAct == 2:
        heroAtk = hero.magAttack()
    elif heroAct == 3:
        hero.healSelf()
    elif heroAct == 4:
        heroDfn = int(math.floor(hero.dfn * 1.2))
    else:
        print('{} tripped!'.format(hero.name))
    print('{0} dealt {2} damage to {1}!'.format(hero.name, mon.name, heroAtk))
    mon.hp -= heroAtk
    if mon.hp > 0:
        monAtk = getMonDamage(heroDfn, mon)
        print('{0} dealt {2} damage to {1}!'.format(mon.name, hero.name, monAtk))
        hero.hp -= monAtk
    if hero.mp < hero.mpMax:
        hero.mp += 1
    if mon.mp < mon.mpMax:
        mon.mp += 1
    print('\n====================================\n')

if is_debug:
    statDbg()

if hero.hp > 0:
    print('{0} defeated the {1}!!'.format(hero.name, mon.race))
else:
    print('{0} was defeated...'.format(hero.name))
print('\n====================================\n')