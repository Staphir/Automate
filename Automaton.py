from rwAutomata import *

# ==============================================================================
"""Project L3-IT : Atomate"""
# ==============================================================================
__author__  = "Lucie Thomasson & Maxime Dulieu"
# ==============================================================================

class Automaton(object):
    def __init__(self, *args):
        if len(args) == 0:
            self._etats = {0,1}
            self._alphabet = set()
            self._transitions = set()
            self._initiaux = {0}
            self._terminaux = {1}
        elif len(args) == 1:
            if not BasicReader(args[0]).etats == []:
                file = BasicReader(args[0])
                self._etats = self._transform_to_set(file.etats)
                self._alphabet = self._transform_to_set(file.alphabet)
                self._transitions = self._transform_to_set(file.transitions)
                self._initiaux = self._transform_to_set(file.initiaux)
                self._terminaux = self._transform_to_set(file.terminaux)
            else:
                self._etats = {0,1}
                self._alphabet = set()
                self._transitions = set()
                self._initiaux = {0}
                self._terminaux = {1}
        elif len(args) == 5:
            self._etats = args[0]
            self._alphabet = args[1]
            self._transitions = args[2]
            self._initiaux = args[3]
            self._terminaux = args[4]

            self._etats = self._transform_to_set(self._verif_etats())
            # N'accepte que les entiers
            self._alphabet = self._transform_to_set(self._verif_alphabet())
            # N'accepte que les caractères alphanumériques, donc l'alphabet et les chiffres de 0 à 9
            self._transitions = self._transform_to_set(self._verif_trans())
            # N'accepte que les triplets de type int-str-int
            self._initiaux = self._transform_to_set(self._verif_initiaux())
            self._terminaux = self._transform_to_set(self._verif_terminaux())
        else:
            print("Automate non conforme vous avez trois choix :\n"
                  "- Automate() -> automate reconnaissant le langage vide\n"
                  "- Automate(file.aut) -> automate créé à partir d'un fichier .aut\n"
                  "- Automate(Q,Sigma,Delta,initial_states,accepting_states)")
            return

        self._afn = False
        self._afd = False
        self._afdc = False
        if self._test_deterministe():
            if self._test_complete():
                self._afdc = True
            else:
                self._afd = True
        else:
            self._afn = True

    # ------------------------------------------------------------------------------
    @property
    def afd(self): return self._afd
    @property
    def afdc(self): return self._afdc
    @property
    def afn(self): return self._afn
    @property
    def automata(self): return (sorted(list(self._etats)),sorted(list(self._alphabet)),sorted(list(self._transitions)),sorted(list(self._initiaux)),sorted(list(self._terminaux)))
    @property
    def Q(self): return sorted(list(self._etats))
    @property
    def Sigma(self): return sorted(list(self._alphabet))
    @property
    def Delta(self): return sorted(list(self._transitions))
    @property
    def S(self): return sorted(list(self._initiaux))
    @property
    def F(self): return sorted(list(self._terminaux))

    # ------------------------------------------------------------------------------
    def __repr__(self):
        text = "Automaton("
        text += str(len(self._etats)) + ", "
        text += str(len(self._alphabet)) + ", "
        text += str(len(self._transitions)) + ", "
        text += str(len(self._initiaux)) + ", "
        text += str(len(self._terminaux)) + ")"
        return text

    # ------------------------------------------------------------------------------
    def __str__(self):
        text = "Etats :\n "
        for e in self._etats: text += str(e) + " "
        text += "\nAlphabet :\n "
        for a in sorted(list(self._alphabet)): text += a + " "
        text += "\nTransitions :\n"
        for triplet in sorted(list(self._transitions)):
            for c in triplet: text += " " + str(c) + " "
            text += "\n"
        text += "Etats initiaux :\n "
        for i in self._initiaux: text += str(i) + " "
        text += "\nEtats terminaux :\n "
        for t in self._terminaux: text += str(t) + " "

        return text

    # ------------------------------------------------------------------------------

    def __eq__(self, other):
        assert isinstance(other,Automaton), "comparaison possible uniquement entre deux automates"
        return self < other and other < self

    def __lt__(self, other):
        assert isinstance(other,Automaton), "inférieur possible uniquement entre deux automates"
        auto_inter = self.inter(other.complement())
        return not auto_inter._terminaux

    # ------------------------------------------------------------------------------

    def _transform_to_set(self,var):
        s = set()
        if var:
            for i in var:
                s.add(i)
        return s

    # ------------------------------------------------------------------------------

    def _verif_etats(self):
        new_etats = set()
        for etat in self._etats:
            if isinstance(etat, int):
                new_etats.add(etat)
        return new_etats

    # ------------------------------------------------------------------------------

    def _verif_alphabet(self):
        # boucle chaque caractère à faire pour garder que les bon caractères
        new_alphabet = ''
        for lettre in self._alphabet:
            if lettre == '':
                new_alphabet += lettre
            elif 47 < ord(str(lettre)) < 58 or 64 < ord(str(lettre)) < 91 or 96 < ord(str(lettre)) < 123 or not str(lettre):
                new_alphabet += lettre
        return new_alphabet

    # ------------------------------------------------------------------------------

    def _verif_trans(self):
        new_transitions = []
        for triplet in self._transitions:
            if type(triplet[0]) == int and triplet[0] in self._etats and type(triplet[2]) == int and triplet[2] in self._etats:
                if type(triplet[1]) == str:
                    inAlphabet = True
                    for t in triplet[1]:
                        if not t in self._alphabet:
                            inAlphabet = False
                            break
                    if inAlphabet == True:
                        new_transitions.append(triplet)
        if new_transitions == []:
            return None
        else:
            return new_transitions
        # besoin de test int-str-int dans une boucle car tableau de transitions

    # ------------------------------------------------------------------------------

    def _verif_initiaux(self):
        new_initiaux = []
        for etat_init in self._initiaux:
            if isinstance(etat_init, int) and etat_init in self._etats:
                new_initiaux.append(etat_init)
        if new_initiaux == []:
            return None
        else:
            return new_initiaux

    # ------------------------------------------------------------------------------

    def _verif_terminaux(self):
        new_terminaux = []
        for etat_term in self._terminaux:
            if isinstance(etat_term, int) and etat_term in self._etats:
                new_terminaux.append(etat_term)
        if new_terminaux == []:
            return None
        else:
            return new_terminaux

    # ------------------------------------------------------------------------------

    def _test_complete(self):
        # on considère que l'automate envoyé est déterministe (donc _test_deterministe déjà fait)
        if len(self._alphabet)*len(self._etats) == len(self._transitions):
            return True
        else:
            return False

    # ------------------------------------------------------------------------------

    def _test_deterministe(self):
        dico_etats = {}
        for etat in self._etats: dico_etats[etat] = set()
        for etat in self._etats:
            for triplet in self._transitions:
                if triplet[0] == etat:
                    if triplet[1] in dico_etats[triplet[0]]:
                        return False
                    else:
                        dico_etats[triplet[0]].update({triplet[1]})
        return True

    # ------------------------------------------------------------------------------

    def _changement_nom_etats(self, debut):
        d_etats = {}
        nouveaux_etats = set()
        nouvelles_transitions = set()
        nouveaux_initiaux = set()
        nouveaux_terminaux = set()
        c = debut
        for e in self._etats:
            d_etats[c] = e
            c += 1
        # transitions
        for triplet in self._transitions:
            t0 = triplet[0]
            t2 = triplet[2]
            for key in d_etats:
                if triplet[0] == d_etats[key]:
                    t0 = key
                if triplet[2] == d_etats[key]:
                    t2 = key
            nouvelles_transitions.add((t0,triplet[1],t2))
        # etats
        for etat in self._etats:
            for key in d_etats:
                if etat == d_etats[key]:
                    nouveaux_etats.add(key)
                    break
        # initiaux
        for initial in self._initiaux:
            for key in d_etats:
                if initial == d_etats[key]:
                    nouveaux_initiaux.add(key)
                    break
        # terminaux
        for terminal in self._terminaux:
            for key in d_etats:
                if terminal == d_etats[key]:
                    nouveaux_terminaux.add(key)
                    break

        return Automaton(nouveaux_etats, self._alphabet, nouvelles_transitions, nouveaux_initiaux, nouveaux_terminaux)

    # ------------------------------------------------------------------------------

    def access(self):
        e_access = self._initiaux.copy()
        e_second = e_access.copy()
        end = False
        while end == False:
            for triplet in self._transitions:
                if triplet[0] in e_access:
                    e_second.add(triplet[2])
            if e_access == e_second:
                end = True
            else:
                e_access.update(e_second)
        return Automaton(e_access,self._alphabet,self._transitions,self._initiaux,self._terminaux)

    # ------------------------------------------------------------------------------

    def deterministe(self):
        a_access = self.access()
        e_new = a_access._etats.copy()
        t_new = a_access._transitions.copy()

        # 1-un seul état initial
        e_new.add("s")
        for init in self._initiaux:
            t_new.add(('s','',init))

        # 2-un seul état final
        e_new.add("f")
        for term in self._terminaux:
            t_new.add((term,'','f'))

        # 3-éliminer les liaisons suppérieurs à 1
        for triplet in self._transitions:
            long = len(triplet[1])
            if long > 1:
                #(a)
                t_new.remove(triplet)
                #(b)
                for i in range(1,long):
                    e_new.add(str(triplet[0])+"q"+str(i))
                #(c)
                t_new.add((triplet[0],triplet[1][0],str(triplet[0])+"q1"))
                for i in range(2,long):
                    t_new.add((str(triplet[0])+"q"+str(i-1),triplet[1][i-1],str(triplet[0])+"q"+str(i)))
                t_new.add((str(triplet[0])+"q"+str(long-1),triplet[1][long-1],triplet[2]))

        # 4-nouvel état sans épsilones
        e_epsilon = {}
        for etat in e_new:
            i_new_etatmp = [etat]
            for state in i_new_etatmp :
                for triplet in t_new:
                    if triplet[0] == state and triplet[1] == '' and triplet[2] not in i_new_etatmp:
                        i_new_etatmp.append(triplet[2])
                e_epsilon[etat] = i_new_etatmp

        # 5-tableau de fusion
        for key in e_epsilon: e_epsilon[key] = set(e_epsilon[key])
        e_deterministe = {0:e_epsilon['s']}
        dict_trans = {}
        nbe = 0
        i_new_etat = 0
        while i_new_etat in e_deterministe.keys():
            ensemble_depuis = e_deterministe[i_new_etat]
            dict_trans[i_new_etat] = set()
            for lettre in self._alphabet:
                ensemble_access = set()
                e_equivalent = set()
                for i in ensemble_depuis:
                    for triplet in t_new:
                        if triplet[0] == i and triplet[1] == lettre:
                            ensemble_access.add(triplet[2])
                    for e_acc in ensemble_access:
                        e_equivalent.update(e_epsilon[e_acc])
                if e_equivalent:
                    if not e_equivalent in e_deterministe.values():
                        nbe += 1
                        e_deterministe[nbe] = e_equivalent
                        dict_trans[i_new_etat].update({(i_new_etat, lettre, nbe)})
                    else:
                        for key in e_deterministe.keys():
                            if e_deterministe[key] == e_equivalent:
                                etat_arrive = key
                                break
                        dict_trans[i_new_etat].update({(i_new_etat, lettre, etat_arrive)})
            i_new_etat += 1

        transitions_finales = set()
        for key in dict_trans:
            transitions_finales.update(dict_trans.get(key))

        etats_finaux = []
        for key in e_deterministe:
            if 'f' in e_deterministe[key]:
                etats_finaux.append(key)

        return Automaton(range(len(e_deterministe)), self._alphabet, transitions_finales, [0], etats_finaux)

    # ------------------------------------------------------------------------------

    def minimal(self):
        afdc = self.complete()
        terminaux = set()
        non_terminaux = set()
        for t1 in afdc._terminaux:
            for t2 in afdc._terminaux:
                terminaux.update({(t1,t2)})
        for e1 in afdc._etats.difference(afdc._terminaux):
            for e2 in afdc._etats.difference(afdc._terminaux):
                non_terminaux.update({(e1,e2)})
        P = {*terminaux, *non_terminaux}
        Q_F = set()

        while 1:
            for duo in P:
                if duo[0] == duo[1]:
                    Q_F.add((duo[0],duo[1]))
                else:
                    ok = True
                    for lettre in afdc._alphabet:
                        for triplet in afdc._transitions:
                            if triplet[0] == duo[0] and triplet[1] == lettre:
                                trans1 = triplet[2]
                            if triplet[0] == duo[1] and triplet[1] == lettre:
                                trans2 = triplet[2]
                        if (trans1,trans2) not in P:
                            ok = False
                    if ok:
                        d1 = (duo[0],duo[1])
                        d2 = (duo[1],duo[0])
                        Q_F.update({d1,d2})
            if P == Q_F:
                break
            P = Q_F
            Q_F = set()

        equivalents = {}
        for etat in afdc._etats: equivalents[etat] = set()
        for duo in P: equivalents[duo[0]].update({duo[1]})
        for etat in equivalents:
            if len(equivalents[etat]) > 1:
                for e_equi in equivalents[etat]:
                    if e_equi != etat:
                        #etats de l'automate
                        a_discard = set()
                        for e in afdc._etats:
                            if e == e_equi:
                                a_discard.add(e_equi)
                        afdc._etats.difference_update(a_discard)
                        #initiaux
                        a_discard = set()
                        a_union = set()
                        for e in afdc._initiaux:
                            if e == e_equi:
                                a_discard.add(e_equi)
                                a_union.add(etat)
                        afdc._initiaux.difference_update(a_discard)
                        afdc._initiaux.update(a_union)
                        #terminaux
                        a_discard = set()
                        a_union = set()
                        for e in afdc._terminaux:
                            if e == e_equi:
                                a_discard.add(e_equi)
                                a_union.add(etat)
                        afdc._terminaux.difference_update(a_discard)
                        afdc._terminaux.update(a_union)
                        #transitions
                        a_discard = set()
                        a_union = set()
                        for triplet in afdc._transitions:
                            if triplet[0] == e_equi and triplet[2] in afdc._etats:
                                a_union.add((etat,triplet[1],triplet[2]))
                                a_discard.add(triplet)
                            if triplet[2] == e_equi and triplet[0] in afdc._etats:
                                a_union.add((triplet[0],triplet[1],etat))
                                a_discard.add(triplet)
                            if triplet[0] == e_equi and triplet[2] == e_equi:
                                a_union.add((etat,triplet[1],etat))
                                a_discard.add((e_equi,triplet[1],e_equi))
                        afdc._transitions.update(a_union)
                        afdc._transitions.difference_update(a_discard)
                        #efface du dico l'état équivalent
                        equivalents[e_equi] = set()
        return afdc

    # ------------------------------------------------------------------------------

    def complete(self):
        a_deterministe = self.deterministe()
        nouvelles_transitions = a_deterministe._transitions.copy()
        nouveaux_etats = a_deterministe._etats.copy()
        dict_alphabet_etat = {}
        etat_puit = -1
        # Création dictionnaire avec pour chaque état l'alphabet
        for etat in nouveaux_etats:
            dict_alphabet_etat[etat] = set(a_deterministe._alphabet)
        # Supprimme les lettres déjà utilisé dans une transition
        for t in a_deterministe._transitions:
            dict_alphabet_etat[t[0]].discard(t[1])
        # Avons-nous besoin de nouveaux état et donc d'un puit
        for value in dict_alphabet_etat.values():
            if value != {}:
                etat_puit = len(nouveaux_etats)
                nouveaux_etats.update({etat_puit})
                dict_alphabet_etat[etat_puit] = set(a_deterministe._alphabet)
                break
        # Ajout des nouvelles transitions
        if etat_puit != -1:
            for key in dict_alphabet_etat.keys():
                if key:
                    for lettre in dict_alphabet_etat[key]:
                        nouvelles_transitions.update({(key,lettre,etat_puit)})

        return Automaton(nouveaux_etats, a_deterministe._alphabet, nouvelles_transitions, a_deterministe._initiaux, a_deterministe._terminaux).access()

    # ------------------------------------------------------------------------------

    def complement(self):
        complement = self.complete()
        s_terminaux = complement._etats.difference(complement._terminaux)
        return Automaton(complement._etats, complement._alphabet, complement._transitions, complement._initiaux, s_terminaux)

    # ------------------------------------------------------------------------------

    def union(self, *automates):
        automate_trie_1 = self._changement_nom_etats(1)
        for i in automates:
            assert isinstance(i, Automaton), "Les arguments doivent être des automates"
        for auto in automates:
            automate_trie_2 = auto._changement_nom_etats(len(automate_trie_1._etats)+1)
            nouveaux_etats = {0}
            nouveaux_etats.update(automate_trie_1._etats)
            nouveaux_etats.update(automate_trie_2._etats)
            nouveaux_etats.update({len(nouveaux_etats)})
            nouvel_initial = {0}
            etat_terminal = len(nouveaux_etats)-1
            nouvel_terminal = {etat_terminal}
            nouvelles_transitions = set()
            for triplet in automate_trie_1._transitions: nouvelles_transitions.add(triplet)
            for triplet in automate_trie_2._transitions: nouvelles_transitions.add(triplet)
            for initial in automate_trie_1._initiaux: nouvelles_transitions.add((0,'',initial))
            for initial in automate_trie_2._initiaux: nouvelles_transitions.add((0,'',initial))
            for terminal in automate_trie_1._terminaux: nouvelles_transitions.add((terminal,'',etat_terminal))
            for terminal in automate_trie_2._terminaux: nouvelles_transitions.add((terminal,'',etat_terminal))
            nouvelle_alphabet = set()
            nouvelle_alphabet.update(automate_trie_1._alphabet)
            nouvelle_alphabet.update(automate_trie_2._alphabet)
            automate_trie_1 = Automaton(nouveaux_etats, nouvelle_alphabet, nouvelles_transitions, nouvel_initial, nouvel_terminal)
        return automate_trie_1

    # ------------------------------------------------------------------------------

    def inter(self, automate2):
        assert isinstance(automate2, Automaton), "L'argument doit être un automate"

        complement_automate_1 = self.complement()
        complement_automate_2 = automate2.complement()
        automate_union = complement_automate_1.union(complement_automate_2)
        automate_inter = automate_union.complement()

        return automate_inter

    # ------------------------------------------------------------------------------

    def concat(self, automate2):
        assert isinstance(automate2, Automaton), "L'argument doit être un automate"

        automate_trie_1 = self._changement_nom_etats(1)
        nouveaux_etats = {0}
        nouveaux_etats.update(automate_trie_1._etats)
        nouvelles_transitions = set()
        etat_terminal_1 = len(nouveaux_etats)-1
        for triplet in automate_trie_1._transitions: nouvelles_transitions.add(triplet)
        for initial in automate_trie_1._initiaux: nouvelles_transitions.add((0, '', initial))
        for terminal in automate_trie_1._terminaux: nouvelles_transitions.add((terminal, '', etat_terminal_1))

        automate_trie_2 = automate2._changement_nom_etats(len(nouveaux_etats)+1)
        etat_initial_2 = len(nouveaux_etats)
        nouveaux_etats.update({etat_initial_2})
        nouveaux_etats.update(automate_trie_2._etats)
        etat_terminal_2 = len(nouveaux_etats)
        nouveaux_etats.update({etat_terminal_2})
        for triplet in automate_trie_2._transitions: nouvelles_transitions.add(triplet)
        for initial in automate_trie_2._initiaux: nouvelles_transitions.add((0, '', initial))
        for terminal in automate_trie_2._terminaux: nouvelles_transitions.add((terminal, '', etat_terminal_2))
        nouvelle_alphabet = set()
        nouvelle_alphabet.update(automate_trie_1._alphabet)
        nouvelle_alphabet.update(automate_trie_2._alphabet)

        return Automaton(nouveaux_etats, nouvelle_alphabet, nouvelles_transitions, [0], [etat_terminal_2])

    # ------------------------------------------------------------------------------

    def fermeture(self):
        auto_fermeture = Automaton(self._etats.copy(), self._alphabet.copy(), self._transitions.copy(), self._initiaux.copy(), self._terminaux.copy())

        nouvel_initial = len(auto_fermeture._etats)
        auto_fermeture._etats.add(nouvel_initial)
        for init in auto_fermeture._initiaux:
            auto_fermeture._transitions.add((nouvel_initial,'',init))

        nouvel_terminal = len(auto_fermeture._etats)
        auto_fermeture._etats.add(nouvel_terminal)
        for term in auto_fermeture._terminaux:
            auto_fermeture._transitions.add((nouvel_terminal,'',term))

        auto_fermeture._initiaux.clear()
        auto_fermeture._initiaux.add(nouvel_initial)
        auto_fermeture._terminaux.clear()
        auto_fermeture._terminaux.add(nouvel_terminal)

        auto_fermeture._transitions.add((nouvel_terminal,'',nouvel_initial))

        return Automaton(auto_fermeture._etats, auto_fermeture._alphabet, auto_fermeture._transitions, auto_fermeture._initiaux, auto_fermeture._terminaux)




# ==============================================================================



# ==============================================================================
if __name__ == "__main__":
    # a = Automaton(range(4), "bca", [(0, 'a', 0), (0, '', 1), (2, 'cabc', 0), (3,'b',2)], [0,2], [1,2])
    b = Automaton("automata/automata_coursA1.aut")
    c = Automaton("automata/automata_coursA2.aut")
    # d = Automaton("automata/automata_coursA3.aut")
    # r = Automaton()
    # e = Automaton("automata/automata_coursA4.aut")
    # f = Automaton("automata/other.aut")
    # print(b.deterministe().automata)
    # print(b.union(c).minimal().automata)
    # print(b.concat(c).minimal().automata)
    # print(b.inter(c).minimal().automata)
    print(b==c)
    print(c<b)
    # ==============================================================================