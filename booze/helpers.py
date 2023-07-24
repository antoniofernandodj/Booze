def check_numeric(value):
    test = []
    try:
        float(value)
        test.append(True)
    except:
        test.append(False)
        
    try:
        int(value)
        test.append(True)
    except:
        test.append(False)
        
    return any(test)
