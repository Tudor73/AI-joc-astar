from random import randint, random
import time
import copy
import os
import pygame
import sys
from joc import Joc, distEuclid
from butoane import Buton, GrupButoane
from piesa import Piesa
from stare import Stare, min_max, alpha_beta 
ADANCIME_MAX=4


def elem_identice(lista):
    if(len(set(lista))==1) :
        return lista[0] if lista[0]!=Joc.GOL else False
    return False


def afis_daca_final(stare_curenta):
    final=stare_curenta.tabla_joc.final()
    if(final):
        if (final=="remiza"):
            print("Remiza!")
        else:
            print("A castigat "+final)
            
        return True
        
    return False


############# ecran initial ########################
def deseneaza_alegeri(display, tabla_curenta) :
    btn_alg=GrupButoane(
        top=30, 
        left=30,  
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"), 
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="alphabeta")
            ],
        indiceSelectat=1)
    btn_juc=GrupButoane(
        top=100, 
        left=30, 
        listaButoane=[
            Buton(display=display, w=35, h=30, text="alb", valoare="alb"), 
            Buton(display=display, w=35, h=30, text="negru", valoare="negru")
            ], 
        indiceSelectat=0)
    ok=Buton(display=display, top=170, left=30, w=40, h=30, text="ok", culoareFundal=(155,0,55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get(): 
            if ev.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN: 
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if ok.selecteazaDupacoord(pos):
                            display.fill((0,0,0)) #stergere ecran 
                            tabla_curenta.deseneaza_grid()
                            return btn_juc.getValoare(), btn_alg.getValoare()
        pygame.display.update()



def main():

    #setari interf grafica
    pygame.init()
    pygame.display.set_caption("astar")
    #dimensiunea ferestrei in pixeli
    WIDTH, HEIGHT = 400, 700
    ecran=pygame.display.set_mode((WIDTH, HEIGHT))# N *w+ N-1= N*(w+1)-1
    Joc.initializeaza(ecran)

    #initializare tabla
    joc_curent=Joc()
    Joc.JMIN, tip_algoritm = deseneaza_alegeri(ecran,joc_curent)
    print(Joc.JMIN, tip_algoritm)
    if Joc.JMIN == "alb":
        Joc.JMAX = "negru"
    ecran.fill((255,255,255))

    

    pygame.display.update()	    
    
    turn = 0
    print("Tabla initiala")
    
    # #creare stare initiala
    # stare_curenta=Stare(joc_curent,'x',ADANCIME_MAX)

    stare_curenta = Stare(joc_curent, Joc.JMIN, 2)


    joc_curent.deseneaza_grid()
    print("Muta "+ ("negru" if turn else "alb"))
    pygame.display.update()	
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if stare_curenta.j_curent == Joc.JMIN:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for nod in joc_curent.coordonateNoduri:
                        if (distEuclid(*pos, *nod) < joc_curent.razaPct):
                            nod_curent = Piesa(nod[0], nod[1])
                            print(nod_curent)
                            if not joc_curent.piesa_selectata and joc_curent.piesa_valida(turn, nod_curent):
                                joc_curent.piesa_selectata = nod_curent
                                joc_curent.deseneaza_grid()
                            elif joc_curent.piesa_selectata and joc_curent.mutare_valida(turn, nod_curent):
                                piese_albe = copy.deepcopy(joc_curent.piese_albe)
                                piese_negre = copy.deepcopy(joc_curent.piese_negre)
                                joc_nou = Joc(piese_albe, piese_negre)
                                stare_curenta = Stare(joc_nou, Joc.JMAX, stare_curenta.adancime)
                                joc_nou.deseneaza_grid()
                            elif joc_curent.piesa_selectata:
                                if joc_curent.piesa_selectata in joc_curent.piese_negre and nod_curent in joc_curent.piese_negre:
                                    joc_curent.piesa_selectata = nod_curent
                                    joc_curent.deseneaza_grid()

                                if joc_curent.piesa_selectata in joc_curent.piese_albe and nod_curent in joc_curent.piese_albe:
                                    joc_curent.piesa_selectata = nod_curent
                                    joc_curent.deseneaza_grid()
            else:
                l_mutari_posibile = stare_curenta.mutari()
                index = randint(0, len(l_mutari_posibile)-1)
                stare_curenta = l_mutari_posibile[index]
                stare_curenta.tabla_joc.deseneaza_grid()
                joc_curent = stare_curenta.tabla_joc                    

                        
if __name__ == "__main__" :
    main()


    