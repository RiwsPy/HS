def Default_script(self, *args, **kwargs):
    if self.nb_turn == 1:
        for card in args:
            crd = self.bob.board.create_card_in(card)
            self.buy_minion(crd)
            crd.play()
    elif self.nb_turn == 2:
        self.bob.level_up()

def Random_card_T2(self, *card_key_number):
    if self.nb_turn == 2:
        card = self.hand.create_card_in("117a")
        card.play()
    else:
        if card_key_number:
            for key_number in card_key_number:
                self.force_buy_card(key_number)

def AFK(self, *card_key_number):
    if self.nb_turn <= 2:
        # gèle un token ou un mousse du pont
        pass

def Yogg(self, *card_key_number):
    if self.nb_turn == 1:
        if card_key_number:
            card = self.hand.create_card_in(card_key_number[0])
            card.buff(self.power.enchantment_id)
            card.play()
    elif self.nb_turn == 2:
        self.bob.level_up()

def Xyrella(self, *card_key_number):
    if self.nb_turn == 1:
        if card_key_number:
            card = self.hand.create_card_in(card_key_number[0])
            if card.attack <= 2 and card.health <= 2:
                card.buff(self.power.enchantment_id)
            card.play()
    elif self.nb_turn == 2:
        self.bob.level_up()

def Roi_liche(self, *card_key_number):
    if self.nb_turn == 1:
        if card_key_number:
            card = self.hand.create_card_in(card_key_number[0])
            card.buff(self.power.enchantment_id)
            card.play()
    elif self.nb_turn == 2:
        self.bob.level_up()
        self.board.cards[0].buff(self.power.enchantment_id)

def Millificent(self, *card_key_number):
    if self.nb_turn == 1:
        if card_key_number:
            card = self.bob.board.create_card_in(card_key_number[0])
            self.buy_minion(card)
            card.play()
    elif self.nb_turn == 2:
        self.bob.level_up()

def Y_Shaarj(self, *card_key_number):
    # stat < default hero car utilisation forcée du pouvoir tour1
    if self.nb_turn == 1:
        if card_key_number:
            self.board.create_card_in(card_key_number[0])
            self.hand.create_card_in(card_key_number[0])
    elif self.nb_turn == 2:
        self.board.remove(self.board.cards[0])
        self.bob.level_up()
        self.hand.cards[0].play()

