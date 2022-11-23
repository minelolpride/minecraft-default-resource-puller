import os
import sys
import json
import shutil
import zipfile

assert(sys.version_info >= (3, 10), "this script requires at least python 3.10!\nyou are on "+str(sys.version_info.major)+"."+str(sys.version_info.minor)+".")

dotmc = os.getenv("APPDATA")+"/.minecraft/"

asset_folder = dotmc+"assets/"
asset_indexes = asset_folder+"indexes/"
asset_objects = asset_folder+"objects/"
asset_jars = dotmc+"versions/"
selected_asset_index = None
selected_asset_jar = None
pack_rootname = "McDefaultResources/" # change this to whatever if you want

def clear():
    os.system("cls" if os.name in ("nt", "dos") else "clear")

def change_pack_name(new_name):
    global pack_rootname
    if len(new_name) == 0:
        pack_rootname = "McDefaultResources/"
        return
    if new_name[-1:] != "/":
        new_name = new_name+"/"
    pack_rootname = new_name
    return

def change_asset_folder(new_path):
    global asset_folder, asset_indexes, asset_objects
    if len(new_path) == 0:
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
    change_asset_folder("")
    return

def change_asset_jars(new_path):
    global asset_jars
    if len(new_path) == 0:
        asset_jars = os.listdir(dotmc+"versions/")
        return
    # theres no extra checks really to do here
    asset_jars = os.listdir(new_path)
    return

def select_asset_index():
    global asset_indexes, selected_asset_index
    print("\n\n")
    [print(v[:-5]) for v in os.listdir(asset_indexes)]
    print("\n")
    selected_asset_index = asset_indexes+input("Select asset index: ")
    if os.path.isfile(selected_asset_index+".json") == False:
        selected_asset_index = None
    return

def select_asset_jar():
    global asset_jars, selected_asset_jar
    print("\n\n")
    [print(v) for v in os.listdir(asset_jars)]
    print("\n")
    _selected_asset_jar_folder = os.listdir(input("Select version: "))
    _selected_asset_jar_folder_jar = None
    [_selected_asset_jar_folder.remove(j) for j in _selected_asset_jar_folder if j[-4:] != ".jar"]
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
    global selected_asset_index, asset_objects, pack_rootname
    if selected_asset_index == None:
        print("you have no hashed object index selected!")
        return
    print("attempting to copy hashed objects now...")
    _index = json.loads(open(select_asset_index).read())
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

def extract_jar_assets():
    global selected_asset_jar, pack_rootname
    if selected_asset_jar == None:
        print("you have no jar selected!")
        return
    print("attempting to extract jar assets now...")
    _jar = zipfile.ZipFile(selected_asset_jar, 'r', allowZip64=True)
    for file in _jar.namelist():
        if file.startswith("assets/"):
            _jar.extract(file, pack_rootname)
    print("jar assets extracted.")
    return

def finalize_pack():
    global pack_rootname
    print("finalizing pack...")
    try:
        os.remove(pack_rootname+"assets/.mcassetsroot")
        shutil.move(pack_rootname+"assets/pack.meta", pack_rootname)
    except:
        pass
    return

if __name__=="__main__":
    while True:
        clear()
        print("\n Pack Name: "+pack_rootname[:-1])
        print(" Assets: "+asset_folder+"\n Selected Index: "+str(selected_asset_index))
        print(" Jars: "+asset_jars+"\n Selected Jar: "+str(selected_asset_jar))
        print("\n [1] Change pack name\n [2] Change assets folder\n [3] Change jars folder")
        print(" [4] Select hashed object index\n [5] Select jar file")
        print(" [6] Extract hashed assets\n [7] Extract jar assets\n [8] Cleanup pack")
        print(" [0] Exit")

        match input(" :: "):
            case "0": exit()
            case "1": change_pack_name(input(" New pack name: "))
            case "2": change_asset_folder(input(" New assets folder path: "))
            case "3": change_asset_jars(input(" New asset jars path: "))
            case "4": select_asset_index()
            case "5": select_asset_jar()
            case "6": extract_asset_objects()
            case "7": extract_jar_assets()
            case "8": finalize_pack()