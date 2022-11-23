import os
import json
import shutil
import zipfile

dotmc = os.getenv("APPDATA")+"/.minecraft"

asset_folder = os.listdir(dotmc+"assets/")
asset_indexes = os.listdir(asset_folder+"indexes/")
asset_objects = os.listdir(asset_folder+"objects/")
asset_jars = os.listdir(dotmc+"versions/")
selected_asset_index = None
selected_asset_jar = None
pack_rootname = "McDefaultResources/" # change this to whatever if you want

def clear():
    os.system("cls" if os.name in ("nt", "dos") else "clear")

def change_asset_folder(new_path):
    global asset_folder, asset_indexes, asset_objects
    if new_path == None:
        # set to default
        asset_folder = os.listdir(dotmc+"assets/")
        return
    if os.path.exists(new_path+"indexes/") and os.path.exists(new_path+"objects/"):
        # set only if we have indexes and objects!
        # update the indexes and objects path too while were at it
        asset_folder = os.listdir(new_path)
        asset_indexes = os.listdir(asset_folder+"indexes/")
        asset_objects = os.listdir(asset_folder+"objects/")
        return
    change_asset_folder(None)
    return

def change_asset_jars(new_path):
    global asset_jars
    if new_path == None:
        asset_jars = os.listdir(dotmc+"versions/")
        return
    # theres no extra checks really to do here
    asset_jars = os.listdir(new_path)
    return

def select_asset_index():
    global asset_indexes, selected_asset_index
    print("\n\n")
    [print(v[:-5]) for v in asset_indexes]
    print("\n")
    selected_asset_index = asset_indexes+input("Select asset index: ")
    if os.path.isfile(selected_asset_index+".json") == False:
        selected_asset_index = None
    return

def select_asset_jar():
    global asset_jars, selected_asset_jar
    print("\n\n")
    [print(v) for v in asset_jars]
    print("\n")
    _selected_asset_jar_folder = os.listdir(input("Select version: "))
    _selected_asset_jar_folder_jar = None
    [_selected_asset_jar_folder.remove(j) for j in _selected_asset_jar_folder if j[len(j)-4:] != ".jar"]
    if len(_selected_asset_jar_folder) > 1:
        print("\n\n")
        [print(j[:-4]) for j in _selected_asset_jar_folder]
        print("\n")
        _selected_asset_jar_folder_jar = _selected_asset_jar_folder+input("Select jar file: ")
        if os.path.isfile(_selected_asset_jar_folder_jar) == False:
            _selected_asset_jar_folder_jar = None
    else:
        _selected_asset_jar_folder_jar = _selected_asset_jar_folder[0]
    selected_asset_jar = _selected_asset_jar_folder_jar

def extract_asset_objects():
    global selected_asset_index, asset_objects
    _index = json.loads(open(select_asset_index).read())
    print("attempting to copy hashed objects now...")
    for obj in _index["objects"]:
        obj_hash = obj["hash"]
        print(obj_hash+" -> "+pack_rootname+"assets/"+obj)
        try:
            shutil.copyfile(asset_objects+"/"+obj_hash[:2]+"/"+obj_hash, pack_rootname+"assets/"+obj)
        except:
            os.makedirs(os.path.dirname(pack_rootname+"assets/"+obj), exist_ok=True)
            shutil.copyfile(asset_objects+"/"+obj_hash[:2]+"/"+obj_hash, pack_rootname+"assets/"+obj)
    print("hashed objects copied.")
    return



if __name__=="__main__":
    
    print("attempting to pull jar assets now...")
    target_jar = dotmc+"/versions/"+selected_jar+"/"+selected_jar+".jar"
    jar = zipfile.ZipFile(target_jar, 'r', allowZip64=True)
    for file in jar.namelist():
        if file.startswith("assets/"):
            jar.extract(file, pack_root_2)
    
    print("cleaning up...")
    os.remove(pack_root_2+"assets/.mcassetsroot")
    shutil.move(pack_root_2+"/assets/pack.mcmeta", pack_root_2)

    print("done.")