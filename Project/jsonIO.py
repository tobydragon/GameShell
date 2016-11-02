import json

def saveToJson(fileName,object):
    if type(object) is dict:
        JSONdata=object
    else:
        try:
            JSONdata=object.toJSON()
        except AttributeError as e:
            print("object does not have toJSON() method (object type %s"%str(type(object)))
            return False
    f = open(fileName,'w')
    json.dump(JSONdata, f,indent="\t")
    f.close()
    return True

def loadFromJson(fileName):
    try:
        f=open(fileName)
    except FileNotFoundError as e:
        print(e)
        return None
    JSONdata=json.load(f)
    f.close()
    return JSONdata