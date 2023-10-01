def water_quality(ph,iron,no3,chloride,pb,zn,turbidity,f,cu,so4,chlorine,mn,solids):
    flags = {
        'ph':0,
        'iron':0,
        'nitrate':0,
        'chloride':0,
        'lead':0,
        'zinc':0,
        'turbidity':0,
        'fluoride':0,
        'copper':0,
        'sulfate':0,
        'chlorine':0,
        'manganese':0,
        'solids':0,
    }

    if (ph < 6.5):
        flags['ph'] = -1
    elif (ph > 8.5):
        flags['ph'] = 1
    
    if (iron > .3):
        flags['iron'] = 1

    if (no3 > 45):
        flags['nitrate'] = 1
    
    if (chloride > 250):
        flags['chloride'] = 1
    
    if (pb > .1):
        flags['lead'] = 1
    
    if (zn > 5.0):
        flags['zinc'] = 1

    if (turbidity > 10):
        flags['turbidity'] = 1
    
    if (f < .6):
        flags['fluoride'] = -1
    elif (f > 1.2):
        flags['fluoride'] = 1
    
    if (cu > .05):
        flags['copper'] = 1
    
    if (so4 > 250):
        flags['sulfate'] = 1

    if (chlorine > .2):
        flags['chlorine'] = 1
    
    if (mn > .1):
        flags['manganese'] = 1
    
    if (solids > 1250):
        flags['solids'] = 1

    return flags