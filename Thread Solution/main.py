#!bin/python
import random
import math
import queue as Queue
import numpy as np
from multiprocessing.pool import ThreadPool
from multiprocessing import Process, Manager
from threading import Thread
import concurrent.futures


#reset array gia ypologismo ton allon set
def resetBees():
    locArray = [[25,65,100],[23,8,200],[7,13,327],[95,53,440],
            [3,3,450],[54,56,639],[67,78,650],[32,4,678],
            [24,76,750],[66,89,801],[84,4,945],[34,23,967]]
    return locArray
#epistrefei to sinolo melison pou yparxoyn sinolika
def sum(locArray):
    sum=0
    for i in locArray:
        sum=sum+i[2]
    return sum
#ypologismos score ton pagidon
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
#evresi tou kaliterou, mesaiou kai xeiroterou score
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
def createPagidaArray():
    pagidaArray1= [[round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)],
                    [round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)],
                    [round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)]]
    pagidaArray2= [[round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)],
                    [round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)],
                    [round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)]]
    pagidaArray3= [[round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)],
                    [round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)],
                    [round(random.uniform(0.0,100.0),3),round(random.uniform(0.0,100.0),3)]]
            #dimiourgia array pou krataei ola ta set vombon     
    pagidaArrays=np.array([pagidaArray1,pagidaArray2,pagidaArray3])       
    return pagidaArrays
def evolve(gen):
    #thread start
    print("Thread Start!")
    #mutation Factor
    mutationFactor=0.2
    for i in range(gen):
        #print("Run number "+str(i))
        locArray=resetBees()
        if(i==0):
            print("Frist run setting traps arrays...")
            #dimiourgia random float theseon vombon
            #dimiourgia array pou krataei ola ta set vombon            
            pagidaArrays=createPagidaArray()
        #reset ton pinaka me tis sfikes
        locArray=resetBees()
        #evalute to score tou protou set
        score=evalute(pagidaArrays[0],locArray)
        #deftero run
        #reset ton pinaka me tis sfikes
        locArray=resetBees()
        #evalute to score tou defterou set
        score=np.append([score],[evalute(pagidaArrays[1],locArray)])
        #reset ton pinaka me tis sfikes
        locArray=resetBees()
        #evalute to score tou tritou set
        score=np.append([score],[evalute(pagidaArrays[2],locArray)])
        #apoktish ton pointers pou dixnoun ton kalitero, meso kai xeirotero
        best,pointer,worstPointer,medPointer=findBest(score)
        #print("####BEST####")
        #print(best)
        #print("#############")
        #print("####BIGGESTPOINTER####")
        #print(pointer)
        #print("#############")
        #print("####WORSTPOINTER####")
        #print(worstPointer)
        #print("#############")
        #dimiourgia paidiou kai metalakseis se afto
        pagidaArrays=mutate(pagidaArrays,pointer,worstPointer,medPointer,mutationFactor)
    # i diadikasia trexei mia teleftea fora sto telos kai emfanizei to kalitero score pou vrethike kathos kai tis sintetagmenes
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
    print("Best Score: "+str(SinolikoScore[pointer])+" Med Score: "+ str(SinolikoScore[medPointer])+ " Worst Score: "+ str(SinolikoScore[worstPointer]))
    #print("Topologia pagidas:"+str(pagidaArrays[pointer]))
    print("Thread Stoped")
    return pagidaArrays[pointer]

def evolveSpecific(gen,pagidaArrays):
    #thread start
    print("Thread Start!")
    #mutation Factor
    mutationFactor=0.2
    for i in range(gen):
        locArray=resetBees()
        #reset ton pinaka me tis sfikes
        locArray=resetBees()
        #evalute to score tou protou set
        score=evalute(pagidaArrays[0],locArray)
        #deftero run
        #reset ton pinaka me tis sfikes
        locArray=resetBees()
        #evalute to score tou defterou set
        score=np.append([score],[evalute(pagidaArrays[1],locArray)])
        #reset ton pinaka me tis sfikes
        locArray=resetBees()
        #evalute to score tou tritou set
        score=np.append([score],[evalute(pagidaArrays[2],locArray)])
        #apoktish ton pointers pou dixnoun ton kalitero, meso kai xeirotero
        best,pointer,worstPointer,medPointer=findBest(score)
        #dimiourgia paidiou kai metalakseis se afto
        pagidaArrays=mutate(pagidaArrays,pointer,worstPointer,medPointer,mutationFactor)
    # i diadikasia trexei mia teleftea fora sto telos kai emfanizei to kalitero score pou vrethike kathos kai tis sintetagmenes
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
    print("#######Thread Data#######")
    print("Best Score: "+str(SinolikoScore[pointer])+" Med Score: "+ str(SinolikoScore[medPointer])+ " Worst Score: "+ str(SinolikoScore[worstPointer]))
    #print("Topologia pagidas:"+str(pagidaArrays[pointer]))
    print("Thread Stoped")
    return pagidaArrays[pointer]
if __name__ == "__main__":
    gen=int(input("Gens: "))
    #dimiourgia tou pinaka pou krataei plirofories gia tis folies ton sfikon
    locArray = [[25,65,100],[23,8,200],[7,13,327],[95,53,440],
                [3,3,450],[54,56,639],[67,78,650],[32,4,678],
                [24,76,750],[66,89,801],[84,4,945],[34,23,967]]
    print("MAX KILL:"+str(sum(locArray)))
    que = Queue.Queue()
    threads_list = list()
    t = Thread(target=lambda q, arg1: q.put(evolve(arg1)), args=(que, gen))
    t.start()
    threads_list.append(t)
    t2 = Thread(target=lambda q, arg1: q.put(evolve(arg1)), args=(que, gen))
    t2.start()
    threads_list.append(t2)
    t3 = Thread(target=lambda q, arg1: q.put(evolve(arg1)), args=(que, gen))
    t3.start()
    threads_list.append(t3)
    BestArrays=[]
    for t in threads_list:
        t.join()
    print("Best of each thread:")
    while not que.empty():
        result = que.get()
        foo=[result]
        BestArrays=np.append([BestArrays],[[foo]])
    NewArray=[
        [
            [BestArrays[0],BestArrays[1]],
            [BestArrays[2],BestArrays[3]],
            [BestArrays[4],BestArrays[5]],
        ],
        [
            [BestArrays[6],BestArrays[7]],
            [BestArrays[8],BestArrays[9]],
            [BestArrays[10],BestArrays[11]],
        ],
        [
            [BestArrays[12],BestArrays[13]],
            [BestArrays[14],BestArrays[15]],
            [BestArrays[16],BestArrays[17]],
        ]]
    print(NewArray[0])
    print(NewArray[1])
    print(NewArray[2])

    print("Last run from the best 3 of threads:")
    pagidaArrays=np.array([NewArray[0],NewArray[1],NewArray[2]])   
    BestPagides=evolveSpecific(gen,pagidaArrays)