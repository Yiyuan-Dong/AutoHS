class Minion:
    def __init__(self, attack, health, is_taunt, is_divine_shield):
        self.attack = attack
        self.health = health
        self.is_taunt = is_taunt
        self.has_divine_shield = is_divine_shield

    def __str__(self):
        temp = str(self.attack) + "-" + str(self.health)
        if self.is_taunt:
            temp += " 嘲讽"
        if self.has_divine_shield:
            temp += " 圣盾"
        return temp

    def delta_h_after_damage(self, damage):
        if self.has_divine_shield:
            if damage == 0:
                return 0
            return self.attack
        else:
            if damage >= self.health:
                return self.attack + self.health
            else:
                return damage

    def get_damaged(self, damage):
        if self.has_divine_shield:
            if damage > 0:
                self.has_divine_shield = False
        else:
            self.health -= damage
            if self.health <= 0:
                return True
        return False
