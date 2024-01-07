pointsPerSide = 9 * 5
numSides = 2
totalPoints = numSides * pointsPerSide

binomN = totalPoints - (numSides)  # 2 generals
maxHorsesChariotsAndCannonsOverBothSides = (
    numSides * 3 * 2
)  # "" * #{h, ch, c} * numOfEachType
binoms = [
    [0] * (maxHorsesChariotsAndCannonsOverBothSides + 1) for i in range(binomN + 1)
]
for n in range(0, binomN + 1):
    binoms[n][0] = 1
for n in range(1, binomN + 1):
    for k in range(1, maxHorsesChariotsAndCannonsOverBothSides + 1):
        binoms[n][k] = binoms[n - 1][k - 1] + binoms[n - 1][k]

summaries = {}
maxSoldiersPerSide = 5


def sameSideSoldiers(numXiangqiMen, soldierPointsOccupiedByEles, perms):
    for numSoldiers in range(0, maxSoldiersPerSide + 1):
        soldierPerms = 0
        uninhibCols = (
            maxSoldiersPerSide - soldierPointsOccupiedByEles
        )  # uninhibCols \in [3, 5]
        for squeezedSoldiers in range(
            max(numSoldiers - uninhibCols, 0),
            min(soldierPointsOccupiedByEles + 1, numSoldiers + 1),
        ):
            uninhibSoldiers = numSoldiers - squeezedSoldiers
            soldierPerms += (
                binoms[soldierPointsOccupiedByEles][squeezedSoldiers]
                * binoms[uninhibCols][uninhibSoldiers]
                * pow(2, uninhibSoldiers)
            )  # 2 for the point before crossing river and the one behind it
        k = (numXiangqiMen + 1 + numSoldiers, numSoldiers)  # 1 for this side's gen
        if k not in summaries:
            summaries[k] = soldierPerms * perms
        else:
            summaries[k] += soldierPerms * perms


def ele(numXiangqiMen, genOn3_5, perms):
    eleOccupiablePointsPerSide = 2 * 3 + 1  # 3 on each side of palace and 3_5
    # 0 ele
    sameSideSoldiers(numXiangqiMen, 0, perms)
    # 1 ele
    sameSideSoldiers(
        numXiangqiMen + 1, 0, ((eleOccupiablePointsPerSide - 2) - genOn3_5) * perms
    )  # elephants can occupy 2 soldier points
    sameSideSoldiers(numXiangqiMen + 1, 1, 2 * perms)
    # 2 ele
    sameSideSoldiers(
        numXiangqiMen + 2,
        0,
        binoms[(eleOccupiablePointsPerSide - 2) - genOn3_5][2] * perms,
    )
    sameSideSoldiers(
        numXiangqiMen + 2,
        1,
        2 * binoms[(eleOccupiablePointsPerSide - 2) - genOn3_5][1] * perms,
    )
    sameSideSoldiers(numXiangqiMen + 2, 2, perms)


def adv(genOnCornerOrCentre, genOn3_5, perms):
    for i in range(2 + 1):
        ele(i, genOn3_5, binoms[5 - genOnCornerOrCentre][i] * perms)


# Fill side summaries
adv(False, False, 3)  # 9 - 5 - 1 = 3
adv(False, True, 1)  # 3_5
adv(True, False, 5)  # 4 corners + 1 centre

# n distinct balls (points) into k distinct bins (piece type & colour) where
# each bin has capacity 2 (there are at most 2 horses, chariots and cannons of each colour).
# n! Coefficient[(1 + x + x^2/2)^k, x^n] for k = 6, 0 <= n <= 12
exps = [
    1,
    6,
    36,
    210,
    1170,
    6120,
    29520,
    128520,
    491400,
    1587600,
    4082400,
    7484400,
    7484400,
]

minFreePoints = totalPoints - numSides * (
    1 + 2 * 2 + maxSoldiersPerSide
)  # "" * (gen + #{adv, ele} * numOfEachType + "")
horseChariotAndCannonPerms = {}
for remPoints in range(minFreePoints, binomN + 1):
    horseChariotAndCannonPerms[remPoints] = 0
    for j in range(maxHorsesChariotsAndCannonsOverBothSides + 1):
        horseChariotAndCannonPerms[remPoints] += binoms[remPoints][j] * exps[j]


def countSideCombo(s0, s1):
    summation = 0
    for freeSoldiers0 in range(maxSoldiersPerSide - s0[1] + 1):  # rem soldiers
        for freeSoldiers1 in range(maxSoldiersPerSide - s1[1] + 1):
            summation += (
                binoms[pointsPerSide - s1[0]][freeSoldiers0]
                * binoms[pointsPerSide - s0[0]][freeSoldiers1]
                * horseChariotAndCannonPerms[
                    totalPoints - s0[0] - s1[0] - freeSoldiers0 - freeSoldiers1
                ]
            )
    return summation * summaries[s0] * summaries[s1]


upperbound = 0
summaryKeys = list(summaries.keys())
for i in range(len(summaries)):
    upperbound += countSideCombo(summaryKeys[i], summaryKeys[i])  # sideToMove
    for j in range(i + 1, len(summaries)):
        upperbound += numSides * countSideCombo(
            summaryKeys[i], summaryKeys[j]
        )  # symmetry
print(upperbound)  # diagrams
# 7583767311308936928441671793917387439659
print(upperbound * 2)  # sideToMove -> positions
# 15167534622617873856883343587834774879318
