import math
from scipy.special import erfinv

qualteams=55
qualrank=13

draft=1
playwon=3
won=3
place=1

if place==1 or place==2:
    placepts=20
elif place == 3:
    placepts = 13
elif place == 4:
    placepts = 7

awardpts=10

agepts=0

qualpts = erfinv((qualteams-2*qualrank+2)/(1.07*qualteams))*((10)/(erfinv(1/1.07)))+12
DEpts = (playwon/won)*placepts



regional_points = qualpts + (17-draft) + DEpts + awardpts + agepts

print(regional_points)