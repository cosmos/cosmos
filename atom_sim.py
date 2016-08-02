print "Compute atoms for validators and delegators over time"
import math

atomsVal = 0.000    # starting atoms for validator
atomsDel = 0.010    # starting atoms delegated to validator
atomsAll = 1.0      #
inflation = 0.3     # 30% inflation
inflationLg = math.log(1.0 + inflation) # for exponential
exponential = True  # exponential
commission = 0.10   # 5% commission
numBlocksPerYear = 1000

for year in range(0,50):
  rewardsYear = 0.0
  for i in range(0,numBlocksPerYear):
    if exponential:
      blockReward = (atomsAll * inflationLg) / float(numBlocksPerYear)
    else:
      blockReward = inflation / float(numBlocksPerYear)

    atomsAll += blockReward
    rewardsYear += blockReward
    rewardVal = blockReward * (atomsVal / atomsAll)
    rewardDel = blockReward * (atomsDel / atomsAll)
    rewardVal += rewardDel * commission
    rewardDel *= (1.0 - commission)
    atomsVal += rewardVal
    atomsDel += rewardDel
    #print atomsVal, atomsDel, (atomsVal / atomsAll)
  print year, "atomsVal: %0.3f" % (atomsVal,), "atomsDel: %0.3f" % (atomsDel,), \
  "atomsAll: %0.3f" % (atomsAll,), "atomsVal%%: %0.2f" % ((100 * atomsVal / atomsAll),), \
  "atomsDel%%: %0.2f" % ((100 * atomsDel / atomsAll),), "rewards: %0.2f"%(rewardsYear,), \
  "valDelRatio: %0.3f" % (atomsVal / (atomsDel + atomsVal))
