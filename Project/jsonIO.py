import json

__author__ = "BenjaminWelsh"

def saveToJson(fileName,object):
    """
    Saves an object's jason data to a file by calling toJSON
    :param fileName: file name to save to
    :param object: object to save
    :return: Returns False if object does not have method toJSON(). Otherwise returns True.
    """
    if type(object) is dict:
        JSONdata=object
    else:
        try:
            JSONdata=object.toJSON()
        except AttributeError as e:
            print("object does not have toJSON() method (object type %s"%str(type(object)))
            return False
    with open(fileName,'w') as f:
        json.dump(JSONdata, f,indent="\t")
    return True

def loadFromJson(fileName):
    """
    Loads a json file
    :param fileName: file to load
    :return: None if file not found, otherwise the data object.
    """
    try:
        f=open(fileName)
    except FileNotFoundError as e:
        print(e)
        return None
    JSONdata=json.load(f)
    f.close()
    return JSONdata