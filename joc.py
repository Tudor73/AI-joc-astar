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
    scor_maxim=500
    razaPiesa=20
    width = 400
    height = 700
    culoare_ecran = (255,255,255)
    def __init__(self, piese_albe = None, piese_negre = None):
        #creez proprietatea ultima_mutare # (l,c)
        self.ultima_mutare=None
        self.scalare=60
        self.translatie=30
        self.razaPct=10
        self.piesa_selectata = False
        self.coordonateNoduri=[[self.translatie + self.scalare * x for x in nod] for nod in self.noduri]
        self.piese_albe = piese_albe
        self.piese_negre = piese_negre
        if self.piese_negre == None:
            self.piese_negre = [Piesa(*self.coordonateNoduri[i]) for i in range(13)]
            for i in range(14,17):
                self.piese_negre.append(Piesa(*self.coordonateNoduri[i]))
            print(self.piese_negre)
        if self.piese_albe == None:
            # self.piese_albe = [Piesa(*self.coordonateNoduri[i]) for i in range(33, len(self.__class__.noduri))]
            self.piese_albe = [Piesa(*self.coordonateNoduri[i]) for i in range(33, 34)]
            # for i in range(29,32):
            for i in range(29,30):
                self.piese_albe.append(Piesa(*self.coordonateNoduri[i]))
            print(self.piese_albe)
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

    def gaseste_piesa(self, nod):
        """cauta piesa de culoare opusa pe coloana sau pe linia piesei curente

        Args:
            Nod: din coordonate noduri 

        Returns:
            piesa gasita sau False
        """
        nod_nou = copy.deepcopy(self.piesa_selectata)
        if self.piesa_selectata.x == nod.x:
            y_dif = self.piesa_selectata.y - nod.y
            nod_nou.y -= y_dif//2
            return nod_nou
        elif self.piesa_selectata.y == nod.y:
            x_dif = self.piesa_selectata.x - nod.x
            nod_nou.x -= x_dif//2
            return nod_nou
        return False

    def mutare_valida(self, turn, nod):
        """functia care verifica daca mutarea userului este valida sau nu 
            (daca muta, captureaza sau selecteaza alta piesa )
        Args:
            turn : spune functiei cu ce piese joaca userul 
            nod : nodul pe care user ul a dat click 

        Returns:
            boolean : daca mutarea este valida sau nu 
        """
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
                nod_nou = self.gaseste_piesa(nod)
                captura, mutare = self.check_for_capture(self.piesa_selectata, nod_nou)
                if captura:
                    self.piese_albe.remove(self.piesa_selectata)
                    self.piese_negre.remove(captura)
                    self.piese_albe.append(mutare)
                    self.piese_totale = self.piese_albe + self.piese_negre
                    return True
                return False
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
                nod_nou = self.gaseste_piesa(nod)
                captura, mutare = self.check_for_capture(self.piesa_selectata, nod_nou)
                if captura:
                    self.piese_negre.remove(self.piesa_selectata)
                    self.piese_albe.remove(captura)
                    self.piese_negre.append(mutare)
                    self.piese_totale = self.piese_albe + self.piese_negre
                    return True
                return False
            else:
                self.piese_negre.remove(self.piesa_selectata)
                self.piese_negre.append(nod)
                self.piese_totale = self.piese_albe + self.piese_negre
            return True
            
    def check_for_capture(self, piesa_curenta, piesa_noua):
        """verific daca piesa noua poate fi capturata si returnez piesa capturata sinoul loc al piesei curente

        Args:
            piesa_curenta Piesa: _description_
            piesa_noua Piesa: _description_

        Returns:
            piesa capturata si noul loc al piesei curente sau false/ false
        """
        if not piesa_noua or piesa_noua not in self.piese_totale:
            return False, False
        nod_aux1 = copy.deepcopy(piesa_noua)
        nod_aux2 = copy.deepcopy(piesa_noua)
        if piesa_curenta.x == piesa_noua.x:
                nod_aux1.y = nod_aux1.y-60
                nod_aux2.y = nod_aux2.y+60
        elif piesa_curenta.y == piesa_noua.y:
                nod_aux1.x = nod_aux1.x + 60
                nod_aux2.x = nod_aux2.x - 60
        if nod_aux1 not in self.piese_totale and [nod_aux1.x, nod_aux1.y] in self.coordonateNoduri:
            return piesa_noua, nod_aux1 
        elif nod_aux2 not in self.piese_totale and [nod_aux2.x, nod_aux2.y] in self.coordonateNoduri:
            return piesa_noua, nod_aux2 
        return False, False
            
    def mutari(self, jucator):
        """
        genereaza mutarile ai ului 

        Args:
            jucator : jucatorul curent

        Returns:
            lista de configuratii posibile ale jocului 
        """
        l_mutari = []
        if jucator == "alb":
            piese_selectate = self.piese_albe
        else:
            piese_selectate = self.piese_negre

        for piesa in piese_selectate:
            captura_posibila, mutari = self.check_for_mutari(piesa, piese_selectate)
            if captura_posibila == False:
                for mutare in mutari: 
                    copie_albe = copy.deepcopy(self.piese_albe)
                    copie_negre = copy.deepcopy(self.piese_negre)
                    if jucator == "alb":
                        copie_albe.remove(piesa)
                        copie_albe.append(mutare)
                    else:
                        copie_negre.remove(piesa)
                        copie_negre.append(mutare)

                    new_joc = Joc(copie_albe, copie_negre)
                    l_mutari.append(new_joc)
            else: 
                captura, mutare = mutari
                copie_albe = copy.deepcopy(self.piese_albe)
                copie_negre = copy.deepcopy(self.piese_negre)
                if jucator == "alb":
                    copie_albe.remove(piesa)
                    copie_albe.append(mutare)
                    copie_negre.remove(captura)
                else:
                    copie_negre.remove(piesa)
                    copie_negre.append(mutare)
                    copie_albe.remove(captura)
                new_joc = Joc(copie_albe, copie_negre)
                l_mutari = []
                l_mutari.append(new_joc)
        return l_mutari

    def check_for_mutari(self, piesa, piese_selectate):
        """functia verifica pentru o piesa daca are mutare sau captura in toate cele 4 directii posbile 

        Args:
            piesa : piesa curenta 
            piese_selectate : piesele ai ului 

        Returns:
            boolean : daca a capturat sau nu
            mutari_valide : lista de mutari valide 
        """

        # edge case uri 
        if piesa == Piesa(90, 510) or piesa == Piesa(210, 510): 
            directions = [[60,0], [0,60], [-60, 0]]
        elif piesa == Piesa(90, 90) or piesa == Piesa(210, 90):
            directions = [[60,0],[-60, 0], [0,-60]] 
        else:
            directions = [[60,0], [0,60], [-60, 0], [0,-60]]

        mutari_valide = []
        captura = False
        for dir in directions:
            new_piesa = Piesa(piesa.x + dir[0], piesa.y + dir[1])
            if [new_piesa.x, new_piesa.y] in self.coordonateNoduri:
                if new_piesa not in self.piese_totale:
                    mutari_valide.append(new_piesa)
                elif new_piesa not in piese_selectate:
                    captura, mutare = self.check_for_capture(piesa, new_piesa)
                    if captura:
                        lista = [captura, mutare]
                        return True, lista
        return False, mutari_valide
            
    def __repr__(self) -> str:
        return f"PIESE ALBE: {self.piese_albe}\n PIESE NEGRE: {self.piese_negre}"

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

    def numar_piese(self, jucator):
        if jucator == "alb":
            return len(self.piese_albe)
        else:
            return len(self.piese_negre)

    def estimeaza_scor(self, adancime):
        """estimeaza scorul dupa numarul de piese ale ambilor jucatori 

        Args:
            adancime (_type_): _description_

        Returns:
            scorul : diferenta dintre numarul de piese sau +/- infinit daca e stare finala 
        """
        t_final=self.final()
        #if (adancime==0):
        if t_final==self.__class__.JMAX :
            return (self.__class__.scor_maxim+adancime)
        elif t_final==self.__class__.JMIN:
            return (-self.__class__.scor_maxim-adancime)
        elif t_final=='remiza':
            return 0
        else: 
            return self.numar_piese(self.__class__.JMAX) - self.numar_piese(self.__class__.JMIN)        

    def estimeaza_scor2(self, adancime, stare):
        """estimeaza scorul dupa numarul de capturari posbilie din starea curenta
            returneaza nnumarul de capturari pentur JMAX sau -numarul de capturari pentru JMIN
        """
        t_final=self.final()
        #if (adancime==0):
        if t_final==self.__class__.JMAX :
            return (self.__class__.scor_maxim+adancime)
        elif t_final==self.__class__.JMIN:
            return (-self.__class__.scor_maxim-adancime)
        elif t_final=='remiza':
            return 0
        for mutare in stare.mutari_posibile:
            piese_selectate = []
            numar_capturari = 0
            if mutare.j_curent == "alb":
                piese_selectate = mutare.tabla_joc.piese_albe
            else:
                piese_selectate = mutare.tabla_joc.piese_negre
            for piesa in piese_selectate:
                if self.check_for_capture(piesa, Piesa(piesa.x + 60, piesa.y)):
                   numar_capturari += 1
                if self.check_for_capture(piesa, Piesa(piesa.x - 60, piesa.y)):
                   numar_capturari += 1
                if self.check_for_capture(piesa, Piesa(piesa.x, piesa.y + 60)):
                   numar_capturari += 1
                if self.check_for_capture(piesa, Piesa(piesa.x, piesa.y) - 60):
                   numar_capturari += 1
        if mutare.j_curent == Joc.JMAX:
            return numar_capturari
        else:
            return -numar_capturari



    def final(self):
        """ 
        verifica daca starea este finala 
        """
        rez = False
        if self.piese_albe == []:
            rez = "negru"
        elif self.piese_negre == []:
            rez = "alb"
        return rez
                
    def marcheaza_castigator(self, castigator):
        if castigator == "negru":
            piese_selectate = self.piese_negre
        else:
            piese_selectate = self.piese_albe

        for piesa in piese_selectate:
            piesa.deseneaza_piesa(self.__class__.display, self.__class__.piesa_selectata)
        pygame.display.update()
