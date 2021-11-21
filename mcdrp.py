import os
import json
import shutil

def clear():
    os.system("cls" if os.name in ("nt", "dos") else "clear")

if __name__=="__main__":
    print("detected versions: ", end="")
    try:
        asset_versions = os.listdir(os.getenv("APPDATA")+"/.minecraft/assets/indexes")
    except OSError:
        print("OSError! something went really wrong!")
        exit() # bail out

    if len(asset_versions) == 0:
        print("none!")
        print("cannot find anything in '.minecraft/assets/indexes'!")
        exit() # nothing available to handle this yet
    
    # get user input on desired version
    select_valid = False
    while select_valid == False:
        [print(v[:-5], end=" ") for v in asset_versions]
        selected_version = input("\nSelect version: ")
        if asset_versions.index(selected_version+".json"): select_valid = True
        else: clear()

    asset_index = open(os.getenv("APPDATA")+"/.minecraft/assets/indexes/"+selected_version+".json").read()
    asset_index_json = json.loads(asset_index)

    pack_root = "Default_"+selected_version+"/"
    asset_objects = os.getenv("APPDATA")+"/.minecraft/assets/objects/"
    
    for object in asset_index_json["objects"]:
        object_hash = asset_index_json["objects"][object]["hash"]
        print(object_hash+" -> "+pack_root+object)
        try:
            shutil.copyfile(asset_objects+"/"+object_hash[:2]+"/"+object_hash, pack_root+object)
        except FileNotFoundError:
            os.makedirs(os.path.dirname(pack_root+object), exist_ok=True)
            shutil.copyfile(asset_objects+"/"+object_hash[:2]+"/"+object_hash, pack_root+object)
    
    print("done.")