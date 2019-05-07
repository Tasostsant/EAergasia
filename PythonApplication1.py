#!bin/python
import random
import math
import numpy as np

def resetBees():
    locArray = [[25,65,100],[23,8,200],[7,13,327],[95,53,440],
            [3,3,450],[54,56,639],[67,78,650],[32,4,678],
            [24,76,750],[66,89,801],[84,4,945],[34,23,967]]
    return locArray
def sum(locArray):
    sum=0
    for i in locArray:
        sum=sum+i[2]
    return sum
def evalute(pagida,locArray):
    score=[]
    pagidaIndex=0
    for i in pagida:
        scorePagidas=0
        for j in locArray:
            x=(i[0]-j[0])**2
            y=(i[1]-j[1])**2
            a=x+y
            d=math.sqrt(a)
            k=(j[2]*141.42)/((20*d)+0.00001)
            if(j[2]-k>0):
                j[2]=j[2]-k
            else:
                j[2]=0
            #print("sfikes pou skotothikan: "+str(k))
            #print("Sfikes se afth tin folia pou emeinan: "+str(j[2]))
            scorePagidas=scorePagidas+k
        #print(scorePagidas,pagidaIndex)
        score=np.append(score,[scorePagidas])
        pagidaIndex=pagidaIndex+1
    return score
def findBest(score):
    scorePagidas=[]
    larger=0
    smaller=9000
    #TODO: allazw afto me max kill pou eixa kanei
    counter=0
    for i in 0,3,6:
        sum=score[i]+score[i+1]+score[i+2]    
        scorePagidas=np.append(scorePagidas,[sum])
        pointerMed=0
        if(sum>larger):
            larger=sum
            pointer=counter
        if(sum<smaller):
            smaller=sum
            pointerSmall=counter
        if(sum>smaller and sum<larger):
            pointerMed=counter
        counter+=1
    return scorePagidas,pointer,pointerSmall,pointerMed
def mutate(array,max,min,med,mutationFactor):
    #se periptosi pou exw dio panomoiotipous goneis 
    #prokalo metalaksi se enan
    if array[max].all()==array[med].all():
        ran=bool(random.getrandbits(1))
        if(ran==True):
            array[med]+=0.02
        else:
            array[med]-=0.02
    #array[min]=(((array[med])+(array[max])))/2
    #pernontas ta proigoumena arrays dimiourgo ena paidi
    #pou pernei xaraktiristika kai apo tous 3
    #se diaforetika pososta
    array[min]=(((array[med]*0.25)+(array[max]*0.70)+(array[min]*0.05)))
    mutationFactorApplied=mutationFactor*random.randint(-3,3)
    if((array[min].any()+mutationFactorApplied)>100):
        array[min]-=mutationFactorApplied
    elif((array[min].any()-mutationFactorApplied)<0): 
        array[min]+=mutationFactorApplied
    else:
        array[min]+=mutationFactorApplied
    return array

maxRangePagida=15
gen=int(input("Gens: "))
locArray = [[25,65,100],[23,8,200],[7,13,327],[95,53,440],
            [3,3,450],[54,56,639],[67,78,650],[32,4,678],
            [24,76,750],[66,89,801],[84,4,945],[34,23,967]]
mutationFactor=0.2
print("MAX KILL:"+str(sum(locArray)))

for i in range(gen):
    print("Run number "+str(i))
    locArray=resetBees()
    if(i==0):
        print("Frist run setting traps arrays...")
        #pagidaArray1= [[random.randint(1,100),random.randint(1,100)],
        #            [random.randint(1,100),random.randint(1,100)],
        #            [random.randint(1,100),random.randint(1,100)]]
        #pagidaArray2= [[random.randint(1,100),random.randint(1,100)],
        #                [random.randint(1,100),random.randint(1,100)],
        #                [random.randint(1,100),random.randint(1,100)]]
        #pagidaArray3= [[random.randint(1,100),random.randint(1,100)],
        #                [random.randint(1,100),random.randint(1,100)],
        #                [random.randint(1,100),random.randint(1,100)]]
        #pagidaArray1=[[0.0,4.0],[85.0,23.0],[61.0,28.0]]
        #pagidaArray2=[[0.0,4.0],[85.0,23.0],[8.0,98.0]]
        #pagidaArray3=[[64.0,12.0],[19.0,25.0],[37.0,86.0]]
        pagidaArray1= [[round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)],
                    [round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)],
                    [round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)]]
        pagidaArray2= [[round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)],
                    [round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)],
                    [round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)]]
        pagidaArray3= [[round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)],
                    [round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)],
                    [round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)]]
        pagidaArrays=np.array([pagidaArray1,pagidaArray2,pagidaArray3])
    print("Start")
    locArray=resetBees()
    score=evalute(pagidaArrays[0],locArray)
    #deftero run
   # print("####")
    locArray=resetBees()
    score=np.append([score],[evalute(pagidaArrays[1],locArray)])
    #print("####")
    locArray=resetBees()
    score=np.append([score],[evalute(pagidaArrays[2],locArray)])
    best,pointer,worstPointer,medPointer=findBest(score)
    print("####BEST####")
    print(best)
    print("#############")
    #print("####BIGGESTPOINTER####")
    #print(pointer)
    #print("#############")
    #print("####WORSTPOINTER####")
    #print(worstPointer)
    #print("#############")
    pagidaArrays=mutate(pagidaArrays,pointer,worstPointer,medPointer,mutationFactor)

locArray=resetBees()
score=evalute(pagidaArrays[0],locArray)
locArray=resetBees()
#deftero run
#print("####")
score=np.append([score],[evalute(pagidaArrays[1],locArray)])
locArray=resetBees()
#print("####")
score=np.append([score],[evalute(pagidaArrays[2],locArray)])
locArray=resetBees() 
SinolikoScore,pointer,worstPointer,medPointer=findBest(score)
print("Best Score: "+str(SinolikoScore[pointer]))
print("Topologia pagidas:"+str(pagidaArrays[pointer]))



