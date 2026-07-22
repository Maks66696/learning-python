import json

player={
    "nickname":123,
    "score":67,
    "is_online":True
}

with open("player.json", "w") as file:
    json.dump(player, file, indent=4)

with open("player.json", "r") as file:
    saved_player = json.load(file)


print(saved_player)