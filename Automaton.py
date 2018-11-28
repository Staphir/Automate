from automata.rwAutomata import *
#Ici, le cardinal des ensembles, c'est juste le nombre de valeurs qu'il y a dans ces ensembles
#Exemple : S = {0,1,3} alors cardinal de S = 3


class Automaton(object):
    def __init__(self, *args):
        if len(args) == 0:
            self._etats = {0}
            self._alphabet = set()
            self._transitions = set()
            self._initiaux = {0}
            self._terminaux = {0}
        elif len(args) == 1:
            if not BasicReader(args[0]) == []:
                file = BasicReader(args[0])
                self._etats = self._transform_to_set(file.etats)
                self._alphabet = self._transform_to_set(file.alphabet)
                self._transitions = self._transform_to_set(file.transitions)
                self._initiaux = self._transform_to_set(file.initiaux)
                self._terminaux = self._transform_to_set(file.terminaux)
            else:
                self._etats = {0}
                self._alphabet = set()
                self._transitions = set()
                self._initiaux = {0}
                self._terminaux = {0}
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

        self._afd = True
        self._afdc = False
        self._afn = True

        #Si etats, alphabet, trans, initiaux et terminaux sont vides :
           #création d un automate reconnaissant le langage vide : " "

        #Pour chaque argument, si il existe:
           #on le traite comme un fichier dans le programme BasicReader
        #mais si un seul de ces arguments existe pas:
           #on construit un automate reconnaissant le langage vide : " "

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
    def T(self): return sorted(list(self._terminaux))

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
        #automate = [__init__.etats, __init__.alphabet, __init__.trans, __init__.initiaux, __init__.terminaux]
        #pour chaque argument dans automate, on veut que le programme convertisse chaque cellule (etats, alphabet...)
        #en une str. Ensuite, il calcule le nombre de valeurs dans cette str, et la remplace dans automate.

        #ATTENTION : les transitions sont délimitées par des parenthèses. (1 aa 2) c'est une seule transition et pas 4.
        #Il faut peut etre compacter chaque transition (1aa2) puis les décompacter au moment de l'affichage ?

        #ATTENTION : les valeurs de l'alphabet sont des triplets. je ne sais pas si ça crée une contrainte...

        #A la fin on renvoie automate, et on aura un truc du genre automate(4,3,1,2,1)

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
        return self._alphabet == other.Sigma

        #On veut que la fonction permette de choisir un argument pour aller voir ses valeurs. 
        #On prend les informations renvoyées par __repr__ lorsqu'elles ont été converties en str. 
        #Puis on les classe en fonction des états, des transitions... Et on les affiche avec les 
        #titres correspondants.

    def _transform_to_set(self,var):
        s = set()
        for i in var:
            s.add(i)
        return s


    def _verif_etats(self):
        new_etats = set()
        for etat in self._etats:
            if isinstance(etat, int):
                new_etats.add(etat)
        return new_etats

    def _verif_alphabet(self):
        # boucle chaque caractère à faire pour garder que les bon caractères
        new_alphabet = ''
        for lettre in self._alphabet:
            if 47 < ord(str(lettre)) < 58 or 64 < ord(str(lettre)) < 91 or 96 < ord(str(lettre)) < 123 or not str(lettre):
                new_alphabet += lettre
        return new_alphabet

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

    def _verif_initiaux(self):
        new_initiaux = []
        for etat_init in self._initiaux:
            if isinstance(etat_init, int) and etat_init in self._etats:
                new_initiaux.append(etat_init)
        if new_initiaux == []:
            return None
        else:
            return new_initiaux

    def _verif_terminaux(self):
        new_terminaux = []
        for etat_term in self._terminaux:
            if isinstance(etat_term, int) and etat_term in self._etats:
                new_terminaux.append(etat_term)
        if new_terminaux == []:
            return None
        else:
            return new_terminaux

        # Automate fini : Nombre d etats fini

        # Automate fini déterministe : Un symbole traite a la fois qui ne part que dans une direction pour chaque etat

        # Automate fini déterministe complet : Chaque etat possede une solution de passage pour chaque element de l alphabet
        # On a aussi l etat puits qui correspond au traitement errone d un etat

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


    def deterministe(self):
        a_access = self.access()
        e_new = a_access._etats.copy()
        t_new = a_access._transitions.copy() #ATTENTION bien mettre .copy() car sinon modification directement sur le self
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
        e_epsi = {}
        continuer = True
        for etat in e_new:
            e_tmp = {etat}
            while continuer == True:
                len_past = len(e_tmp)
                continuer = False
                for triplet in t_new:
                    if triplet[0] in e_tmp and triplet[1] == '':
                        e_tmp.add(triplet[2])
                if len(e_tmp)>len_past:
                    continuer = True
            e_epsi[etat] = e_tmp
            continuer = True

        # 5-tableau de fusion
        e_deter = {0:e_epsi['s']}
        dict_trans = {}
        end = False
        nbe = 0
        e_t = 0
        while end == False:
            end = True
            while e_t in e_deter.keys():
                e_d = e_deter[e_t]
                for lettre in self._alphabet:
                    s_tmp = set()
                    for t in e_d:
                        for triplet in self._transitions:
                            if triplet[0] == t and triplet[1] == lettre:
                                s_tmp.add(triplet[2])
                        e_equi = set()
                        for e_acc in s_tmp:
                            e_equi.update(e_epsi[e_acc])
                        if not e_equi in e_deter.values() and e_equi :
                            nbe += 1
                            e_deter[nbe] = e_equi
                            dict_trans[nbe] = set()
                            end = False
                        elif e_equi:
                            for key in e_deter.keys():
                                if e_deter[key] == e_equi:
                                    dict_trans[nbe].update({(e_t,lettre,key)})
                e_t += 1
        print(e_deter)
        print(dict_trans)
        self._afn = False
        self._afd = True
# ==============================================================================



# ==============================================================================
if __name__ == "__main__":
    # a = Automaton(range(4), "bca", [(0, 'a', 0), (0, '', 1), (2, 'cabc', 0), (3,'b',2)], [0,2], [1])
    b = Automaton("automata/automata_cours.aut")
    # a = Automaton()
    # print(repr(a.automata))
    # print(b.automata)
    b.deterministe()
    # ==============================================================================