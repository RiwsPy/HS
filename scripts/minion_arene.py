
class Chasse_maree_murloc:
    strats = ('strat_1')

    def __iter__(self):
        yield self.__class__.strats

    class strat_1:
        def turn_1(self, player):
            player.bob.board.append(self)
            self.buy()
            self.play()

        def turn_2(self, player):
            player.levelup()

        def turn_3(self, player, *cards):
            pass

Chasseur_rochecave = Chasse_maree_murloc
Mande_flots_murloc = Chasse_maree_murloc
Chat_de_gouttiere = Chasse_maree_murloc
Hyene_charognarde = Chasse_maree_murloc
Homoncule_sans_gene = Chasse_maree_murloc
Tisse_colere = Chasse_maree_murloc
Serviteur_diabolique = Chasse_maree_murloc
Micromomie = Chasse_maree_murloc
Micro_machine = Chasse_maree_murloc
Lieutenant_draconide = Chasse_maree_murloc
Dragonnet_rouge = Chasse_maree_murloc
Forban = Chasse_maree_murloc
Mousse_du_pont = Chasse_maree_murloc
Acolyte_CThun = Chasse_maree_murloc
Élémenplus = Chasse_maree_murloc
Anomalie_actualisante = Chasse_maree_murloc
Bronze_couenne = Chasse_maree_murloc



class Geomancien_de_Tranchebauge:
    strats = ('strat_1', 'strat_2')

    class strat_1:
        def turn_1(self, player):
            player.bob.board.append(self)
            self.buy()
            self.play()

        def turn_2(self, player):
            player.levelup()

        def turn_3(self, player, *cards):
            pass

    class strat_2:
        def turn_1(self, player):
            player.bob.board.append(self)
            self.buy()
            player.hand.auto_play()

        def turn_2(self, player):
            player.levelup()

        def turn_3(self, player, *cards):
            pass
