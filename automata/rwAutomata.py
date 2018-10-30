#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "05.10.18"
__usage__ = "read/write .aut files"

import os, sys

class BasicReader:
    def __init__(self, fname):
        self.__istates = set([])
        self.__tstates = set([])
        self.__states = set([])
        self.__trans = set([])
        self.__alfaB = set([])
        
        print("Lecture de {}".format(fname))
        _0 =  fname.split('.')
        if len(_0) == 1: _1 = fname+'.aut'
        elif _0[-1] == 'aut': _1 = fname
        else: _1 = fname+'.aut'

        if os.path.isfile(_1):
            with open(_1, 'r') as _2:
                _lines = [ _.strip() for _ in _2.readlines() ]
                _2.close()
        else:
            _lines = []

        self.traitement(_lines)
        print("_"*7)

    # property
    @property
    def initiaux(self): return frozenset(self.__istates)
    @property
    def terminaux(self): return frozenset(self.__tstates)
    @property
    def etats(self): return frozenset(self.__states)
    @property
    def transitions(self): return frozenset(self.__trans)
    @property
    def alphabet(self): return frozenset(self.__alfaB)

    def traitement(self, liste):
        """ gère une liste de lignes """
        for l in liste:
            if '#' in l: _lig = l.split('#')[0]
            else: _lig = l
            if _lig == '': continue
            if _lig[0] == '>': self.__r_initiaux(_lig[1:].split())
            elif _lig[0] == '<': self.__r_terminaux(_lig[1:].split())
            else: self.__r_transitions(_lig.split())

    # Méthodes privées de traitement des lignes
    def __r_initiaux(self, liste):
        """ gère une liste d'états initiaux """
        print('initial', liste)
        for state in liste:
            if state.isdigit():
                self.__istates.add(int(state))
                self.__states.add(int(state))

    def __r_terminaux(self, liste):
        """ gère une liste d'états initiaux """
        print('terminal', liste)
        for state in liste:
            if state.isdigit():
                self.__tstates.add(int(state))
                self.__states.add(int(state))

    def __r_transitions(self, tr_lst):
        """ gère une transition """
        print('transition', tr_lst)
        _0 = None ; _1 = None ; _2 = None
        if len(tr_lst) == 2:
            _0 = int(tr_lst[0]) if tr_lst[0].isdecimal() else None
            _2 = int(tr_lst[1]) if tr_lst[1].isdecimal() else None
            _1 = ''
        elif len(tr_lst) == 3:
            _0 = int(tr_lst[0]) if tr_lst[0].isdecimal() else None
            _2 = int(tr_lst[2]) if tr_lst[2].isdecimal() else None
            _1 = tr_lst[1] if tr_lst[1].isalnum() else None

        if None in (_0, _1, _2): print("{} ignored".format(tr_lst))
        else:
            self.__states.add(_0)
            self.__states.add(_2)
            if _1 != '': self.__alfaB.update(_1)
            self.__trans.add( (_0, _1, _2) )

class BasicWriter:
    def __init__(self, initiaux, terminaux, transitions, fname):
        """ aucun controle ou presque """
        _0 =  fname.split('.')
        if len(_0) == 1: _1 = fname+'.aut'
        elif _0[-1] == 'aut': _1 = fname
        else: _1 = fname+'.aut'

        _2 = "oO0Yy"
        if os.path.isfile(_1):
            _msg = "{} exists, write [{}] ?".format(_1,_2)
            _3 = input(_msg)
            if _3 not in _2: sys.exit(0)
            
        print("Ecriture dans {}".format(_1))
        with open(_1, 'w') as _f:
            _f.write("# automatic generation\n")
            _in = "> {}\n".format(" ".join([str(_) for _ in initiaux]))
            _f.write(_in)
            _out = "< {}\n".format(" ".join([str(_) for _ in terminaux]))
            _f.write(_out)
            for tr in transitions:
                _ = ""
                for x in tr: _ = _+"{} ".format(x)
                _f.write(_+'\n')
            _f.close()

        print("fin de l'écriture dans {}".format(_1))
        print("##"*13)
        
if __name__ == "__main__":
    for fichier in "tyty automata_0 automata_0.aut automata_1".split():
        a = BasicReader(fichier)
        for meth in "initiaux terminaux etats transitions alphabet".split():
            print(meth, getattr(a, meth))
        print("="*13)

    mmc_file = "checkMe_mmc"
    
    b = BasicWriter(a.initiaux, a.terminaux, a.transitions, mmc_file)

    c = BasicReader(mmc_file)

