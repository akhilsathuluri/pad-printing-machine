import cv2

def check_model(register_model):
    identified_model = 3
    if identified_model == register_model:
        return True, identified_model
    elif identified_model != register_model:
        return False, identified_model
    else:
        return 'ERROR', 0

def check_orientation():
    # Fill code with thresholding blob analysis
    check = True
    return check
