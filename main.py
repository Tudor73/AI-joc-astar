import time
import copy
import os
import pygame
import sys
from joc import Joc
from butoane import Buton, GrupButoane
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
    nl=10
    nc=7
    WIDTH, HEIGHT = 400, 700
    w=50
    ecran=pygame.display.set_mode((WIDTH, HEIGHT))# N *w+ N-1= N*(w+1)-1
    Joc.initializeaza(ecran, NR_LINII=5, NR_COLOANE=4, dim_celula=70)

    #initializare tabla
    tabla_curenta=Joc(WIDTH, HEIGHT,NR_LINII=4,NR_COLOANE=5, )
    Joc.JMIN, tip_algoritm = deseneaza_alegeri(ecran,tabla_curenta)
    print(Joc.JMIN, tip_algoritm)
    ecran.fill((255,255,255))

    

    pygame.display.update()	

    Joc.JMAX= '0' if Joc.JMIN == 'x' else 'x'
    
    

    print("Tabla initiala")
    print(str(tabla_curenta))
    
    # #creare stare initiala
    # stare_curenta=Stare(tabla_curenta,'x',ADANCIME_MAX)

    tabla_curenta.deseneaza_grid2()
    pygame.display.update()	

    # while True :

    # 	if (stare_curenta.j_curent==Joc.JMIN):
            
    # 		for event in pygame.event.get():
    # 			if event.type== pygame.QUIT:
    # 				#iesim din program
    # 				pygame.quit()
    # 				sys.exit()
    # 			if event.type == pygame.MOUSEMOTION:
                    
    # 				pos = pygame.mouse.get_pos()#coordonatele cursorului
    # 				for np in range(len(Joc.celuleGrid)):						
    # 					if Joc.celuleGrid[np].collidepoint(pos):
                            
    # 							stare_curenta.tabla_joc.deseneaza_grid(coloana_marcaj=np%Joc.NR_COLOANE)
    # 							break

    # 			elif event.type == pygame.MOUSEBUTTONDOWN:
                    
    # 				pos = pygame.mouse.get_pos()#coordonatele cursorului la momentul clickului
                    
    # 				for np in range(len(Joc.celuleGrid)):
                        
    # 					if Joc.celuleGrid[np].collidepoint(pos):
    # 						#linie=np//Joc.NR_COLOANE
    # 						coloana=np%Joc.NR_COLOANE
    # 						###############################
                            
    # 						if stare_curenta.tabla_joc.matr[0][coloana] == Joc.GOL:	
    # 							niv=0
    # 							while True:
    # 								if niv == Joc.NR_LINII or stare_curenta.tabla_joc.matr[niv][coloana] != Joc.GOL:
    # 									stare_curenta.tabla_joc.matr[niv - 1][coloana] = Joc.JMIN
    # 									stare_curenta.tabla_joc.ultima_mutare=(niv-1, coloana)
    # 									break
    # 								niv += 1
                                
    # 							#afisarea starii jocului in urma mutarii utilizatorului
    # 							print("\nTabla dupa mutarea jucatorului")
    # 							print(str(stare_curenta))
                                
    # 							stare_curenta.tabla_joc.deseneaza_grid(coloana_marcaj=coloana)
    # 							#testez daca jocul a ajuns intr-o stare finala
    # 							#si afisez un mesaj corespunzator in caz ca da
    # 							if (afis_daca_final(stare_curenta)):
    # 								break
                                    
                                    
    # 							#S-a realizat o mutare. Schimb jucatorul cu cel opus
    # 							stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)


    
    # 	#--------------------------------
    # 	else: #jucatorul e JMAX (calculatorul)
    # 		#Mutare calculator
            
    # 		#preiau timpul in milisecunde de dinainte de mutare
    # 		t_inainte=int(round(time.time() * 1000))
    # 		if tip_algoritm=='minimax':
    # 			stare_actualizata=min_max(stare_curenta)
    # 		else: #tip_algoritm=="alphabeta"
    # 			stare_actualizata=alpha_beta(-500, 500, stare_curenta)
    # 		stare_curenta.tabla_joc=stare_actualizata.stare_aleasa.tabla_joc

    # 		print("Tabla dupa mutarea calculatorului\n"+str(stare_curenta))

    # 		#preiau timpul in milisecunde de dupa mutare
    # 		t_dupa=int(round(time.time() * 1000))
    # 		print("Calculatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
            
    # 		stare_curenta.tabla_joc.deseneaza_grid()
    # 		if (afis_daca_final(stare_curenta)):
    # 			break
                
    # 		#S-a realizat o mutare. Schimb jucatorul cu cel opus
    # 		stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)
    
if __name__ == "__main__" :
    main()
    while True :
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()


    