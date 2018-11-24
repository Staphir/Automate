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
        elif len(args) == 1 and args[0].split(".")[1] == "aut":
            file = BasicReader(args[0])
            self._etats = self.transform_to_set(file.etats)
            self._alphabet = self.transform_to_set(file.alphabet)
            self._transitions = self.transform_to_set(file.transitions)
            self._initiaux = self.transform_to_set(file.initiaux)
            self._terminaux = self.transform_to_set(file.terminaux)
        elif len(args) == 5:
            self._etats = args[0]
            self._alphabet = args[1]
            self._transitions = args[2]
            self._initiaux = args[3]
            self._terminaux = args[4]

            self._etats = self.transform_to_set(self.verif_etats())
            # N'accepte que les entiers
            self._alphabet = self.transform_to_set(self.verif_alphabet())
            # N'accepte que les caractères alphanumériques, donc l'alphabet et les chiffres de 0 à 9
            self._transitions = self.transform_to_set(self.verif_trans())
            # N'accepte que les triplets de type int-str-int
            self._initiaux = self.transform_to_set(self.verif_initiaux())
            self._terminaux = self.transform_to_set(self.verif_terminaux())
        else:
            print("Automate non conforme vous avez trois choix :\n"
                  "- Automate() -> automate reconnaissant le langage vide\n"
                  "- Automate(file.aut) -> automate créé à partir d'un fichier .aut\n"
                  "- Automate(Q,Sigma,Delta,initial_states,accepting_states)")

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
    def automata(self): return (list(self._etats),list(self._alphabet),list(self._transitions),list(self._initiaux),list(self._terminaux))
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

    def transform_to_set(self,var):
        s = set()
        for i in var:
            s.add(i)
        return s


    def verif_etats(self):
        new_etats = set()
        for etat in self._etats:
            if isinstance(etat, int):
                new_etats.add(etat)
        return new_etats

    def verif_alphabet(self):
        # boucle chaque caractère à faire pour garder que les bon caractères
        new_alphabet = ''
        for lettre in self._alphabet:
            if 47 < ord(str(lettre)) < 58 or 64 < ord(str(lettre)) < 91 or 96 < ord(str(lettre)) < 123:
                new_alphabet += lettre
        return new_alphabet

    def verif_trans(self):
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

    def verif_initiaux(self):
        new_initiaux = []
        for etat_init in self._initiaux:
            if isinstance(etat_init, int) and etat_init in self._etats:
                new_initiaux.append(etat_init)
        if new_initiaux == []:
            return None
        else:
            return new_initiaux

    def verif_terminaux(self):
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
        e_access = self._initiaux
        e_second = e_access
        end = False
        while end == False:
            for triplet in self._transitions:
                if triplet[0] in e_access:
                    e_second.add(triplet[2])
            if e_access == e_second:
                end = True
            else:
                e_access.union(e_second)
        return Automaton(e_access,self._alphabet,self._transitions,self._initiaux,self._terminaux)
        # pour chaque état initial regarder s'il existe un triplet qui a pour début l'etat initial pour chaque états non initiaux

# ==============================================================================



# ==============================================================================
if __name__ == "__main__":
    a = Automaton(range(4), "bca", [(0, 'a', 0), (0, 'b', 1), (2, 'cc', 0)], [0,2], [1])
    b = Automaton("automata/automata_1.aut")
    # a = Automaton()
    # print(a)
    # print(repr(a.automata))
    print(a==8)
    # ==============================================================================