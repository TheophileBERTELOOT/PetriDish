import numpy as np

SCREEN_SIZE_X = 1000
SCREEN_SIZE_Y = 1000

nbHerbivore = 0
herbivoreInitRadius=20
herbivoreInitHealth=10000
herbivoreBonusHealthWhenEat=10000
herbivoreReproductionThreshold=2
herbivoreHungrinessThreshold=75


nbCarnivore = 0
carnivoreInitRadius=20
carnivoreInitHealth=10000
carnivoreBonusHealthWhenEat=10000
carnivoreReproductionThreshold=3
carnivoreHungrinessThreshold=25

nbFourmiPerColonie = 5
nbFourmiColonie = 2
timeInEggForm = 500
fourmiInitRadius=20
fourmiInitHealth=10000
fourmiBonusHealthWhenEat=10000
fourmiReproductionThreshold=3
fourmiHungrinessThreshold=25
fourmiSenseRadius=150
fourmiNbRay = 10
fourmiAngleOfVision = np.pi*2

positionObstacle = [(100, 100), (200,200)]


grassRadius=10
nbGrass=50
grassZoneEditRadius=50
herbivorePas=1
carnivorePas=1
fourmiPas=1

bodyDecayingThreshold = -1000

nbEntityQlearning = 50