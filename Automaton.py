#Ici, le cardinal des ensembles, c'est juste le nombre de valeurs qu'il y a dans ces ensembles
#Exemple : S = {0,1,3} alors cardinal de S = 3


class Automaton(object):
    def __init__(self, etats = None, alphabet = None, trans = None, etats_init = None, etats_term = None):

        self.etats = verif_etats(etats)
        # N'accepte que les entiers
        self.alphabet = verif_alphabet(alphabet)
        # N'accepte que les caractères alphanumériques, donc l'alphabet et les chiffres de 0 à 9
        self.trans = verif_trans(trans, self.alphabet)
        # N'accepte que les triplets de type int-str-int
        self.etats_init = verif_etats_init(etats_init, self.etats)
        self.etats_term = verif_etats_term(etats_term, self.etats)

        #Si etats, alphabet, trans, etats_init et etats_term sont vides :
           #création d un automate reconnaissant le langage vide : " "

        #Pour chaque argument, si il existe:
           #on le traite comme un fichier dans le programme BasicReader
        #mais si un seul de ces arguments existe pas:
           #on construit un automate reconnaissant le langage vide : " "

    # ------------------------------------------------------------------------------
    def __repr__(self):
        #automate = [__init__.etats, __init__.alphabet, __init__.trans, __init__.etats_init, __init__.etats_term]
        #pour chaque argument dans automate, on veut que le programme convertisse chaque cellule (etats, alphabet...)
        #en une str. Ensuite, il calcule le nombre de valeurs dans cette str, et la remplace dans automate.

        #ATTENTION : les transitions sont délimitées par des parenthèses. (1 aa 2) c'est une seule transition et pas 4.
        #Il faut peut etre compacter chaqye transition (1aa2) puis les décompacter au moment de l'affichage ?

        #ATTENTION : les valeurs de l'alphabet sont des triplets. je ne sais pas si ça crée une contrainte...

        #A la fin on renvoie automate, et on aura un truc du genre automate(4,3,1,2,1)

    # ------------------------------------------------------------------------------
    def __str__(self):
        #On veut que la fonction permette de choisir un argument pour aller voir ses valeurs. 
        #On prend les informations renvoyées par __repr__ lorsqu'elles ont été converties en str. 
        #Puis on les classe en fonction des états, des transitions... Et on les affiche avec les 
        #titres correspondants. 

# ==============================================================================
def verif_etats(etats):
    new_etats = set()
    for etat in etats:
        if isinstance(etat, int):
            new_etats.add(etat)
            print("type etats incorrect, il faut un int")
    return new_etats

def verif_alphabet(alphabet):
    #boucle chaque caractère à faire pour garder que les bon caractères
    unicode_alphabet = ord(str(alphabet))
    if 47<unicode_alphabet<58 or 64<unicode_alphabet<91 or 96<unicode_alphabet<123:
        return alphabet
    else:
        print("type alphabet incorrect, il faut un type alphanumérique")
        return None

def verif_trans(trans, alphabet):
    #besoin de test int-str-int dans une boucle car tableau de transitions
    print("type trans incorrect, il faut int-str-int")

    return trans

def verif_etats_init(etat_init, etats):
    if not isinstance(etat_init, int) or not etat_init in etats:
        print("type etats_init incorrect, il faut un int")
        etat_init = None
    return etat_init

def verif_etats_term(etat_term, etats):
    if not isinstance(etat_term, int) or not etat_term in etats:
        print("type etats_term incorrect, il faut un int")
        etat_term = None
    return etat_term

    #Automate fini : Nombre d etats fini

    #Automate fini déterministe : Un symbole traite a la fois qui ne part que dans une direction pour chaque etat

    #Automate fini déterministe complet : Chaque etat possede une solution de passage pour chaque element de l alphabet
                                         #On a aussi l etat puits qui correspond au traitement errone d un etat


# ==============================================================================
if __name__ == "__main__":

# ==============================================================================