import script_minion
import card
import player
import random
import constants
import combat

def print_error(function_name, commentaire, attendu, obtenu):
    if attendu != obtenu:
        print(f"ERROR {function_name} : {commentaire}\
            \nattendu : {attendu}\
            \nobtenu : {obtenu}")


class test():
    def test_all(self, bob):
        self.Guetteur_pri(bob)
        """
        self.Bob(bob)
        #self.Murozond(bob)
        self.Aile_de_mort(bob)
        self.Daryl(bob)
        self.Edwin(bob)
        #self.Maitre_chien(bob)
        self.Reno1(bob)
        self.Reno2(bob)
        self.Amalgadon_double_deathrattle(bob)
        self.Brutalite_heraut(bob)
        self.Deflecto_rover_goule(bob)
        self.Cleave(bob)
        self.Toxi_bouclier(bob)
        self.Dragonnet_Illidan(bob)
        self.Dragonnet_Illidan2(bob)
        self.Baron_Boum(bob)
        self.Baron_Boum2(bob)
        self.Gardien_AlAkir(bob)
        self.Khadgar_invoc(bob)
        self.Khadgar_invoc2(bob)
        self.Tasse_menagerie(bob)
        self.Alexstrasza(bob)
        self.Bazial(bob)
        self.Millificent(bob)
        self.Aranna(bob)
        self.Sindragosa(bob)
        self.Regisseur(bob)
        self.Yogg(bob)
        self.Raflelor(bob)
        """

    def Guetteur_pri(self, bob):
        player_1 = player.Player(bob, '', '')
        player_2 = player.Player(bob, '', '')
        bob.go_party(player_1, player_2)
        bob.begin_turn()
        murloc_1 = player_1.hand.create_card('105')
        murloc_2 = player_1.hand.create_card('503')
        murloc_3 = player_1.hand.create_card('105')
        murloc_4 = player_1.hand.create_card('503')
        murloc_1.play()
        murloc_2.play()
        murloc_3.play()
        murloc_4.play()
        print(player_1.board)
        murloc_4.die()
        print(player_1.board)
        murloc_1.set_card("108", copy=False)
        print(player_1.board)
        murloc_1.health -= 1
        print(player_1.board)
        murloc_2.die()
        print(player_1.board)


    def Raflelor(self, bob):
        player_1 = player.Player(bob, '', '')
        player_2 = player.Player(bob, '', '')
        bob.go_party(player_1, player_2)
        bob.begin_turn()
        goldencard = player_1.hand.create_card('100_p')
        rafle = player_1.hand.create_card('420')
        goldencard.play()
        rafle.play()
        bob.end_turn()
        print_error('Raflelor', 'Bonus incorrect', 2*2, rafle.attack - rafle.init_attack)
        print(rafle)

    def Aile_de_mort(self, bob):
        player_1 = player.Player(bob, '', 'Aile de mort')
        player_2 = player.Player(bob, '', '')

        bob.go_party(player_1, player_2)
        bob.begin_turn()
        minion = player_1.board.opponent[0]
        minion.trade()
        minion.play()
        print_error('Aile de mort', 'Attaque bonus incorrecte', 2, minion.attack - minion.init_attack)
        minion = player_1.board.opponent[0]
        print_error('Aile de mort', 'Attaque bonus incorrecte (2)', 2, minion.attack - minion.init_attack)

    def Daryl(self, bob):
        player_1 = player.Player(bob, '', 'Daryl')
        player_2 = player.Player(bob, '', '')

        bob.go_party(player_1, player_2)
        bob.begin_turn()
        player_1.gold = 7
        minion = player_1.board.opponent[0]
        minion.trade()
        print_error('Daryl', 'Gold incorrectes', 4, player_1.gold)
        minion2 = player_1.board.opponent[0]
        minion2.trade()
        minion.play()
        minion2.play()
        minion.trade()
        minion2.trade()
        print_error('Daryl', 'Gold incorrectes', 3, player_1.gold)
        minion = player_1.board.opponent[0]
        minion.trade()
        print_error('Daryl', 'Gold incorrectes', 0, player_1.gold)
        minion.play()
        print_error('Daryl', 'Caractéristiques incorrectes', [4, 4], [minion.attack - minion.init_attack, minion.health - minion.init_health])

    def Edwin(self, bob):
        player_1 = player.Player(bob, '', 'Edwin')
        player_2 = player.Player(bob, '', '')

        bob.go_party(player_1, player_2)
        bob.begin_turn()
        player_1.gold = 7
        minion = player_1.board.opponent[0]
        minion.trade()
        minion.play()
        minion = player_1.board.opponent[0]
        minion.trade()
        minion.play()
        minion = player_1.power.active_manual()
        print_error('Edwin', 'Caractéristiques incorrectes', [2, 2], [minion.attack - minion.init_attack, minion.health - minion.init_health])

    def Maitre_chien(self, bob):
        player_1 = player.Player(bob, '', '')
        player_2 = player.Player(bob, '', '')

        bob.go_party(player_1, player_2)
        bob.begin_turn()
        cat = player_1.hand.create_card('103')
        cat.play()
        master = player_1.hand.create_card('307')
        master.play()

    def Murozond(self, bob):
        player_1 = player.Player(bob, '', '')
        player_2 = player.Player(bob, '', '')

        bob.go_party(player_1, player_2)
        bob.begin_turn(False)
        player_2.board.create_card("107") # Tisse-colère
        bob.end_turn()

        bob.begin_turn(False)
        player_1.force_buy_card("513") # Murozond
        bob.end_turn()

        print_error("Murozond", "Nombre de carte dans la main incorrecte", 1, len(player_1.hand))
        print_error("Murozond", "Carte dans la main incorrecte", "107", player_1.hand[0].key_number)

    def Reno1(self, bob):
        player_1 = player.Player(bob, '', 'Reno')
        card = player_1.board.create_card("107") # Tisse-colère
        card.set_card("107_p")
        print_error("Reno1", "key_number incorrect", "107_p", card.key_number)
        print_error("Reno1", "caractéristiques incorrectes", [2, 6], [card.attack, card.health])

    def Reno2(self, bob):
        player_1 = player.Player(bob, '', 'Reno')
        card = player_1.board.create_card("109") # Micro-momie
        card2 = player_1.hand.create_card("404") # Ennuyo-module
        card2.play(position=0)
        card.set_card("109_p")
        print_error("Reno2", "key_number incorrect", "109_p", card.key_number)
        print_error("Reno2", "caractéristiques incorrectes", [4, 8], [card.attack, card.health])
        print_error("Reno2", "state incorrect", 7, card.state)

    def Yogg(self, bob):
        player_1 = player.Player(bob, "", "Yogg")
        player_2 = player.Player(bob, "", "")

        bob.go_party(player_1, player_2)
        bob.begin_turn(False)
        player_1.power.active_manual()

        print_error("Yogg", "nombre de carte dans la main incorrect", 1, len(player_1.hand))
        print_error("Yogg", "attaque bonus incorrecte", 1, player_1.hand[0].attack - player_1.hand[0].init_attack)


    def Bob(self, bob):
        j1 = player.Player(bob, "Rivvers", "Ysera")
        j2 = player.Player(bob, "notoum", "George")
        bob.go_party(j1, j2)
        bob.begin_turn()
        j1.board.opponent.create_card("201")
        j1.hand.create_card("202")
        card = random.choice(bob.hand.cards_of_tier_max(6))
        card.play(board=j1.board.opponent)

        #print_error("Bob", "Taille main incorrecte", 7, len(bob.hand))

    def Regisseur(self, bob):
        player_1 = player.Player(bob, "", "")
        player_2 = player.Player(bob, "", "")

        bob.go_party(player_1, player_2)
        bob.begin_turn(False)
        regisseur = player_1.hand.create_card("214")
        regisseur.play()
        regisseur.trade()
        atk_bonus = player_1.bob_board[0].attack - player_1.bob_board[0].init_attack
        print_error("Regisseur", "Erreur d'attaque bonus", 2, atk_bonus)


    def Sindragosa(self, bob):
        player_1 = player.Player(bob, "", "Sindragosa")
        player_2 = player.Player(bob, "", "")

        bob.go_party(player_1, player_2)
        bob.begin_turn(False)
        board_1 = player_1.bob_board
        player_1.board.opponent.freeze()
        bob.end_turn()
        bob.begin_turn(False)
        board_2 = player_1.bob_board
        minion = player_1.bob_board[0]
        print_error("Sindragosa", "Erreur d'attaque bonus", 2, minion.attack - minion.init_attack)
        print_error("Sindragosa", "Board de Bob différent", [board_1, board_1], [board_1, board_2])

    def Aranna(self, bob):
        player_1 = player.Player(bob, "", "Aranna")
        player_2 = player.Player(bob, "", "")

        #bob.go_party(player_1, player_2, player_3, player_4, player_5, player_6, player_7, player_8)
        bob.go_party(player_1, player_2)

        bob.begin_turn(False)
        player_1.roll(4)
        bob.end_turn()
        bob.begin_turn(False)
        player_1.roll(2)
        nb_minion = len(bob.boards[player_1])
        print_error("Aranna", "Nombre de carte chez Bob incorrect", 7, nb_minion)

    def Millificent(self, bob): # problème si Mech ban
        player_1 = player.Player(bob, "", "Millificent")
        player_2 = player.Player(bob, "", "")
        bob.go_party(player_1, player_2)

        find = False
        player_1.nb_free_roll = 10
        bob.begin_turn(False)
        while not find:
            for minion in player_1.bob.boards[player_1]:
                if minion.type & constants.TYPE_MECH:
                    minion.play(board=player_1.board.opponent)
                    minion.trade()
                    atk_bonus = minion.attack - minion.init_attack
                    def_bonus = minion.health - minion.init_health
                    find = True
                    break
            player_1.roll()
        print_error("Millificent", "Aucun méca trouvé", True, find)
        print_error("Millificent", "Caractéristiques du méca incorrectes", [1, 1], [atk_bonus, def_bonus])

    def Bazial(self, bob):
        player_1 = player.Player(bob, "", "Baz'hial")
        j2 = player.Player(bob, "", "")
        bob.go_party(player_1, j2)
        bob.begin_turn(no_bob=True)

        card_id = player_1.power.active_manual()
        print_error("Bazial", "pv incorrects", 38, player_1.hp)
        print_error("Bazial", "nombre de carte dans la main incorrect", 1, len(player_1.hand))
        card_id.play()
        print_error("Bazial", "po incorrectes", 4, player_1.gold)
        print_error("Bazial", "nombre de carte dans la main incorrect (2)", 0, len(player_1.hand))
        player_1.board.create_card("503") # Mal'Ganis
        card_id = player_1.power.active_manual()
        print_error("Bazial", "pv incorrects", 38, player_1.hp)
        # un pouvoir n'est utilisable qu'une fois par tour
        print_error("Bazial", "nombre de carte dans la main incorrect (3)", 0, len(player_1.hand))


    def Alexstrasza(self, bob):
        player_1 = player.Player(bob, "", "Alexstrasza")
        j2 = player.Player(bob, "", "")
        bob.go_party(player_1, j2)

        player_1.level_up_cost = 0
        player_1.level = 4
        player_1.level_up()
        print_error("Alexstrasza", "nombre de carte dans la main incorrect", 2, len(player_1.hand))
        for minion in player_1.hand:
            if not minion.type & constants.TYPE_DRAGON:
                print(f"ERROR Alexstrasza serviteur découvert non dragon")


    def Tasse_menagerie(self, bob):
        j1 = player.Player(bob, "", "")
        j2 = player.Player(bob, "", "")
        bob.go_party(j1, j2)
        bob.begin_turn()

        # Amalgame, hyène, gentille grand-mère, le clan des rats
        j1.board.create_card("151", "104", "203", "305")
        j1.force_buy_card("217") # tasse
        atk_cumul = 0
        for minion in j1.board:
            atk_cumul += minion.attack - minion.init_attack
        print_error("Tasse_ménagerie", "Attaque bonus incorrecte", 2, atk_cumul)

    def Khadgar_invoc2(self, bob):
        j1 = player.Player(bob, "", "")
        j2 = player.Player(bob, "", "")
        bob.go_party(j1, j2)
        bob.begin_turn()

        j1.board.create_card("303_p", "209") # khadgar doré, chef de meute
        j1.force_buy_card("103", position=0) # chat
        for minion in j1.board[::-1]:
            if minion.key_number == "103a":
                last_cat = minion
                break

        print_error("Khadgar_invoc2", "Erreur nombre de serviteurs", 6, len(j1.board))
        print_error("Khadgar_invoc2", "Attaque bonus chat tigré incorrecte", 3, last_cat.attack)


    def Khadgar_invoc(self, bob):
        j1 = player.Player(bob, "", "")
        j2 = player.Player(bob, "", "")
        bob.go_party(j1, j2)
        bob.begin_turn()


        j1.board.create_card("303") # khadgar
        mande = j1.board.create_card("102") # mande_flots
        j1.gold = 6
        j1.force_buy_card("100", position=0) # chasse-marée murloc
        j1.force_buy_card("100", position=0)

        print_error("Khadgar_invoc", "Erreur nombre de serviteurs", 7, len(j1.board))
        print_error("Khadgar_invoc", "Attaque bonus mande-flots incorrecte", 6, mande.attack)

    def Gardien_AlAkir(self, bob):
        j1 = player.Player(bob, "", "Al'Akir")
        j2 = player.Player(bob, "", "")
        bob.go_party(j1, j2)

        j1.board.create_card("211") # Gardien des glyphes
        tisse = j1.board.create_card("107") # Tisse-colère
        j2.board.create_card("608") # Kalecgos
        champ = combat.Combat(j1, j2)
        gagnant, damage = champ.fight_initialisation()
        if gagnant != j1:
            print("ERROR Gardien_AlAkir :\
            \n espéré : j1 gagnant")
        if damage != j1.level+tisse.level:
            print(f"ERROR Gardien_AlAkir : damage\
            \n espéré {j1.level+tisse.level}\
            \n obtenu {damage}")

    def Baron_Boum(self, bob):
        j1 = player.Player(bob, "", "")
        j2 = player.Player(bob, "", "")
        bob.go_party(j1, j2)

        j1.board.create_card("206") # Gro'Boum
        baron = j1.board.create_card("500") # Baron vaillefendre
        j2.board.create_card("613") # Zapp
        champ = combat.Combat(j1, j2)
        gagnant, damage = champ.fight_initialisation()
        if gagnant != j1:
            print("ERROR Baron_Boum :\
            \n espéré : j1 gagnant")
        if damage != j1.level+baron.level:
            print(f"ERROR Baron_Boum : damage\
            \n espéré {j1.level+baron.level}\
            \n obtenu {damage}")

    def Baron_Boum2(self, bob):
        j1 = player.Player(bob, "", "")
        j2 = player.Player(bob, "", "Illidan")
        bob.go_party(j1, j2)
        bob.begin_turn()

        j1.board.create_card("206", "500") # Gro'Boum, Baron vaillefendre
        zapp = j2.board.create_card("613") # Zapp
        j1.bob.end_turn()
        champ = combat.Combat(j1, j2)
        gagnant, damage = champ.fight_initialisation()
        if gagnant != j2:
            print("ERROR Baron_Boum2 :\
            \n espéré : j2 gagnant")
        if damage != zapp.level+j2.level:
            print(f"ERROR Baron_Boum2 : damage\
            \n espéré {zapp.level+j2.level}\
            \n obtenu {damage}")

    def Dragonnet_Illidan(self, bob):
        j1 = player.Player(bob, "", "Illidan")
        j2 = player.Player(bob, "", "")
        bob.go_party(j1, j2)
        bob.begin_turn()

        j1.board.create_card("315") # cyclone crépitant
        j2.board.create_card("112", "112") # Dragonnet rouge
        bob.end_turn()
        champ = combat.Combat(j1, j2)
        gagnant, damage = champ.fight_initialisation()
        if gagnant != None:
            print("ERROR Dragonnet_Illidan : j1 ???\
            \n espéré : égalité")

    def Dragonnet_Illidan2(self, bob):
        j1 = player.Player(bob, "", "Illidan")
        j2 = player.Player(bob, "")
        bob.go_party(j1, j2)
        bob.begin_turn()

        zapp = j1.board.create_card("613") # Zapp
        j2.board.create_card("112", "112", "112", "112") # Dragonnet rouge
        bob.end_turn()
        champ = combat.Combat(j1, j2)
        gagnant, damage = champ.fight_initialisation()
        if gagnant != j1:
            print("ERROR Dragonnet_Illidan2 : j1 perdant\
            \n espéré : j1 gagnant")
        if damage != j1.level+zapp.level:
            print(f"ERROR Dragonnet_Illidan2 : damage incorrect\
            \n espéré : {j1.level+zapp.level}\
            \n obtenu : {damage}")

    def Toxi_bouclier(self, bob):
        j1 = player.Player(bob, "")
        j2 = player.Player(bob, "")
        bob.go_party(j1, j2)
        bob.begin_turn()

        spore = j1.board.create_card("521") # spore mortelle
        spore.state |= 0x2 
        j2.board.create_card("601") # Maexxna
        j1.bob.end_turn()

        champ = combat.Combat(j1, j2)
        gagnant, damage = champ.fight_initialisation()
        if gagnant != j1:
            print("ERROR Toxi_bouclier : j1 non gagnant\
            \n espéré : gagnant")
        if damage != spore.level+j1.level:
            print(f"ERROR Toxi_bouclier : damage incorrect\
            \n espéré : {spore.level+j1.level}\
            \n obtenu : {damage}")

    def Cleave(self, bob):
        j1 = player.Player(bob, "po")
        j2 = player.Player(bob, "ca")
        bob.go_party(j1, j2)
        bob.begin_turn()

        j1.board.create_card("407") # hydre
        j2.board.create_card("203", "610", "215") # gentille grand-mère, Lieutenant Garr, saurolisque enragé
        bob.end_turn()

        champ = combat.Combat(j1, j2)
        gagnant, damage = champ.fight_initialisation()
        if gagnant != None:
            print("ERROR Cleave : résultat du match incorrect\
            \n espéré : égalité")


    def Deflecto_rover_goule(self, bob):
        j1 = player.Player(bob, "")
        j2 = player.Player(bob, "")
        bob.go_party(j1, j2)
        bob.begin_turn()

        j1.board.create_card("205", "318", "410") # goule, deflecto, rover
        j2.board.create_card("101") # rochecave

        j1.bob.end_turn()

        champ = combat.Combat(j1, j2)
        gagnant, damage = champ.fight_initialisation()
        if gagnant != j1:
            print("ERROR Deflecto_rover_goule : j1 perdant\
            \n espéré : gagnant")
        minion_key_theorique = ["318", "410", "410a"]
        minion_key_obtenu = []
        minion_state_theorique = [2, 0, 1]
        minion_state_obtenu = []

        for minion in j1.board:
            minion_key_obtenu.append(minion.key_number)
            minion_state_obtenu.append(minion.state)

        if minion_key_obtenu != minion_key_theorique:
            print(f"ERROR Deflecto_rover_goule board : \
                \n espéré : {minion_key_theorique}\
                \n obtenu : {minion_key_obtenu}")
        elif j1.board[2].health != 0:
            print(f"ERROR Deflecto_rover_goule : Erreur health robot gardien : \
                \n espéré : 0\
                \n obtenu : {j1.board[2].health}")

        if minion_state_obtenu != minion_state_theorique:
            print(f"ERROR Deflecto_rover_goule board : State incorrect : \
                \n espéré : {minion_state_theorique}\
                \n obtenu : {minion_state_obtenu}")


    def Brutalite_heraut(self, bob):
        j1 = player.Player(bob, "")
        j2 = player.Player(bob, "")
        bob.go_party(j1, j2)

        heraut = j1.board.create_card("418")

        while len(j2.board) < constants.BATTLE_SIZE:
            j2.board.create_card("306a")

        champ = combat.Combat(j1, j2)
        gagnant, damage = champ.fight_initialisation()
        if gagnant == j2:
            print("ERROR Brutalite_heraut : j1 perdant\
            \n espéré : gagnant")
        if heraut.health != 4:
            print(f"ERROR Brutalite_heraut : total défense incorrect\
            \n espéré : 4\
            \n obtenu {heraut.health}\
            \n {heraut.init_health} {heraut.health}")

    def Amalgadon_double_deathrattle(self, bob):
        player_1 = player.Player(bob, "")
        player_2 = player.Player(bob, "")
        bob.go_party(player_1, player_2)
        bob.begin_turn()

        amalgadon = player_1.board.create_card("602_p")
        script_minion.adapt_spell(amalgadon, 8)
        player_1.force_buy_card("308", position=0)
        amalgadon.active_script_type(constants.EVENT_DEATHRATTLE)
        lst_minion_name_obtenu = []
        lst_minion_name_theorique = ["Amalgadon", "Micro-bot", "Micro-bot", "Micro-bot", "Plante", "Plante"]
        lst_minion_premium_obtenu = []
        for minion in player_1.board:
            lst_minion_name_obtenu.append(minion.name)
            lst_minion_premium_obtenu.append(minion.is_premium)

        print_error("Amalgadon_double_deathrattle", "Erreur nombre de serviteurs", 6, len(player_1.board))
        print_error("Amalgadon_double_deathrattle", "Erreur dans l'ordre d'invocation", lst_minion_name_theorique, lst_minion_name_obtenu)
        print_error("Amalgadon_double_deathrattle", "Erreur serviteurs premiums", [True, False, False, False, False, False], lst_minion_premium_obtenu)
        print_error('Amalgadon_double_deathrattle', 'Caractéristiques incorrectes', [15, 13], [amalgadon.attack, amalgadon.health])
