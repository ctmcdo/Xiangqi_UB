pointsPerSide = 9 * 5
numSides = 2
totalPoints = numSides * pointsPerSide

maxUnoccupiedPoints = totalPoints - (numSides)  # 2 generals
maxHorsesChariotsAndCannonsBetweenThe2Sides = (
    numSides * 3 * 2
)  # "" * #{h, ch, c} * numOfEachTypeInBrackets
C = [  # binomial coefficients
    [0] * (maxHorsesChariotsAndCannonsBetweenThe2Sides + 1)
    for i in range(maxUnoccupiedPoints + 1)
]
for n in range(0, maxUnoccupiedPoints + 1):
    C[n][0] = 1
for n in range(1, maxUnoccupiedPoints + 1):
    for k in range(1, maxHorsesChariotsAndCannonsBetweenThe2Sides + 1):
        C[n][k] = C[n - 1][k - 1] + C[n - 1][k]

genAdvEleSameSideSoldierPerms = {}
maxSoldiersPerSide = 5


def sameSideSoldiers(numXiangqiMen, soldierPointsOccupiedByElephants, perms):
    for numSoldiers in range(0, maxSoldiersPerSide + 1):
        soldierPerms = 0
        uninhibitedCols = maxSoldiersPerSide - soldierPointsOccupiedByElephants
        # uninhibitedCols \in [3, 5]
        for inhibitedSoldiers in range(
            max(numSoldiers - uninhibitedCols, 0),  # the min inhibited
            min(numSoldiers + 1, soldierPointsOccupiedByElephants + 1),  # the max
        ):
            uninhibitedSoldiers = numSoldiers - inhibitedSoldiers
            soldierPerms += (
                C[soldierPointsOccupiedByElephants][inhibitedSoldiers]
                * C[uninhibitedCols][uninhibitedSoldiers]
                * pow(2, uninhibitedSoldiers)
            )  # 2 points: 1 adjacent to river and one behind it
        k = (numXiangqiMen + numSoldiers, numSoldiers)
        if k not in genAdvEleSameSideSoldierPerms:
            genAdvEleSameSideSoldierPerms[k] = soldierPerms * perms
        else:
            genAdvEleSameSideSoldierPerms[k] += soldierPerms * perms


def ele(numXiangqiMen, genOn35, perms):
    eleOccupiablePointsPerSide = 2 * 3 + 1  # 3 on each side of palace and 35
    for i in range(2 + 1):
        for j in range(i + 1):
            sameSideSoldiers(
                numXiangqiMen + i,
                j,
                C[2][j]  # elephants can occupy 2 soldier points
                * C[
                    (eleOccupiablePointsPerSide - 2) - genOn35
                ][  #                             ^ same 2 points
                    i - j
                ]
                * perms,
            )


def gen(numXiangqiMen, perms):
    ele(
        numXiangqiMen + 1, False, (3 * 3 - numXiangqiMen - 1) * perms
    )  #                           palace is 3 x 3 grid, in this case less #advisors and 35
    #                                                                       (rank 3, row 5)
    ele(numXiangqiMen + 1, True, perms)


# Compute genAdvEleSameSideSoldierPerms
for i in range(2 + 1):  # advisors
    gen(i, C[5][i])  # 4 corners + 1 centre


# We're interested in the number of ways to place n distinct balls (points / sites) into k
# distinct bins (piece types which include the piece colour) where each bin has a capacity
# of 2 (there are at most 2 horses, chariots and cannons of each colour).
# This is given by an exponential generating function.
# The following can be calculated by a computer algebra system like Wolfram:
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

minUnoccupiedPointsWithOnlyGenAdvEleAndSoldiers = totalPoints - numSides * (
    1 + 2 * 2 + maxSoldiersPerSide
)  # "" * (gen + #{adv, ele} * numOfEachType + "")
horseChariotAndCannonPerms = {}
for numUnoccupiedPoints in range(
    minUnoccupiedPointsWithOnlyGenAdvEleAndSoldiers, maxUnoccupiedPoints + 1
):
    horseChariotAndCannonPerms[numUnoccupiedPoints] = 0
    for balls in range(maxHorsesChariotsAndCannonsBetweenThe2Sides + 1):
        horseChariotAndCannonPerms[numUnoccupiedPoints] += (
            C[numUnoccupiedPoints][balls] * exps[balls]
        )


def sumSides(s0, s1):
    side0_numXiangqiMen = s0[0]
    side1_numXiangqiMen = s1[0]
    numXiangqiMen = s0[0] + s1[0]
    side0_numSameSideSoldiers = s0[1]
    side1_numSameSideSoldiers = s1[1]
    summation = 0
    for crossedSoldiers0 in range(maxSoldiersPerSide - side0_numSameSideSoldiers + 1):
        for crossedSoldiers1 in range(
            maxSoldiersPerSide - side1_numSameSideSoldiers + 1
        ):
            summation += (
                C[pointsPerSide - side1_numXiangqiMen][crossedSoldiers0]
                * C[pointsPerSide - side0_numXiangqiMen][crossedSoldiers1]
                * horseChariotAndCannonPerms[
                    totalPoints - numXiangqiMen - crossedSoldiers0 - crossedSoldiers1
                ]
            )
    return (
        summation
        * genAdvEleSameSideSoldierPerms[s0]
        * genAdvEleSameSideSoldierPerms[s1]
    )


diagram_upperbound = 0
sideKeys = list(genAdvEleSameSideSoldierPerms.keys())
for i in range(len(genAdvEleSameSideSoldierPerms)):
    diagram_upperbound += sumSides(sideKeys[i], sideKeys[i])
    for j in range(i + 1, len(genAdvEleSameSideSoldierPerms)):
        diagram_upperbound += numSides * sumSides(sideKeys[i], sideKeys[j])  # symmetry
print(2 * diagram_upperbound)  # 2 for side-to-move
# 15167534622617873856883343587834774879318
