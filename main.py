import time
import copy
import os
import pygame
import sys
from random import randint, random
from joc import Joc, distEuclid
from butoane import Buton, GrupButoane
from piesa import Piesa
from stare import Stare, min_max, alpha_beta 

def elem_identice(lista):
    if(len(set(lista))==1) :
        return lista[0] if lista[0]!=Joc.GOL else False
    return False


# def afis_daca_final(stare_curenta):
#     final=stare_curenta.tabla_joc.final()
#     if(final):
#         if (final=="remiza"):
#             print("Remiza!")
#         else:
#             print("A castigat "+final)
            
#         return True
        
#     return False

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
        top=120, 
        left=30, 
        listaButoane=[
            Buton(display=display, w=35, h=30, text="alb", valoare="alb"), 
            Buton(display=display, w=35, h=30, text="negru", valoare="negru")
            ], 
        indiceSelectat=0)
    btn_dificultate = GrupButoane(
        top=70, 
        left=30, 
        listaButoane=[
            Buton(display=display, w=50, h=30, text="easy", valoare=2), 
            Buton(display=display, w=50, h=30, text="medium", valoare=3),
            Buton(display=display, w=50, h=30, text="hard", valoare=4)
            ], 
        indiceSelectat=0)
    ok=Buton(display=display, top=170, left=30, w=40, h=30, text="ok", culoareFundal=(155,0,55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_dificultate.deseneaza()
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
                        if not btn_dificultate.selecteazaDupacoord(pos):
                            if ok.selecteazaDupacoord(pos):
                                display.fill((0,0,0)) #stergere ecran 
                                tabla_curenta.deseneaza_grid()
                                return btn_juc.getValoare(), btn_alg.getValoare(), btn_dificultate.getValoare()
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
    Joc.JMIN, tip_algoritm, ADANCIME_MAX = deseneaza_alegeri(ecran,joc_curent)
    
    if Joc.JMIN == "alb":
        turn = 0
        Joc.JMAX = "negru"
    elif Joc.JMIN == "negru":
        turn = 1
        Joc.JMAX = "alb"

    ecran.fill((255,255,255))
    pygame.display.update()	    
    
    stare_curenta = Stare(joc_curent, Joc.JMIN, ADANCIME_MAX) # stare intiala 

    joc_curent.deseneaza_grid()
    ok = False
    pygame.display.update()	
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                Stare.afiseaza_stats()
                pygame.quit()
                sys.exit()
            if stare_curenta.j_curent == Joc.JMIN: # randul userului 
                if ok == False:
                    t_inainte=time.time()
                    ok = True
                    print(f"Muta {Joc.JMIN}")
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for nod in joc_curent.coordonateNoduri:
                        if (distEuclid(*pos, *nod) < joc_curent.razaPct):
                            nod_curent = Piesa(nod[0], nod[1])
                            if not joc_curent.piesa_selectata and joc_curent.piesa_valida(turn, nod_curent):
                                joc_curent.piesa_selectata = nod_curent
                                joc_curent.deseneaza_grid()

                            elif joc_curent.piesa_selectata and joc_curent.mutare_valida(turn, nod_curent):
                                piese_albe = copy.deepcopy(joc_curent.piese_albe)
                                piese_negre = copy.deepcopy(joc_curent.piese_negre)

                                joc_nou = Joc(piese_albe, piese_negre)
                                stare_curenta = Stare(joc_nou, Joc.JMAX, ADANCIME_MAX)
                                joc_nou.deseneaza_grid()
                                t_dupa=time.time()
                                print(f"Timp mutare {t_dupa - t_inainte} secunde")

                            elif joc_curent.piesa_selectata:
                                if Joc.JMIN == "alb":
                                    piese_selectate = joc_curent.piese_albe
                                else :
                                    piese_selectate = joc_curent.piese_negre
                                if nod_curent in piese_selectate:
                                    joc_curent.piesa_selectata = nod_curent
                                    joc_curent.deseneaza_grid()

            else: # randul ai ului
                print(f"Muta {Joc.JMAX}")
                ok = False
                t_inainte=int(round(time.time() * 1000))
                if tip_algoritm == "minimax":
                    stare_noua = min_max(stare_curenta)
                elif tip_algoritm == "alphabeta":
                    stare_noua = alpha_beta(-500, 500, stare_curenta)

                stare_curenta = copy.deepcopy(stare_noua.stare_aleasa)

                t_dupa=int(round(time.time() * 1000))
                Stare.timpi_gandire.append(t_dupa - t_inainte)
                print("Calculatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
                print("Scorul mutarii " + str(stare_curenta.scor))

                print("noduri generate " + str(Stare.total_noduri_generate) )
                Stare.numar_noduri_generate.append(Stare.total_noduri_generate)
                Stare.total_noduri_generate = 0

                stare_curenta.tabla_joc.deseneaza_grid()
                stare_curenta.adancime = ADANCIME_MAX
                joc_curent = stare_curenta.tabla_joc

            # verific daca sunt intr-o stare finala     
            final = stare_curenta.tabla_joc.final()
            if final:
                if ok == False:
                    print("A castigat " + final)
                    ok = True
                stare_curenta.tabla_joc.marcheaza_castigator(final)
                Stare.afiseaza_stats()
                event = pygame.event.wait()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pass    
                    else:
                        pygame.quit()
                        sys.exit()                 
                        
if __name__ == "__main__" :
    main()


    