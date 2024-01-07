totalPoints = 9 * 10
binomN = totalPoints - 2 # 2 generals
maxHorsesChariotsAndCannonsOverBothSides = 2 * 3 * 2 # numSides * (h | ch | c) * numOfEachType
binoms = [[0] * (maxHorsesChariotsAndCannonsOverBothSides + 1)] * (binomN + 1)
for n in range(0, binomN + 1):
    binoms[n][0] = 1
for n in range(1, binomN + 1):
    for k in range(1, maxHorsesChariotsAndCannonsOverBothSides + 1):
        binoms[n][k] = binoms[n-1][k-1] + binoms[n-1][k]

summaries = {}
def sameSideSoldiers(numXiangqiMen, soldierPointsOccupied, perms):
    for numSoldiers in range(0, 5 + 1):
        soldierPerms = 0
        freeCols = 5 - soldierPointsOccupied
        for squeezedSoldiers in range(max(numSoldiers - freeCols, 0),
                soldierPointsOccupied + 1):
            soldierPerms += binoms[soldierPointsOccupied][squeezedSoldiers] \
                    + 2 * binoms[freeCols][numSoldiers - squeezedSoldiers]
        k = (numXiangqiMen + numSoldiers, numSoldiers)
        if k not in summaries:
            summaries[k] = soldierPerms * perms
        else:
            summaries[k] += soldierPerms * perms

def ele(numXiangqiMen, genOn3_5, perms):
    sameSideSoldiers(numXiangqiMen, 0, perms)
    sameSideSoldiers(numXiangqiMen + 1, 0, (5 - genOn3_5) * perms)
    sameSideSoldiers(numXiangqiMen + 1, 1, 2 * perms)
    sameSideSoldiers(numXiangqiMen + 2, 0, binoms[5 - genOn3_5][2] * perms)
    sameSideSoldiers(numXiangqiMen + 2, 1, 2 * (5 - genOn3_5) * perms)
    sameSideSoldiers(numXiangqiMen + 2, 2, perms)

def adv(genOnCornerOrCentre, genOn3_5, perms):
    ele(genOn3_5, 0, perms)
    ele(genOn3_5, 1, (5 - genOnCornerOrCentre) * perms)
    ele(genOn3_5, 2, binoms[5 - genOnCornerOrCentre][2] * perms)

# Fill summaries
adv(0, 1, 1)
adv(1, 0, 5)
adv(0, 0, 4)

# n! Coefficient[(1 + x + x^2/2)^k, x^n] for k = 6, 0 <= n <= 12
# k = 6 for h, ch, c, H, CH, C, or maxHorsesChariotsAndCannonsOverBothSides // 2
exps = [1, 6, 36, 210, 1170, 6120, 29520, 128520, 491400, 1587600, 4082400, 7484400, 7484400]

minFreePoints = totalPoints - 2 * (1 + 2 * 2 + 5) # numSides * (gen + 2 * (adv or ele) + maxSoldiers)
horseChariotAndCannonPerms = {}
for remPoints in range(minFreePoints, binomN + 1):
    horseChariotAndCannonPerms[remPoints] = 0
    for j in range(maxHorsesChariotsAndCannonsOverBothSides + 1):
        horseChariotAndCannonPerms[remPoints] += binoms[remPoints][j] * exps[j]

def countSideCombo(k0, k1):
    halfb = totalPoints // 2
    summation = 0
    for i in range(5 - k0[1]): # rem soldiers
        for j in range(5 - k1[1]):
            summation += binoms[halfb - (k1[0] + 1)][i] * binoms[halfb - (k0[0] + 1)][j] * \
                    horseChariotAndCannonPerms[totalPoints - k0[0] - k1[0] - 2 - i - j]
    return summation

upperbound = 0
summaryKeys = list(summaries.keys())
for i in range(len(summaries)):
    upperbound += countSideCombo(summaryKeys[i], summaryKeys[i])
    for j in range(i + 1, len(summaries)):
        upperbound += 2 * countSideCombo(summaryKeys[i], summaryKeys[j])
print(upperbound)
