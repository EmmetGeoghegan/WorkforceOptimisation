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


# Job Class
class Jobs:
    def __init__(self, name, time):
        self.name = name
        self.time = time
        self.assigned = False


# People Class
class People:
    def __init__(self, name, time):
        self.name = name
        self.time = time
        self.remainingtime = time
        self.jobs = []

    # Add a Job to a persons workflow
    def addjob(self, Job):
        self.remainingtime = round(self.remainingtime - Job.time, 2)
        Job.assigned = True
        self.jobs.append(Job)

    # Remove a Job from a persons workflow
    def removejob(self, Job):
        self.remainingtime = round(self.remainingtime + Job.time, 2)
        Job.assigned = False
        self.jobs.remove(Job)


# Generate our employee data
all_people = createdf("data.xlsx", "People")
peoplenames = all_people["Person"].values
peoplevalues = all_people["Time Available"].values

# Generate our Job data
all_jobs = createdf("data.xlsx", "Jobs")
jobnames = all_jobs["Project"].values
jobvalues = all_jobs["Average Time Per Week (Hours)"].values


# Create our Employee Objects
People_Objects = []
for i in range(len(peoplenames)):
    People_Objects.append(People(peoplenames[i], peoplevalues[i]))

# Create our Job Objects
Job_Objects = []
for i in range(len(jobnames)):
    Job_Objects.append(Jobs(jobnames[i], jobvalues[i]))

# for i in People_Objects:
#     print(i.name, i.time)
#
# for i in Job_Objects:
#     print(i.name, i.time)

# Go through jobs
# Assign to people in round robin
# Remove the job from available list
# Add job to the assigned list


Peopletobeassigned = People_Objects
Jobstobeassigned = Job_Objects


def spreadJobs(People, Jobs):
    while Jobs != []:
        rand_person = random.choice(People)
        rand_job = random.choice(Jobs)
        rand_person.addjob(rand_job)
        Jobs.remove(rand_job)

def gettimes(person_list):
    timelist = []
    for i in person_list:
        timelist.append(i.remainingtime)
    index_min = min(range(len(timelist)), key=timelist.__getitem__)
    return index_min
        # Look at test func

def stripjobs(Person):
    print(Person.name, [x.name for x in Person.jobs])
    jobs = []
    jobs += Person.jobs
    for j in Person.jobs[:]:
        i.removejob(j)
    return jobs

# # Do Our first assign
# while Job_Objects != []:
#     rand_person = random.choice(People_Objects)
#     rand_job = random.choice(Job_Objects)
#     assigned_jobs.append(rand_job)
#     rand_person.addjob(rand_job)
#     Job_Objects.remove(rand_job)
print("-------- Spawn ------------")
spreadJobs(Peopletobeassigned, Jobstobeassigned)


for rounds in range(1,200,1):
    print("      ")
    print(f"ROUND {rounds}")
    print("      ")
    Peopletobeassigned = []
    for i in People_Objects:
        print(i.name, i.time, i.remainingtime, [x.name for x in i.jobs])
        if i.remainingtime < 0:
            Peopletobeassigned.append(i)
            Jobstobeassigned += i.jobs
            for j in i.jobs[:]:
                i.removejob(j)


    print("      ")
    print(f"After Checking")
    print("      ")
    print("--- Jobless People ---")
    print([x.name for x in Peopletobeassigned])
    print("----------------------")
    print("      ")
    print("--- Peopleless Jobs ---")
    print([x.name for x in Jobstobeassigned])
    print("-----------------------")
    print("   ")

    print("------- After Removal --------")
    for i in People_Objects:
        print(i.name, i.remainingtime, [x.name for x in i.jobs])
    print("  ")

    print(f"The Lowest person is {gettimes(People_Objects)}")
    print("BEFORE", [x.name for x in Jobstobeassigned])
    Jobstobeassigned += stripjobs(People_Objects[gettimes(People_Objects)])
    print("AFTER", [x.name for x in Jobstobeassigned])

    Peopletobeassigned += People_Objects[gettimes(People_Objects)]
    print("--- Jobless People ---")
    print([x.name for x in Peopletobeassigned])
    print("----------------------")
    print("      ")
    print("--- Peopleless Jobs ---")
    print([x.name for x in Jobstobeassigned])
    print("-----------------------")

    spreadJobs(Peopletobeassigned, Jobstobeassigned)
    print(" ")
    print(" ")
# print("------")
# for i in People_Objects:
#     print(i.name, i.time, i.remainingtime, [x.name for x in i.jobs])
#
# print("--------")
# print([x.name for x in Job_Objects])
# print([x.name for x in Peopletobeassigned])
