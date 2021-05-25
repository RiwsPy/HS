import constants
import random

def Default_script(self, *card_key_number):
    if self.bob.nb_turn == 2:
        self.level_up()
    else:
        if card_key_number:
            for key_number in card_key_number:
                self.force_buy_card(key_number)

def Random_card_T2(self, *card_key_number):
    if self.bob.nb_turn == 2:
        card = self.hand.create_card("117a")
        card.play()
    else:
        if card_key_number:
            for key_number in card_key_number:
                self.force_buy_card(key_number)

def AFK(self, *card_key_number):
    if self.bob.nb_turn <= 2:
        # gèle un token ou un mousse du pont
        pass

def Yogg(self, *card_key_number):
    if self.bob.nb_turn == 2:
        self.level_up()
    else:
        bonus = False
        for key_number in card_key_number:
            if not bonus:
                cost = self.minion_cost
                self.minion_cost = 2
            card = self.force_buy_card(key_number)

            if not bonus:
                self.minion_cost = cost
                if card:
                    card.attack += 1
                    card.health += 1
                    bonus = True
