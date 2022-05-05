import pygame 
class Buton:
	def __init__(self, display=None, left=0, top=0, w=0, h=0,culoareFundal=(53,80,115), culoareFundalSel=(89,134,194), text="", font="arial", fontDimensiune=16, culoareText=(255,255,255), valoare=""):
		self.display=display		
		self.culoareFundal=culoareFundal
		self.culoareFundalSel=culoareFundalSel
		self.text=text
		self.font=font
		self.w=w
		self.h=h
		self.selectat=False
		self.fontDimensiune=fontDimensiune
		self.culoareText=culoareText
		#creez obiectul font
		fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
		self.textRandat=fontObj.render(self.text, True , self.culoareText) 
		self.dreptunghi=pygame.Rect(left, top, w, h) 
		#aici centram textul
		self.dreptunghiText=self.textRandat.get_rect(center=self.dreptunghi.center)
		self.valoare=valoare

	def selecteaza(self,sel):
		self.selectat=sel
		self.deseneaza()
		
	def selecteazaDupacoord(self,coord):
		if self.dreptunghi.collidepoint(coord):
			self.selecteaza(True)
			return True
		return False

	def updateDreptunghi(self):
		self.dreptunghi.left=self.left
		self.dreptunghi.top=self.top
		self.dreptunghiText=self.textRandat.get_rect(center=self.dreptunghi.center)

	def deseneaza(self):
		culoareF= self.culoareFundalSel if self.selectat else self.culoareFundal
		pygame.draw.rect(self.display, culoareF, self.dreptunghi)	
		self.display.blit(self.textRandat ,self.dreptunghiText) 


class GrupButoane:
	def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10,left=0, top=0):
		self.listaButoane=listaButoane
		self.indiceSelectat=indiceSelectat
		self.listaButoane[self.indiceSelectat].selectat=True
		self.top=top
		self.left=left
		leftCurent=self.left
		for b in self.listaButoane:
			b.top=self.top
			b.left=leftCurent
			b.updateDreptunghi()
			leftCurent+=(spatiuButoane+b.w)

	def selecteazaDupacoord(self,coord):
		for ib,b in enumerate(self.listaButoane):
			if b.selecteazaDupacoord(coord):
				self.listaButoane[self.indiceSelectat].selecteaza(False)
				self.indiceSelectat=ib
				return True
		return False

	def deseneaza(self):
		#atentie, nu face wrap
		for b in self.listaButoane:
			b.deseneaza()

	def getValoare(self):
		return self.listaButoane[self.indiceSelectat].valoare

