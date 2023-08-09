import math
from constants import tAmb, E, g, rho, cp

def convert_print_to_string(args):
    # loop through args -> convert to string
    try:
        float(args)
        args = str(args)
    except:
        pass

    i = 0
    array = []
    while i < len(args):
        # move to array
        array.append(str(args[i]))
        i += 1

    # # join
    # return string
    return ("").join(array)

def find_centre_coords(coords):
    return [
                (coords[0] + coords[1]) / 2, 
                (coords[2] + coords[3]) / 2, 
                (coords[4] + coords[5]) / 2
                ]
def find_dist(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def Get_Coords_from_FDS_Code(string): ## this returns a list with the coordinates when fed a bit of FDS code 
    string = string.translate({ord(c): None for c in ' XB='}) # strips X, B, = and spaces from string
    string = string.split(",") # splits string into list of strings separated by the comma values
    return [float(f) for f in string if is_number(f)] # co-ordinates extracted as float

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True
    

def compute_q(elapsed_time, growth_rate):
    if elapsed_time == 0:
        return 0
    else:
        return growth_rate * (elapsed_time**2)
    
def compute_qC(q):
    return q * 0.7

def compute_m_entropy(z, g, prev_rho_upper, cP, t_amb, qC):
    return ((E * ((g*(prev_rho_upper**2) / 
        (cP*t_amb))**(1/3))*((qC**(1/3))*(z**(5/3)))) )
    
def compute_rho_upper(t_amb, t_upper):
    return rho * ( t_amb / t_upper )


def computeMUpper(mEntropy, prevMUpper): 
    return mEntropy + prevMUpper


def computeTUpper(tSmoke, prevTUpper, mEntropy, mUpper
    ): 
    if mEntropy == 0 :
        tUpper = prevTUpper
    else:

        tUpper = (((tSmoke - prevTUpper)*mEntropy) / (mEntropy + mUpper)) + prevTUpper
    return tUpper


def computeTSmoke(qC, mEntropy): 
    if qC == 0:
        LHS = 0
    else:
        LHS = qC/(mEntropy*cp)
    
    return LHS + tAmb


def computeZ(prevZ, deltaH):
    return prevZ - deltaH

def computeDeltaH(mEntropy, rhoUpper, area):
    deltaH = mEntropy/(rhoUpper*area)
    # how to change below to python?
    return deltaH if math.isfinite(deltaH) else 0


def computeUpperDepth(deltaH, prevSmokeLayerDepth):
    return deltaH + prevSmokeLayerDepth

# // sprinkler activation functions
def computeU(r, H, q): # u: jet velocity
    u = None
    if (H == 0 or r/H > 0.15): 
        u = 0.195*(q**(1/3))*(H**(1/2))/(r**(5/6))
    else: 
        u = 0.96*((q/H)**(1/3))
    
    return u

def computeDeltaTdetector(u, tUpper, prevTDetector, rTI):
    return ((u**(1/2))*(tUpper - prevTDetector))/rTI

def computeTDetector(prevTDetector, deltaTDetector):
    return prevTDetector + deltaTDetector

# // add time to hashmap; if hashmap not full
def checkIfActivated(tDetector, tActive, activated=False):
    tC = convertKelvinToCelsius(tDetector)
    if (tC >= tActive):
        activated = True
    return activated

def convertKelvinToCelsius(tempK):
    return tempK - 273

def computeHeatReleaseRate(growthRate, t):
    return growthRate*t**2


def computeActivationTime(maxDistance, roomArea, roomHeight, growthRate, rTI=80, tActive=68):
    # // Question: should all values be stored, even after activation?
    activated = False
    tDetector= tAmb 
    currentTDetector = None
    time = 0
    currentTime = None
    deltaTDetector = None
    u = None
    q = None
    qc = None
    tSmoke = None 
    deltaH = None
    tUpper = 273 # why zero, not tAmb??
    z = roomHeight
    rhoUpper = round(rho, 2) # always 1.1
    h = 0 # smoke layer depth
    mUpper = 0#
    mEntropy = 0
    print(tDetector, currentTDetector, time, currentTime)
    while activated  == False:

        activated = checkIfActivated(tDetector, tActive, activated)
        currentTime= time
        currentTDetector = tDetector

        # # functions to get other values below
        # # smoke layer functions
        q = compute_q(time, growthRate) 
        qc = compute_qC(q)
        mUpper = computeMUpper(mEntropy, mUpper)
        mEntropy = compute_m_entropy(z, g, rhoUpper, cp, tAmb, qc)
        tSmoke = computeTSmoke(qc, mEntropy)
        
        tUpper = computeTUpper(tSmoke, tUpper, mEntropy, mUpper
            )
        rhoUpper = compute_rho_upper(tAmb, tUpper)
        
        deltaH = computeDeltaH(mEntropy, rhoUpper, roomArea)

        z = computeZ(z, deltaH)
        # smokeLayerDepth: h
        h = computeUpperDepth(deltaH, h)
        
        # # sprinkler functions
        u = computeU(maxDistance, h, q)
        
        deltaTDetector = computeDeltaTdetector(u, tUpper, tDetector, rTI)
        tDetector = computeTDetector(tDetector, deltaTDetector)

        time += 1

    print("tripped values: ",currentTime, currentTDetector)
    return currentTime

if __name__ == '__main__':
    from constants import growthRateObject
    activation_time = computeActivationTime(maxDistance=2.7, roomArea=10, roomHeight=2.5, growthRate=growthRateObject["medium"], rTI=80, tActive=68)