import os
import json

assets_versions = []

if __name__=="__main__":
    assets_versions = os.listdir(os.getenv("APPDATA")+"/.minecraft/assets/indexes")
    print("detected versions: ", end="")
    for v in assets_versions: print(v[:len(v)-5], end=", ") # chop off the .json for display
