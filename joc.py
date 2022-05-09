import pygame
import copy
import math 
import os

from piesa import Piesa

def distEuclid(x0,y0,x1,y1):
    return math.sqrt((x0-x1)**2+(y0-y1)**2)


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    noduri=[(0,0),(1,0),(2,0),(3,0),(4,0),(1,1),(2,1),(3,1),(0,2),
        (1,2),(2,2),(3,2),(4,2), (0,3),(1,3),(2,3),(3,3),(4,3),(0,4),(1,4),(2,4),(3,4),(4,4),
        (0,5),(1,5),(2,5),(3,5),(4,5),(0,6),(1,6),(2,6),(3,6),(4,6),
        (0,7), (1,7),(2,7),(3,7),(4,7),(1,8),(2,8),(3,8),(0,9),(1,9),(2,9),(3,9),(4,9)
    ]
    muchii=[(0,1), (1,2), (2,3), (3,4),(0,5), (1,5), (5,6) ,(2,6),(6,7),(3,7), (4,7),(5,10), (6,10),(7,10),
    (8,9), (8,13), (9,10), (9,14), (10, 11), (10, 15), (11, 12), (11, 16), (12,17),
    (13, 14), (13, 18), (14, 15), (14, 19), (15,16), (15, 20), (16, 17), (16, 21), (17, 22),
    (18, 19), (18, 23), (19, 20), (19, 24), (20, 21), (20, 25), (21, 22), (21, 26) ,(22, 27),
    (23, 24), (23, 28), (24, 25), (24, 29), (25, 26), (25, 30), (26,27), (26, 31), (27, 32),
    (28,29), (28, 33), (29,30), (29,34), (30, 31), (30, 35), (31, 32), (31, 36), (32, 37),
    (33,34), (34,35), (35, 36), (36, 37),
    (35,38), (35,39), (35,40), (38,39),(39, 40), (41,38), (41, 42), (42,38), (42,43), (43,39), 
    (43,44),(44,40), (44,45), (45,40)
    ]
    JMIN=None
    JMAX=None
    scor_maxim=0
    razaPiesa=20
    culoare_ecran = (255,255,255)
    def __init__(self,  width, height, matr=None, NR_LINII=None, NR_COLOANE=None):
        #creez proprietatea ultima_mutare # (l,c)
        self.ultima_mutare=None
        self.width = width
        self.height = height
        self.scalare=60
        self.translatie=30
        self.razaPct=10
        self.piesa_selectata = False
        self.coordonateNoduri=[[self.translatie + self.scalare * x for x in nod] for nod in self.noduri]
        self.piese_negre = [Piesa(*self.coordonateNoduri[i]) for i in range(13)]
        for i in range(14,17):
            self.piese_negre.append(Piesa(*self.coordonateNoduri[i]))

        self.piese_albe = [Piesa(*self.coordonateNoduri[i]) for i in range(33, len(self.__class__.noduri))]
        for i in range(29,32):
            self.piese_albe.append(Piesa(*self.coordonateNoduri[i]))
        self.piese_totale = self.piese_albe + self.piese_negre

    def deseneaza_grid(self):
        self.display.fill(self.__class__.culoare_ecran)
        for nod in self.coordonateNoduri:
            pygame.draw.circle(surface=self.__class__.display, color=(0,0,0), center=nod, radius=self.razaPct,width=0) #width=0 face un cerc plin
        for muchie in self.__class__.muchii:
            p0=self.coordonateNoduri[muchie[0]]
            p1=self.coordonateNoduri[muchie[1]]
            pygame.draw.line(surface=self.__class__.display,color=(0,0,0),start_pos=p0,end_pos=p1,width=5)

        for piesa in self.piese_negre:
            piesa.deseneaza_piesa(self.__class__.display, self.__class__.piesa_neagra)
        for piesa in self.piese_albe:
            piesa.deseneaza_piesa(self.__class__.display, self.__class__.piesa_alba)
        if self.piesa_selectata:
            self.piesa_selectata.deseneaza_piesa(self.__class__.display, self.__class__.piesa_selectata)
        pygame.display.update()


    def piesa_valida(self,turn, nod):
        if turn == 0 and nod in self.piese_albe:
            return True
        elif turn == 1 and nod in self.piese_negre:
            return True
        return False

    def mutare_valida(self, turn, nod):
        if distEuclid(self.piesa_selectata.x, self.piesa_selectata.y, nod.x, nod.y)  != 60 and distEuclid(self.piesa_selectata.x, self.piesa_selectata.y, nod.x, nod.y)   != 120 :
            return False


        if nod == self.piesa_selectata:
            self.piesa_selectata = False
            return False

        if turn == 0:
            if nod in self.piese_albe:
                self.piesa_selectata = nod
                return False
            if distEuclid(self.piesa_selectata.x, self.piesa_selectata.y, nod.x, nod.y)  == 120:
                nod_aux1 = copy.deepcopy(nod)
                nod_aux2 = copy.deepcopy(nod)
                if self.piesa_selectata.x == nod.x:
                    nod_aux1.y = nod_aux1.y-60
                    nod_aux2.y = nod_aux2.y+60
                elif self.piesa_selectata.y == nod.y:
                    nod_aux1.x = nod_aux1.x + 60
                    nod_aux2.x = nod_aux2.x - 60
                return self.check_for_capture(nod, nod_aux1) or self.check_for_capture(nod, nod_aux2)
            else:
                self.piese_albe.remove(self.piesa_selectata)
                self.piese_albe.append(nod)
                self.piese_totale = self.piese_albe + self.piese_negre
            return True
        elif turn == 1:
            if nod in self.piese_negre:
                self.piesa_selectata = nod
                return False
            if distEuclid(self.piesa_selectata.x, self.piesa_selectata.y, nod.x, nod.y)   == 120:
                nod_aux1 = copy.deepcopy(nod)
                nod_aux2 = copy.deepcopy(nod)
                if self.piesa_selectata.x == nod.x:
                    nod_aux1.y = nod_aux1.y-60
                    nod_aux2.y = nod_aux2.y+60
                elif self.piesa_selectata.y == nod.y:
                    nod_aux1.x = nod_aux1.x + 60
                    nod_aux2.x = nod_aux2.x - 60


                return self.check_for_capture(nod, nod_aux1) or self.check_for_capture(nod, nod_aux2)
            else:
                self.piese_negre.remove(self.piesa_selectata)
                self.piese_negre.append(nod)
                self.piese_totale = self.piese_albe + self.piese_negre
            return True


    def check_for_capture(self, nod_curent, nod_aux):
        if self.piesa_selectata in self.piese_albe and nod_aux in self.piese_negre:
            self.piese_albe.remove(self.piesa_selectata)
            self.piese_negre.remove(nod_aux)
            self.piesa_selectata = nod_curent
            self.piese_albe.append(self.piesa_selectata)
            self.piese_totale = self.piese_albe + self.piese_negre
            return True
        elif self.piesa_selectata in self.piese_negre and nod_aux in self.piese_albe:
            self.piese_negre.remove(self.piesa_selectata)
            self.piese_albe.remove(nod_aux)
            self.piesa_selectata = nod_curent
            self.piese_negre.append(self.piesa_selectata)
            self.piese_totale = self.piese_albe + self.piese_negre

            return True
        return False
            


    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator==cls.JMIN else cls.JMIN


    @classmethod
    def initializeaza(cls, display):
        cls.display=display
        cls.diametru_piesa = 2 * cls.razaPiesa
        cls.piesa_alba = pygame.image.load(os.path.join("images", 'alb.png'))
        cls.piesa_alba = pygame.transform.scale(cls.piesa_alba, (cls.diametru_piesa,cls.diametru_piesa))

        cls.piesa_neagra = pygame.image.load(os.path.join("images", 'negru.png'))
        cls.piesa_neagra = pygame.transform.scale(cls.piesa_neagra, (cls.diametru_piesa,cls.diametru_piesa))

        cls.piesa_selectata = pygame.image.load(os.path.join("images", 'rosu.png'))
        cls.piesa_selectata = pygame.transform.scale(cls.piesa_selectata, (cls.diametru_piesa,cls.diametru_piesa))

    def parcurgere(self, directie):
        um = self.ultima_mutare # (l,c)
        culoare = self.matr[um[0]][um[1]]
        nr_mutari = 0
        while True:
            um = (um[0] + directie[0], um[1] + directie[1])
            if not 0 <= um[0] < self.__class__.NR_LINII or not 0 <= um[1] < self.__class__.NR_COLOANE:
                break
            if not self.matr[um[0]][um[1]] == culoare:
                break
            nr_mutari += 1
        return nr_mutari
        
    def final(self):
        if not self.ultima_mutare: #daca e inainte de prima mutare
            return False
        directii = [[(0, 1), (0, -1)], [(1, 1), (-1, -1)], [(1, -1), (-1, 1)], [(1, 0), (-1, 0)]]
        um = self.ultima_mutare
        rez = False
        for per_dir in directii:
            len_culoare = self.parcurgere(per_dir[0]) + self.parcurgere(per_dir[1]) + 1 # +1 pt chiar ultima mutare
            if len_culoare >= 4:
                rez = self.matr[um[0]][um[1]]
     
        if(rez):
            return rez
        elif all(self.__class__.GOL not in x for x in self.matr):
            return 'remiza'
        else:
            return False

    def mutari(self, jucator):
        l_mutari=[]
        for j in range(self.__class__.NR_COLOANE):
            last_poz = None
            if self.matr[0][j] != self.__class__.GOL:
                continue
            for i in range(self.__class__.NR_LINII):
                if self.matr[i][j]!=self.__class__.GOL:
                        last_poz = (i-1,j)
                        break			 
            if last_poz is None:
                last_poz = (self.__class__.NR_LINII-1, j)
            matr_tabla_noua = copy.deepcopy(self.matr)
            matr_tabla_noua[last_poz[0]][last_poz[1]] = jucator
            jn=Joc(matr_tabla_noua)
            jn.ultima_mutare=(last_poz[0],last_poz[1])
            l_mutari.append(jn)
        return l_mutari


    #linie deschisa inseamna linie pe care jucatorul mai poate forma o configuratie castigatoare
    #practic e o linie fara simboluri ale jucatorului opus
    def linie_deschisa(self,lista, jucator):
        jo=self.jucator_opus(jucator)
        #verific daca pe linia data nu am simbolul jucatorului opus
        if not jo in lista:
                #return 1
                return lista.count(jucator)
        return 0
        
    def estimeaza_scor(self, adancime):
        t_final=self.final()
        #if (adancime==0):
        if t_final==self.__class__.JMAX :
            return (self.__class__.scor_maxim+adancime)
        elif t_final==self.__class__.JMIN:
            return (-self.__class__.scor_maxim-adancime)
        elif t_final=='remiza':
            return 0
        else:
            return (self.linii_deschise(self.__class__.JMAX)- self.linii_deschise(self.__class__.JMIN))
                
            
