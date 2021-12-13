
class Default_script:
    def turn_1(self, *args, force=False, **kwargs):
        for card in args:
            crd = self.game.hand.remove_and_create(card)
            self.bob.board.append(crd)
            #crd = self.bob.board.create_card_in(card)
            if force:
                crd.buy(cost=0)
            else:
                crd.buy()
        self.hand.auto_play()

    def turn_2(self, *args, **kwargs):
        self.levelup()

    def turn_3(self, *args, force=False, **kwargs):
        self.board.cards.sort(key=lambda x: x.dbfId.rating, reverse=True)
        if args and type(args[0]) is str:
            args = [self.all_cards[arg]
            for arg in args]
        else:
            args = list(args)
        args.sort(key=lambda x: x.rating, reverse=True)

        for card in args:
            if self.gold >= self.minion_cost:
                crd = self.bob.board.create_card_in(card)
                crd.buy()
            elif force:
                crd = self.bob.board.create_card_in(card)
                crd.buy(cost=0)
            elif self.gold == self.minion_cost -1 and self.board.cards:
                if card.rating > self.board.cards[-1].dbfId.rating:
                    self.board.cards[-1].sell()
                    crd = self.bob.board.create_card_in(card)
                    crd.buy()
        self.hand.auto_play()

class Special_arene_base_T2_to_T3:
    def turn_1(self, card):
        crd = self.game.hand.remove_and_create(card)
        self.bob.board.append(crd)
        crd.buy(cost=0)
        crd.play()

    def turn_2(self, *args, **kwargs):
        self.levelup()

    def turn_3(self, card_1, card_2, force=False, diff_esp=0):
        if card_1.rating < card_2.rating:
            card_1, card_2 = card_2, card_1

        crd = self.game.hand.remove_and_create(card_1)
        self.bob.board.append(crd)
        crd.buy()

        self.board.cards.sort(key=lambda x: x.dbfId.rating, reverse=True)
        worst_rating_minion = self.board.cards[-1]
        if worst_rating_minion:
            # rating basé sur base_T3, T1_to_T3_rating basé sur le T1_to_T3_no_refound
            worst_rating_minion_rating = self.all_cards[worst_rating_minion.dbfId].ratings.T1_to_T3
            if card_2.rating-worst_rating_minion_rating > diff_esp or\
                    hasattr(worst_rating_minion, 'sell_on') or\
                    hasattr(worst_rating_minion, 'sell_off'):
                worst_rating_minion.sell()
                crd = self.game.hand.remove_and_create(card_2)
                self.bob.board.append(crd)
                crd.buy()
        else:
            print('No minion in board ?!!')
        self.hand.auto_play()


class AFK:
    def turn_1(self, *args, **kwargs):
        pass
    turn_2 = turn_1

class Yogg:
    def turn_1(self, *args, **kwargs):
        if args:
            card = self.bob.board.create_card_in(args[0])
            self.power.use()
            card.play()

    def turn_2(self, *args, **kwargs):
        self.levelup()

class Xyrella:
    def turn_1(self, *args, **kwargs):
        if args:
            card = self.bob.board.create_card_in(args[0])
            if card.attack <= 2 and card.health <= 2:
                self.power.use()
            else:
                card.buy()
            card.play()

    def turn_2(self, *args, **kwargs):
        self.levelup()

class Roi_liche:
    def turn_1(self, *args, **kwargs):
        if args:
            card = self.hand.create_card_in(args[0])
            card.play()
            self.buff(card, self.power.enchantmentDbfId)

    def turn_2(self, *args, **kwargs):
        self.levelup()
        self.buff(self.board.cards[0], self.power.enchantmentDbfId)

class Y_Shaarj:
    def turn_1(self, *args, **kwargs):
        if args:
            self.board.create_card_in(args[0])
            self.hand.create_card_in(args[0])

    def turn_2(self, *args, **kwargs):
        self.board.remove(self.board.cards[0])
        self.levelup()
        self.hand.cards[0].play()

