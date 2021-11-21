# minecraft-default-resource-puller

This script is intended to pull the default assets of a Minecraft installation and arrange them into a resource-pack that can be loaded and modified.

Here, it is assumed that you own the game and have installed it at least once, and that you are using this to pull the default resources of **at least** 1.6.1, since that is the version that introduced resource packs. Any version of the game earlier than that will **not work** and **crash the script**.


First, you get to pick the version to pick various objects (mostly sound files) from. This will have you pick from the `.minecraft/assets/indexes` folder. Each object map covers multiple versions unless noted otherwise.

Second, you get to pick the specific version of the game to take everything else (such as textures) from. This will have you pick from the `.minecraft/versions` folder.