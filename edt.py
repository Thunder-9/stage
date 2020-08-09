import os
import sys
import math
import sys
import random as rand
from copy import deepcopy
import copy
from threading import Thread
from multiprocessing import Process, Queue, Array
import dill

#from operator import itemgetter, attrgetter

class Etudiant:
	def __init__(self,ide,St_Origin,St_Dest,bus):
		self.id=ide
		self.St_Origin=St_Origin
		self.St_Dest=St_Dest
		self.cours=[]
		self.bus=bus
		self.firstbus=[]
		self.lastbus=[]
		self.firstSc=[]
		self.lastSc=[]
		for i in range (0,5):
			self.firstSc.append(None)
			self.lastSc.append(None)
			self.firstbus.append(None)
			self.lastbus.append(None)

	def sortSC(self):
		self.cours.sort(key= lambda sc: sc.period)	

	# def FindFirstAndLastSeances(self): #sortSC before use 
	# 	global Tmax
	# 	#self.sortSC()
	# 	i=0
	# 	self.firstSc.append(self.cours[0])
	# 	for j in range(0,len(Tmax)-1):
	# 		while(self.cours[i].period < Tmax[j]):
	# 			i=i+1
	# 		self.lastSc.append(self.cours[i-1])
	# 		self.firstSc.append(self.cours[i])
	# 	self.lastSC.append(cours[-1])


	def findBus(self,sh,t,iSctmax):
		global busAller
		global busRetour

		if sh==0:
			for i in range(0,len(busAller)-1):
				if(busAller[i].endTime < t and busAller[i+1].endTime>=t and busAller[i].itmax==iSctmax):
					#self.firstbus[iSctmax]=i
					return i
			if(busAller[-1].endTime < t and busAller[-1].itmax==iSctmax):
				print("-----here")
				return len(busAller)-1
			for b in busAller: print(b.endTime,b.itmax)

			sys.exit("could not find bus aller for period "+str(t)+ " day:"+str(iSctmax))			

		if sh==1:
			for i in range(0,len(busRetour)):
				if(busRetour[i].endTime > t and busRetour[i].itmax==iSctmax):
					#self.lastbus[iSctmax]=i
					return i
			for b in busRetour: print(b.deb,b.itmax)
			sys.exit("could not find bus retour for period "+str(t)+ " day:"+str(iSctmax))		



	


		#return le tmax de sc et -1 si aucun changment dans la congestion, 0 si sc est un first et 1 si un last 
	def shouldProcess(self,sc,t):
		global Tmax			




		# if len(self.cours)<=1:
		# 	return True
		should=-1
		# global Tmax
		iSctmax=None
		if(t<Tmax[0]):
			iSctmax=0
		else :
			for itmax in range(0,len(Tmax)-1):
				if (t>=Tmax[itmax] and t<Tmax[itmax+1]):
					iSctmax=itmax+1	
					

		if iSctmax is None:
			sys.exit("no Tmax found for seance with period = "+str(sc.period)) 
		if self.firstSc[iSctmax] is None or t<self.firstSc[iSctmax].period:
			#return (0,iSctmax)
			should=0
		if self.lastSc[iSctmax] is None or t>self.lastSc[iSctmax].period:
			if should==0:
				should=2
			else:
				should=1

			#return (1,iSctmax)
		
		return (should,iSctmax) 

		# # for scetu in self.cours:
		# # 	should=True
		# # 	if (scetu.period>=Tmax[iSctmax-1] and scetu.period<=Tmax[iSctmax]):
		# # 		if(scetu.period>sc.period)
		# for i in range(0,len(self.cours)-2):
		# 	if (self.cours[i].period>=Tmax[iSctmax-1] and self.cours[i].period<=Tmax[iSctmax]):
		# 		if self.cours[i].period<sc.period and self.cours[i+1].period>sc.period 
		# 			if  self.cours[i+1].period<Tmax[iSctmax]:
		# 				return -1
		# 			else:
		# 				return True







		# return True


	#def lastSeances(self):

class Prof:
	def __init__(self,ide):
		self.id=ide
		self.cours=[]


class Seance:
	def __init__(self,ide,duration):
		self.id=ide
		self.etudiants=[]
		self.ngh=[]
		self.duration = duration
		self.period= -1
		self.salle=None
		#self.bus=None
		self.itmax=None


	

	def __repr__(self):
		return(str(self.id))

	def check_TimeCompatibility(self,Sc_toCheckWith,period):
		if ( (period+self.duration <= Sc_toCheckWith.period)  or (period >= Sc_toCheckWith.period + Sc_toCheckWith.duration) ) :
			return True
		else:
			return False
	

	def check_RoomCompatibility(self,Sa_room,period):
		# if (Sa_room!=Sc_toCheckWith.salle):
		# 	return(True)
		# else:  
		# 	return(False)
		for sc in Sa_room.cours:
			if self.check_TimeCompatibility(sc,period)==False:
				return False
		return True

	def set_Room(self,Sa_room):
		if(Sa_room.capacity<self.etudiants.length()):
			return(False)
		else :
			for Sc in Sa_room.cours:
				if(check_TimeCompatibility(Sc,self.period)==False):
					return False
			self.salle=Sa_room
			return(True)


	
	def check_period(self,period):
		global Tmax 
		#print("period:"+str(period)+" duration:"+str(self.duration))
		for t in Tmax:
			if ((period <= t) and (period + self.duration > t)):
				return False
		for ngh in self.ngh:
			if ngh.period != -1 :
				if self.check_TimeCompatibility(ngh,period)==False:
					return False
		return True
	
	#a refaire avec new check_period et check_roomCompatibility
	def set_period(self,period,salle):
		
		# if(self.check_period(period)==False):
		# 	return(False)
		# else:
		# 	for Sc_ngh in self.ngh:
		# 		if(Sc_ngh.period!=-1):
		# 			if !( self.check_Timecompatibility(Sc_ngh,period) and self.check_RoomCompatibility(Sc_ngh,salle)):
		# 				return (False)
		# 	self.period=period
		# 	return(True)
		salle.cours.append(self)
		self.salle=salle
		self.period=period
		#affecter first et lastsc des etudiants + le tmax


		for etu in self.etudiants:
			if etu.bus:
				print("ok")
				(sh,iSctmax)=etu.shouldProcess(self,period)
				#self.itmax=iSctmax
				if sh==0:
					etu.firstSc[iSctmax]=self
					etu.firstbus[iSctmax]=etu.findBus(sh,period,iSctmax)
					print(etu.firstbus)
					

				if sh==1:
					etu.lastSc[iSctmax]=self
					etu.lastbus[iSctmax]=etu.findBus(sh,period+self.duration,iSctmax)
					print(etu.lastbus)

				if sh==2:
					etu.firstSc[iSctmax]=self
					etu.lastSc[iSctmax]=self
					etu.firstbus[iSctmax]=etu.findBus(0,period,iSctmax)
					etu.lastbus[iSctmax]=etu.findBus(1,period+self.duration,iSctmax)
				print("set " + str(sh))
				print(etu.firstbus)
				print(etu.lastbus)


	def nbAvRoom(self,period):
		global salles
		nb=0
		for sa in salles:
			if sa.capacity>=len(self.etudiants):
				if self.check_RoomCompatibility(sa,period):
					nb+=1

		return nb





class Salle:
	def __init__(self,ide,capacity):
		self.id=ide
		self.capacity=capacity
		self.cours=[]
	
	def __repr__(self):
		return(str(self.id))


class Bus:
	def __init__(self,ide,cap,deb,interStTime,itmax):
		self.id=ide
		self.capacity=cap
		self.deb=deb
		self.passenger=0
		self.interStTime=interStTime
		self.endTime=deb+sum(interStTime)
		self.itmax=itmax





def ListSort():
	global seances
	global salles
	global Bus

	#seances.sort(key=lambda seance : len(seance.ngh)*seance.duration,reverse=True)
	salles.sort(key=lambda salle: salle.capacity)
	bus.sort(key = lambda b : b.deb)






	#for e in etudiants:


def ReadGraph():
	initGraph()
	f=open("graph.data","r")
	f.readline()
	f.readline()
	f.readline()
	line=f.readline()
	global seances
	while (line != ''):
		linetmp=line.split(" ")
		for i in range (1,len(linetmp)):
			seances[int(linetmp[0])].ngh.append(seances[int(linetmp[i])])
			seances[int(linetmp[i])].ngh.append(seances[int(linetmp[0])])
		line=f.readline()
	f.close()

def ReadBus():
	global busAller
	global busRetour
	global Tmax

	f=open("busA.data","r")
 #(self,ide,cap,deb,interStTime,itmax):
	line=f.readline()
	currendBusID=0
	while (line != ''):
		linetmp=line.split(" ")
		linetmp2=linetmp[0].split(":")
		linetmp3=[]
		for time in linetmp[1:]:
			linetmp3.append(int(time))

		busAller.append(Bus(currendBusID,100,int(linetmp2[0])*60-480+int(linetmp2[1]),linetmp3,0))
		for i in range(1,5):
			busAller.append(Bus(currendBusID,100,int(linetmp2[0])*60-480+Tmax[i-1]+int(linetmp2[1]),linetmp3,i)) #-480min == -8h ->8h == t=0
			currendBusID+=1
		line=f.readline()

	f.close()
	f=open("busR.data","r")
	busAller.sort(key=lambda b: b.deb)
 #(self,ide,cap,deb,interStTime,itmax):
	line=f.readline()
	currendBusID=0
	while (line != ''):
		linetmp=line.split(" ")
		linetmp2=linetmp[0].split(":")
		linetmp3=[]
		for time in linetmp[1:]:
			linetmp3.append(int(time))
		
		busRetour.append(Bus(currendBusID,100,int(linetmp2[0])*60-480+int(linetmp2[1]),linetmp3,0))
		for i in range(1,5):
			busRetour.append(Bus(currendBusID,100,int(linetmp2[0])*60-480+Tmax[i-1]+int(linetmp2[1]),linetmp3,i)) #-480min == -8h ->8h == t=0
			currendBusID+=1
		line=f.readline()
	f.close()
	busRetour.sort(key=lambda b: b.deb)


def initGraph():
	global seances
	seq=[60,90,120,180,240]
	for i in range (0,int(sys.argv[1])):
		seances.append(Seance(i,rand.choice(seq)))

def addStudent():
	global seances
	global etudiants
	global salles
	global nbStationA
	global nbStationB
	#rand.seed(10)
	currentEtuId=0
	for se in seances:
		for seNgh in se.ngh:
			for i in range(currentEtuId,currentEtuId+10):
				buschoice=rand.random()
				if (buschoice<=0.5): #0.2
					etudiants.append(Etudiant(i,rand.randint(0,nbStationA-1),rand.randint(0,nbStationB-1),True))
				else:
					etudiants.append(Etudiant(i,None,None,False))
				se.etudiants.append(etudiants[i])
				etudiants[i].cours.append(se)
			#for seNgh in se.ngh:
				seNgh.etudiants.append(etudiants[i])
				etudiants[i].cours.append(seNgh)

			currentEtuId+=10


def addRoom():
	global salles
	global seances


	maxcap= len(max(seances,key=lambda x: len(x.etudiants)).etudiants)
	for i in range(0,5):
		salles.append(Salle(i,maxcap))
	currentSid=5

	for se in seances:
		randcreate=rand.random()
		if(randcreate>0.4):
			salles.append(Salle(currentSid,len(se.etudiants)))
			currentSid+=1
	salles.sort(key=lambda salle: salle.capacity)

	

def addBus():
	global busAller
	global busRetour




def printAdjGraph():
	global seances 
	for i in range (0,len(seances)):
		print(seances[i].ngh)







def nextSeance():
	global seancesToAffect
	global seances
	global salles
	global Tmax
	
	minConstraint=float('inf')
	minSc=None
	minSa=None
	minPeriodList=[]
	for sc in seancesToAffect:
		constraint=0
		# sa=getMincapSalle(sc)
		# 
		# 	for sc2 in seances:
		# 		if sc2 != sc and sc2.period==-1:
		for sa in salles:
			constraintSa=0
			freeperiod=0
			periodList=[]
			#print(Tmax[-1])
			#print(sa.capacity)
			#print(len(sc.etudiants))
			if sa.capacity>=len(sc.etudiants):
				#print("cap ok")
				for t in range(0,Tmax[-1],15):
					if sc.check_period(t):
						#print("check ok, period:"+str(t)+" duration:"+str(sc.duration))
						if sc.check_RoomCompatibility(sa,t):
							#print("room ok")
							freeperiod+=1
							periodList.append(t)
							for sc2 in seancesToAffect:
								if sc2 != sc:
									#print("diff ok")
									if sc2.check_period(t) and sc2.check_RoomCompatibility(sa,t):
										#print("double sc2 check ok")
										constraintSa+=1/float(sc2.nbAvRoom(t))
										#print(minConstraint)
			if freeperiod>0 :
				#print("free period ok")
				#print(minConstraint)
				constrainttmp=constraintSa/float(freeperiod)
				#print(constrainttmp)
				#print(minConstraint)
				if (constrainttmp < minConstraint):
					#print("min found")
					minSc=sc
					#print(sc)
					#print(minSc)
					#sys.exit()
					minSa=sa
					minConstraint=constrainttmp #.copy()
					minPeriodList=periodList.copy()
	if not minSc:
		for sc in seancesToAffect:
			print(str(sc.id)+" nb etudiants : "+str(len(sc.etudiants)))
		sys.exit("les seances precedantes son implassables")
	#print(minSc)
	return(minSc,minSa,minPeriodList)



def nextSeanceThreads():
	global seancesToAffect
	global seances
	global salles
	global Tmax


	# tirage=[i for i in range(0,len(seancesToAffect))]
	# tire=tirage[randint(0,len(seancesToAffect)-1)]


	#results=[None for sc in seancesToAffect]
	results=[]
	#q=[Queue() for sc in seancesToAffect]
	#q=Queue()
	#q=[Queue() for range(0,4) ]
	# p=[None for sc in seancesToAffect]
	# for i in range(0,len(p)):
	# 	p[i]=Process(target=nextSeanceT,args=(q,seancesToAffect,salles,Tmax,i))
	# 	print("Process for seance : "+str(i)+" started")
	pqList=[]
	test=0
	for i in range(0,len(seancesToAffect)):
		qtmp=Queue()
		ptmp=Process(target=nextSeanceT,args=(qtmp,seancesToAffect,salles,Tmax,i))

		if(test<4):
			ptmp.start()
			pqList.append([ptmp,qtmp])
			test+=1
			print("Process for seance : "+str(i)+" with pid : "+str(ptmp.pid)  +" started")
		else:
			t=True
			while(t):
				for pq in pqList:
					if not(pq[0].exitcode is None):
						test-=1
						results.append(pq[1].get())
						pqList.remove(pq)
						print("Process with pid : "+str(pq[0].pid)+" terminated")
						t=False

	for pq in pqList:
		pq[0].join()
		results.append(pq[1].get())

	# for i in range(0,len(p)):
	# 	results[i]=q.get()

		#p[i].close()
		#close(p[i])
		
	print(results)	
		#p[i].close()
		#results[i]=q[i].get()
		#q[i].close()
		#close(p[i])
		# 	print(results[i])
		# sys.exit()
	
	minIndex=results.index(min(results,key=lambda x: x[0]))
	print("index:"+str(minIndex))
	return(seancesToAffect[results[minIndex][3]],salles[results[minIndex][1]],copy.deepcopy(results[minIndex][2]))



def nextSeanceThreadsMC():
	global seancesToAffect
	global seances
	global salles
	global Tmax


	tirage=[i for i in range(0,len(seancesToAffect))]
	pqList=[]
	test=0
	results=[]
	lim=10 if len(seancesToAffect)>10 else len(seancesToAffect)
	for i in range(0,lim):

		# tire=rand.randint(0,len(tirage)-1)
		tire=tirage[rand.randint(0,len(tirage)-1)]
		tirage.remove(tire)
		qtmp=Queue()
		ptmp=Process(target=nextSeanceT,args=(qtmp,seancesToAffect,salles,Tmax,tire))

		if(test<4):
			ptmp.start()
			pqList.append([ptmp,qtmp])
			test+=1
			print("Process for seance : "+str(tire)+" with pid : "+str(ptmp.pid)  +" started")
		else:
			t=True
			while(t):
				for pq in pqList:
					if not(pq[0].exitcode is None):
						test-=1
						results.append(pq[1].get())
						pqList.remove(pq)
						print("Process with pid : "+str(pq[0].pid)+" terminated")
						t=False

	for pq in pqList:
		pq[0].join()
		results.append(pq[1].get())


		
	print(results)	
		#p[i].close()
		#results[i]=q[i].get()
		#q[i].close()
		#close(p[i])
		# 	print(results[i])
		# sys.exit()
	
	minIndex=results.index(min(results,key=lambda x: x[0]))
	print("index:"+str(minIndex))
	

	
	return(seancesToAffect[results[minIndex][3]],salles[results[minIndex][1]],copy.deepcopy(results[minIndex][2]))

	
def nextSeanceT(results,seancesToA,salles,Tmax,Index):
	# global seancesToAffect
	# global seances
	# global salles
	# global Tmax
	
	minConstraint=float('inf')
	minSc=None
	minSa=None
	minPeriodList=[]
	sc=seancesToA[Index]

	constraint=0
	# sa=getMincapSalle(sc)
	# 
	# 	for sc2 in seances:
	# 		if sc2 != sc and sc2.period==-1:
	for sa in salles:
		constraintSa=0
		freeperiod=0
		periodList=[]
		#print(Tmax[-1])
		#print(sa.capacity)
		#print(len(sc.etudiants))
		if sa.capacity>=len(sc.etudiants):
			#print("cap ok")
			for t in range(0,Tmax[-1],15):
				if sc.check_period(t):
					#print("check ok, period:"+str(t)+" duration:"+str(sc.duration))
					if sc.check_RoomCompatibility(sa,t):
						#print("room ok")
						freeperiod+=1
						periodList.append(t)
						for sc2 in seancesToA:
							if sc2 != sc:
								#print("diff ok")
								if sc2.check_period(t) and sc2.check_RoomCompatibility(sa,t):
									#print("double sc2 check ok")
									constraintSa+=1/float(sc2.nbAvRoom(t))
									#print(minConstraint)
		if freeperiod>0 :
			#print("free period ok")
			#print(minConstraint)
			constrainttmp=constraintSa/float(freeperiod)
			#print(constrainttmp)
			#print(minConstraint)
			if (constrainttmp < minConstraint):
				#print("min found")
				minSc=sc
				#print(sc)
				#print(minSc)
				#sys.exit()
				minSa=sa
				minConstraint=constrainttmp #.copy()
				minPeriodList=periodList.copy()
	if not minSc:
		for sc in seancesToAffect:
			print(str(sc.id)+" nb etudiants : "+str(len(sc.etudiants)))
		sys.exit("les seances precedantes son implassables")
	#print(minSc)
	#results[index]=[minConstraint,minSa,minPeriodList]
	#print(results)
	print(" seance:"+str(seancesToAffect.index(sc))  +" periodList")
	print(minPeriodList)
	results.put([minConstraint,salles.index(minSa),minPeriodList,seancesToAffect.index(sc)])
	if results.full():
		sys.exit("Queue is full")





def getMincapSalle(Sc):
	global salles
	for sa in salles:
		if len(Sc.etudiants)>=sa.capacity:
			return sa
	sys.exit('pas de salles disponibles pour le cours'+Sc.id)





def ConstructEdt():
	global seances
	global seancesToAffect 
	global etudiants
	global salles
	global Tmax
	global bus 
	global objA
	global objR
	global MIn
	global MOut
	global MPIn
	global MPOut

	while seancesToAffect:
		print("recherche de la meilleur séance à placer")
		#(sc,sa,periodList)=nextSeance()
		# (sc,sa,periodList)=nextSeanceThreads()
		(sc,sa,periodList)=nextSeanceThreadsMC()
		print("periodList")
		print(periodList)
		print("recherche de la meilleur période pour la seances : "+str(sc.id))
		sc.set_period(Bestperiod(sc,sa,periodList),sa) #a moddifier +++
		print("seance affecté à la période :"+ str(sc.period))
		print("MIn :")
		print(MIn)
		print("MOut :")
		print(MOut)
		print("MPIn :")
		print(MPIn)
		print("MPOut :")
		print(MPOut)
		print("objA :")
		print(objA)
		print("objR :")
		print(objR) 
		seancesToAffect.remove(sc)	
		print("----nb seances "+str(len(seancesToAffect	)))
		





def ProcessCongestion(sc,t):
	global MIn
	global MOut
	global MPIn
	global MPOut
	global objA
	global objR
	global busAller
	global busRetour
	busAllerToReprocess=[]
	busRetourToReprocess=[]
	# MIn=[[]]
	# MOut=[[]]
	# MPIn=[[]]
	# MPOut=[[]]

	MInTmp=copy.deepcopy(MIn)
	MOutTmp=copy.deepcopy(MOut)
	MPInTmp=copy.deepcopy(MPIn)
	MPOutTmp=copy.deepcopy(MPOut)
	obAtmp=copy.deepcopy(objA)
	obRtmp=copy.deepcopy(objR)
	nb=0

	for etu in sc.etudiants:
		if etu.bus:
			(sh,iSctmax)=etu.shouldProcess(sc,t)
			print("ok2 sh:"+str(sh) )

			if sh==0 or sh==2:

				if (not(etu.firstSc[iSctmax] is None)):
					print("not None")
					MInTmp[etu.firstbus[iSctmax]][etu.St_Origin]-=1
					if MInTmp[etu.firstbus[iSctmax]][etu.St_Origin]<0:
						print("----- wtf "+str(t)+" "+str(busAller[etu.firstbus[iSctmax]].endTime))
						print(MInTmp[etu.firstbus[iSctmax]])
						print(busRetour[etu.lastbus[iSctmax]].deb)
						print(busAller[etu.findBus(0,etu.firstSc[iSctmax].period,iSctmax)].endTime)
						print(etu.lastSc[iSctmax].id)
						print("--")
						for s in sc.ngh:
							print (s.id)
						print(sc.check_period(t))
						print("-")
						for s in etu.cours:
							print(s.id)
						sys.exit()
					if etu.firstbus[iSctmax] not in busAllerToReprocess:
						busAllerToReprocess.append(etu.firstbus[iSctmax])
				bustmp=etu.findBus(0,t,iSctmax)
				print(bustmp)
				if bustmp not in busAllerToReprocess:
					busAllerToReprocess.append(bustmp)
				MInTmp[bustmp][etu.St_Origin]+=1

			if sh==1 or sh==2:
				print("processing student")
				if not(etu.lastSc[iSctmax] is None):
					print("not None")
					MPInTmp[etu.lastbus[iSctmax]][0]-=1
					MPOutTmp[etu.lastbus[iSctmax]][etu.St_Dest]-=1
					if etu.lastbus[iSctmax] not in busRetourToReprocess:
						busRetourToReprocess.append(etu.lastbus[iSctmax])
				bustmp=etu.findBus(1,t+sc.duration,iSctmax)
				if bustmp not in busRetourToReprocess:
					busRetourToReprocess.append(bustmp)
				MPOutTmp[bustmp][etu.St_Dest]+=1
				MPInTmp[bustmp][0]+=1
				#print ("bus tmp")
				#print (MPInTmp[bustmp][0])

			

	(obAm,obRm)=CalcObj(busAllerToReprocess,busRetourToReprocess,MInTmp,MOutTmp,MPInTmp,MPOutTmp,obAtmp.copy(),obRtmp.copy())
	#print(obAtmp)
	print("obrm")
	print(obRm)
	return (sum(obAm)+sum(obRm),MInTmp.copy(),MOutTmp.copy(),MPInTmp.copy(),MPOutTmp.copy(),obAm.copy(),obRm.copy())	


			#trouver les bus a recalculer 
			#calculer la congestion aproprier grace a iScTmax
			#ajouter firstbus et last bus a etudiants ? 



#retourne les liste obj modifier avec les val calculees
def CalcObj(busAllerP,busRetourP,MInT,MOutT,MPInT,MPOutT,objA,objR):
	global busAller
	global busRetour
	global nbStationA
	global nbStationB
	

	print(busAllerP)
	print(busRetourP)

	for b in busAllerP:
		obTmp=0
		passg=0
		for i in range(0,nbStationA):
			passg+=MInT[b][i]
			passg-=MOutT[b][i]
			if passg>busAller[b].capacity:
				obTmp+=passg-busAller[b].capacity
		objA[b]=obTmp
	

	for b in busRetourP:
		obTmp=0
		passg=0
		passg=MPInT[b][0]
		if passg>busAller[b].capacity:
			obTmp+=passg-busAller[b].capacity
		for i in range(1,nbStationB-1):
			passg+=MPInT[b][i]
			passg-=MPOutT[b][i-1]
			if passg>busAller[b].capacity:
				obTmp+=passg-busAller[b].capacity
		objR[b]=obTmp
	#à changer
		#objR[b]=0
	print("objR")
	print(objR)
	return(objA,objR)





def Bestperiod(sc,sa,periodList):
	global bus
	global MIn
	global MOut
	global MPIn
	global MPOut
	global Congestion
	global objA
	global objR

#TODO NEXT + log system
	minCong=99999999999999
	minT=-1
	mMInTmp=[]
	mMOutTmp=[]
	mMPInTmp=[]
	mMPOutTmp=[]
	mObAtmp=[]
	mObRtmp=[]
	congTmp=0	
	obAtmp=[]
	obRtmp=[]

	#print("periodlist"+str(periodList))
	for t in periodList:
		if sc.check_period(t)==False:
			print(periodList)
			sys.exit("check period issue, t:"+str(t))
	#for t in range (0,1):
		print ("t ---- "+str(t))
		(congTmp,MInTmp,MOutTmp,MPInTmp,MPOutTmp,obAtmp,obRtmp)=ProcessCongestion(sc,t)
		print("cong--------------------------------------------------"+str(congTmp))
		if (congTmp<minCong):

			#print("min per")
			#print(MInTmp)
			print("-----------------------")
			print(congTmp)
			minT=t
			minCong=congTmp
			mMInTmp=MInTmp.copy()
			mMOutTmp=MOutTmp.copy()
			mMPInTmp=MPInTmp.copy()
			mMPOutTMp=MPOutTmp.copy()
			mObAtmp=obAtmp.copy()
			mObRtmp=obRtmp.copy()
	print("best")
	#if(minCong>0):
	#	sys.exit()
	MIn=mMInTmp.copy()
	MOut=mMOutTmp.copy()
	MPIn=mMPInTmp.copy()
	MPOut=mMPOutTMp.copy()
	objA=mObAtmp.copy()
	objR=mObRtmp.copy()
	# print("MINtmp")
	# print(mMInTmp)
	# print("MIn after")
	# print(MIn)
	return(minT)





etudiants=[]
#cours=[]
salles=[]
seances=[]
Tmax=[600,1200,1800,2400,3000]
busAller=[]
busRetour=[]
seancesToAffect=[]

#MIn=[[]] #C->U
#MOut=[[]] #C->U
#MPIn=[[]] #U->C
#MPOut=[[]] #U->C
objA=[] #congestion creer par chaque bus
objB=[] 
nbStationA=2 #12
nbStationB=2 #11

rand.seed(1)


ReadGraph()
printAdjGraph()
addStudent()
addRoom()
ReadBus()
tmp=[0 for i in range(0,nbStationA)]
# tmp2=[0 for i in range(0,nbStationB)]
# tmp3=[0 for i in range(0,nbStationA)-1]
# tmpp4=[0 for i in range(0,nbStationB)-1]
#MIn=[ tmp.copy() for i in range(0,len(busAller)+len(busRetour)-1)]
MIn=[[0,0] for i in range(0,len(busAller)+len(busRetour)-1)]
MOut=[[0,0] for i in range(0,len(busAller)+len(busRetour)-1)]
MPIn=[[0,0] for i in range(0,len(busAller)+len(busRetour)-1)]
MPOut=[[0,0] for i in range(0,len(busAller)+len(busRetour)-1)]
objA=[0 for i in range(0,len(busAller)+len(busRetour)-1)]
objR=[0 for i in range(0,len(busAller)+len(busRetour)-1)]
for b in busRetour:
	print(str(b.id)+" "+str(b.deb)+" "+str(b.itmax)+" " + str(b.interStTime))

seancesToAffect=seances.copy()

# print(ProcessCongestion(seances[0],2800)[1])
# seances[0].set_period(2800,salles[0])
# print(ProcessCongestion(seances[1],0)[1])
# seances[0].set_period(0,salles[0])



# e=None 
# print(  1 < 2 or 1 < MIn[None] )
ConstructEdt()


print(sum(objA)+sum(objR))

for sc in seances:
	etubus=0
	for etu in sc.etudiants:
		if etu.bus:
			etubus+=1
	print("seance:"+str(sc.id)+" period:"+str(sc.period)+" durée:"+str(sc.duration)    +" nb etudiants bus:"+str(etubus)+" nb etu:"+str(len(sc.etudiants)))

s=0
for etu in etudiants:
	if etu.bus:
		print(etu.firstbus)
		s+=1
print(s)

sys.setrecursionlimit(50000)
dill.dump_session("edt.pkl")

#ConstructEdt()
# a=Seance(1)
# b=Seance(2)
# a.ngh.append(b)
# b.ngh.append(a)
# seances.append(a)
# seances.append(b)
# c=Salle(1,20)
# d=Salle(2,50)
# salles.append(d)
# salles.append(c)
# ListSort()
# print(salles)
# print(seances)