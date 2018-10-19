#thank god we can use fractions
import fractions

# This is an Absorbing Markov Chain problem.
# 1. All states reach terminal states
# 2. Once in a terminal state, cannot leave.
# Gets a list of the terminal states
def getTransientAndAbsorbing(m):
    t = []
    r = []
    for ind, state in enumerate(m):
        s = sum(state)
        if s == 0:
            r.append(ind)
        else:
            t.append(ind)
    return (t, r)

# Compute the determinant of a square matrix
def determinant(a):
    if len(a) != len(a[0]):
        raise ValueError("Matrix not square!")
    if len(a) == 1:
        return a[0][0]
    if len(a) == 2 and len(a[0]) == 2:
        return a[0][0] * a[1][1] - a[1][0] * a[0][1]
    else:
        multiplierSign = 1
        cumulativeSum = 0
        for multiplierInd in range(len(a)):
            miniMatrix = []
            for x in range(1, len(a)):
                miniRow = []
                for y in range(len(a)):
                    if y != multiplierInd:
                        miniRow.append(a[x][y])
                miniMatrix.append(miniRow)
            cumulativeSum += multiplierSign * a[0][multiplierInd] * determinant(miniMatrix)
            multiplierSign *= -1
        return cumulativeSum

# Transpose a matrix
def transpose(a):
    newMatrix = []
    for x in range(len(a[0])):
        newRow = []
        for y in range(len(a)):
            newRow.append(a[y][x])
        newMatrix.append(newRow)
    return newMatrix

# Compute the adjugate of a square matrix
def adjugate(a):
    if len(a) != len(a[0]):
        raise ValueError("Matrix not square!")
    columnSign = 1
    cofactors = []
    for minorX in range(len(a)):
        cofactorRow = []
        rowSign = columnSign
        for minorY in range(len(a)):
            miniMatrix = []
            for subMatX in range(len(a)):
                if subMatX == minorX:
                    continue
                miniRow = []
                for subMatY in range(len(a)):
                    if subMatY != minorY:
                        miniRow.append(a[subMatX][subMatY])
                miniMatrix.append(miniRow)
            cofactor = rowSign * determinant(miniMatrix)
            cofactorRow.append(cofactor)
            rowSign *= -1
        columnSign *= -1
        cofactors.append(cofactorRow)
    return transpose(cofactors)

# Calculate the inverse of a matrix using determinant and adjoint
# Must be a square matrix
def inverse(a):
    if len(a) != len(a[0]):
        raise ValueError("Matrix not square!")

    # Get adjugate matrix
    adjugateMatrix = adjugate(a)

    # Get the determinant
    det = determinant(a)

    # Denominator limit
    denomLimit = 1 << 31
    
    # Use fractions to get inverse matrix
    fractionMatrix = []
    for x in range(len(a)):
        fractionsRow = []
        for y in range(len(a)):
            fractionsRow.append(fractions.Fraction(adjugateMatrix[x][y], det).limit_denominator(denomLimit))
        fractionMatrix.append(fractionsRow)
    return fractionMatrix
            
# Generate an n by n identity fractions matrix
def identity(n):
    # Denominator limit
    denomLimit = 1 << 31
    i = []
    for x in range(n):
        iRow = []
        for y in range(n):
            if x == y:
                iRow.append(fractions.Fraction(1, 1).limit_denominator(denomLimit))
            else:
                iRow.append(fractions.Fraction(0, 1).limit_denominator(denomLimit))
        i.append(iRow)
    return i

# Generate a probablity matrix from a list of indices a to a list of indices b in the states
# To generate, for example, probabilities of transient states to transient states, you pass in t for a and b
def probabilities(a, b, states):
    # Denominator limit
    denomLimit = 1 << 31
    probs = []
    for x in range(len(a)):
        probsRow = []
        denominator = sum(states[a[x]])
        for y in range(len(b)):
            probsRow.append(fractions.Fraction(states[a[x]][b[y]], denominator).limit_denominator(denomLimit))
        probs.append(probsRow)
    return probs

# Generate N, the fundamental matrix
# This will be calculated as follows:
# N = (I_t - Q)^-1
def n(q):
    if len(q) != len(q[0]):
        raise ValueError("Matrix not square!")
    i = identity(len(q))
    N = []
    for x in range(len(q)):
        NRow = []
        for y in range(len(q)):
            NRow.append(i[x][y] - q[x][y])
        N.append(NRow)
    return inverse(N)

# Dot product of two equal-length vectors
def dot(a, b):
    if len(a) != len(b):
        raise ValueError("Vectors A and B are not the same length!")
    cumulativeSum = 0
    for ind in range(len(a)):
        cumulativeSum += a[ind] * b[ind]
    return cumulativeSum

# Multply matrices A and B
def multiply(a, b):
    b_t = transpose(b)
    finalArr = []
    if len(a[0]) != len(b):
        raise ValueError("Matrices A and B don't have matching axes!")
    for x in a:
        interArr = []
        for y in b_t:
            interArr.append(dot(x, y))
        finalArr.append(interArr)
    return finalArr

# Get a numerator with the forced denominator
def forceLargerDenominator(fraction, denominator):
    if fraction.denominator == denominator:
        return fraction.numerator
    m = denominator % fraction.denominator
    if m == 0:
        return fraction.numerator * (denominator // fraction.denominator)
    else:
        raise ValueError("Do not divide properly. Check your denominator.")

# Get the least common multiple of an array of numbers
def lcm(a):
    LCM = 1
    for n in a:
        LCM *= n // fractions.gcd(LCM, n)
    return LCM
        

# B = NR, where N is the fundamental matrix, and R is the matrix of probabilities from
# transient states to absorbing states
def answer(m):
    # Check for weird 1-state systems
    if len(m) == 1:
        return [1, 1]
    transientIndices, absorbingIndices = getTransientAndAbsorbing(m)
    Q = probabilities(transientIndices, transientIndices, m)
    N = n(Q)
    R = probabilities(transientIndices, absorbingIndices, m)
    B = multiply(N, R)
    # B[0] should indicate the probabilies to each absorbing state
    # Thus, we now have to noramlize all the fractions
    probsList = []
    for x in range(len(B)):
        denominator = lcm([fraction.denominator for fraction in B[x]])
        probs = []
        for fraction in B[x]:
            probs.append(forceLargerDenominator(fraction, denominator))
        probs.append(denominator)
        probsList.append(probs)
    return probsList

a = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [1,4,0,0,1,0,1,0,1,0],
    [3,0,2,0,0,0,0,0,1,1],
    [4,1,1,0,0,0,0,2,0,1],
    [7,4,0,0,2,0,3,1,0,0],
    [1,2,2,0,1,0,0,3,2,0],
    [3,2,1,0,0,0,1,0,7,0],
    [1,3,0,0,0,7,0,1,0,4],
    [2,7,0,0,1,0,2,0,1,0]
]
ans = answer(a)
print(ans)
prob = 1
byte = ""
for p in ans:
    if p[0] > p[1]:
        byte = "0" + byte
        prob *= p[0] / p[2]
    else:
        byte = "1" + byte
        prob *= p[1] / p[2]
print("byte: {:02x}".format(int(byte, 2)))
print(prob)