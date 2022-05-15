from statistics import median
from joc import Joc

class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """
    numar_noduri_generate = []
    total_noduri_generate = 0
    timpi_gandire = []
    def __init__(self, tabla_joc : Joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc=tabla_joc
        self.j_curent=j_curent
        
        #adancimea in arborele de stari
        self.adancime=adancime	
        
        #scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor=scor
        
        #lista de mutari posibile din starea curenta
        self.mutari_posibile=[]
        
        #cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa=None



    def mutari(self):		
        l_mutari=self.tabla_joc.mutari(self.j_curent)
        juc_opus=Joc.jucator_opus(self.j_curent)
        l_stari_mutari=[Stare(mutare, juc_opus, self.adancime-1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari
        
    
    def __str__(self):
        sir= str(self.tabla_joc) + "(Juc curent:"+self.j_curent+")\n"
        return sir	
    def __repr__(self):
        sir= str(self.tabla_joc) + "(Juc curent:"+self.j_curent+")\n"
        return sir
    
    @classmethod
    def afiseaza_stats(cls):
        print("TIMP:")
        cls.timpi_gandire.sort()
        timp_mediu = sum(cls.timpi_gandire)/len(cls.timpi_gandire)
        print(f"Maxim: {cls.timpi_gandire[-1]} milisecunde")
        print(f"Minim: {cls.timpi_gandire[0]} milisecunde")
        print(f"Mediu: {timp_mediu} milisecunde")
        print(f"Median: {median(cls.timpi_gandire)} milisecunde")

        print("NUMAR NODURI:")
        cls.numar_noduri_generate.sort()
        numar_mediu = sum(cls.numar_noduri_generate)/len(cls.numar_noduri_generate)
        print(f"Maxim: {cls.numar_noduri_generate[-1]}")
        print(f"Minim: {cls.numar_noduri_generate[0]}")
        print(f"Mediu: {numar_mediu}")
        print(f"Median: {median(cls.numar_noduri_generate)}")
            
""" Algoritmul MinMax """

def min_max(stare : Stare) -> Stare:
    
    if stare.adancime==0 or stare.tabla_joc.final() :
        stare.scor=stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare
        
    #calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile=stare.mutari()
    Stare.total_noduri_generate += len(stare.mutari_posibile)
    #aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor=[min_max(mutare) for mutare in stare.mutari_posibile]
    
    

    if stare.j_curent==Joc.JMAX :
        #daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa=max(mutari_scor, key=lambda x: x.scor)
    else:
        #daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa=min(mutari_scor, key=lambda x: x.scor)
    stare.scor=stare.stare_aleasa.scor
    return stare
    

def alpha_beta(alpha, beta, stare):
    if stare.adancime==0 or stare.tabla_joc.final() :
        stare.scor=stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare
    
    if alpha>beta:
        return stare #este intr-un interval invalid deci nu o mai procesez
    
    stare.mutari_posibile=stare.mutari()
    Stare.total_noduri_generate += len(stare.mutari_posibile)


    if stare.j_curent==Joc.JMAX :
        scor_curent=float('-inf')
        
        for mutare in stare.mutari_posibile:
            #calculeaza scorul
            stare_noua=alpha_beta(alpha, beta, mutare)
            
            if (scor_curent<stare_noua.scor):
                stare.stare_aleasa=stare_noua
                scor_curent=stare_noua.scor
            if(alpha<stare_noua.scor):
                alpha=stare_noua.scor
                if alpha>=beta:
                    break

    elif stare.j_curent==Joc.JMIN :
        scor_curent=float('inf')
        
        for mutare in stare.mutari_posibile:
            stare_noua=alpha_beta(alpha, beta, mutare)
            
            if (scor_curent>stare_noua.scor):
                stare.stare_aleasa=stare_noua
                scor_curent=stare_noua.scor

            if(beta>stare_noua.scor):
                beta=stare_noua.scor
                if alpha>=beta:
                    break
    stare.scor=stare.stare_aleasa.scor

    return stare
    
