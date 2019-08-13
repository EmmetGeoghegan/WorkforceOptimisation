import pandas as pd
import random


# Excel Parser
def createdf(filename, sheetname):
    try:
        xlsx = pd.ExcelFile(filename)
        dataframe = pd.DataFrame(pd.read_excel(xlsx, sheetname, index_col=False))
        return(dataframe)
    except FileNotFoundError:
        print("File not found")


# Fitness Function
def fitnessfunc(People):
    totaltime = 0
    for i in People:
        if i.remainingtime < 0:
            totaltime += 1000000
        else:
            totaltime += i.remainingtime
        totaltime = totaltime/len(People)
    return totaltime


# Spread jobs
def spreadJobsRandomly(People, Jobs):
    while Jobs != []:
        rand_person = random.choice(People)
        rand_job = random.choice(Jobs)
        rand_person.addjob(rand_job)
        Jobs.remove(rand_job)


# Get the lowest time
def getlowesttimes(person_list):
    timelist = []
    for i in person_list:
        timelist.append(i.remainingtime)
    index_min = min(range(len(timelist)), key=timelist.__getitem__)
    return index_min


# Get the highest remaining time
def getbiggesttimes(person_list):
    timelist = []
    for i in person_list:
        if i.remainingtime == 39.5:
            timelist.append(-100)
        else:
            timelist.append(i.remainingtime)
    index_max = max(range(len(timelist)), key=timelist.__getitem__)
    return index_max


# Get rid of a Persons Jobs
def stripjobs(Person):
    # print(Person.name, [x.name for x in Person.jobs])
    jobs = []
    jobs += Person.jobs
    for j in Person.jobs[:]:
        Person.removejob(j)
    return jobs
