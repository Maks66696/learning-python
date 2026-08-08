class Character:
    def __init__(self, *, level: int) -> None:
        self.level = level
        self.health_points = self.base_health_points * level
        self.attack_power = self.base_attack_power * level

    def __str__(self) -> str:
        return f"{self.character_name} (level: {self.level}, hp: {self.health_points})"

    def attack(self, *, target: "Character") -> None:
        print(
            f"{self.character_name} attacks {target.character_name} ({target.health_points} health_points) "
            f"with {self.attack_power} power."
        )
        target.health_points -= self.attack_power
        print(f"After attack {target.character_name} hp has {target.health_points}")

    def is_alive(self) -> bool:
        return self.health_points > 0


class Ork(Character):
    character_name = "Ork"
    base_health_points = 100
    base_attack_power = 10


class Elf(Character):
    character_name = "Elf"
    base_health_points = 70
    base_attack_power = 15


def fight(*, character_1: Character, character_2: Character) -> None:
    while character_1.is_alive() and character_2.is_alive():
        character_1.attack(target=character_2)
        if character_2.is_alive():
            character_2.attack(target=character_1)

    if character_1.is_alive():
        winner = character_1

    else:
        winner = character_2


    if winner.level < 3:
        winner.level +=1
        winner.health_points += int(winner.base_health_points /2)


ork = Ork(level=1)
elf = Elf(level=1)
fight(character_1=ork, character_2=elf)

for char in [ork, elf]:
    if char.is_alive():
        print(f"{char.character_name} is alive {char}")
    else:
        print(f"{char.character_name} is dead {char}")

