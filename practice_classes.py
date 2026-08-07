# Реализовать два вида существ в игре со своими перками:
#
# Орки base_health_points = 100, base_attack_power = 10, base_defence = 10
# Перк: орки увеличивают защиту в три раза, если у них меньше 50 хп.

# Эльфы, base_health_points = 50, base_attack_power = 15, base_defence = 10
# Перк: эльфы бьют по существам у которых меньше 30% хп, в два раза сильнее.
#


class Character:
    def __init__(self,*,health_points,attack_power,defence)-> None:
        self.health_points = health_points
        self.attack_power = attack_power
        self.defence = defence
    def __str__(self) -> str:
        return f"{self.character_name} (hp: {self.health_points}, attack: {self.attack_power}, defence: {self.defence})"
    
    def attack(self):
        print(f"{self.character_name} attacks with {self.attack_power} power")
    def get_defence(self):
        return self.defence


class Ork(Character):
    character_name = "Ork"

    def __init__(self):
        super().__init__(health_points=100, attack_power=10, defence=10)

    def get_defence(self):
        if self.health_points < 50:
            print("Перк Орка: защита утроена!")
            return self.defence * 3  
        return self.defence




class Elf(Character):
    character_name = "Elf"

    def __init__(self):
        super().__init__(health_points=50,attack_power=15,defence=10)

    def attack(self, target):
        damage = self.attack_power

        if target.health_points < 30:
            damage *=2
            print("Перк Эльфа: Урон удвоен")

        real_damage = max(0,damage - target.get_defence())
        target.health_points -= real_damage

        print(f"{self.character_name} атаковал {target.character_name} на {real_damage} урона!")


ork = Ork()
elf = Elf()

print(ork)
print(elf)


ork.health_points = 40

print("\n--- Эльф атакует Орка с перком ---")
elf.attack(ork)

