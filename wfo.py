
import myfuncs as mf


# Job Class
class Jobs:
    def __init__(self, name, time):
        self.name = name
        self.time = time


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
        self.jobs.append(Job)

    # Remove a Job from a persons workflow
    def removejob(self, Job):
        self.remainingtime = round(self.remainingtime + Job.time, 2)
        self.jobs.remove(Job)


# Generate our employee data
all_people = mf.createdf("data.xlsx", "People")
peoplenames = all_people["Person"].values
peoplevalues = all_people["Time Available"].values

# Generate our Job data
all_jobs = mf.createdf("data.xlsx", "Jobs")
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

# Assign our Fluid lists
Peopletobeassigned = People_Objects
Jobstobeassigned = Job_Objects


# Spawn our initial People - Job configurations
print("-------- Spawn ------------")
mf.spreadJobsRandomly(Peopletobeassigned, Jobstobeassigned)


# Set variable to be an initial value well out of the range
bestscore = 100000

# The number of Generations we want to run
Generations = 10000000

# Our Optimisation loop
for rounds in range(1, Generations+1, 1):

    print(f"Generation {rounds}")

    # The people who we stole jobs from
    Peopletobeassigned = []

    # Get the score of our current configuration
    configscore = mf.fitnessfunc(People_Objects)

    # If we get a new highscore save it in memory
    if configscore < bestscore:
        bestconfig = []
        bestscore = configscore
        for i in People_Objects:
            bestconfig.append([i.name, i.time, i.remainingtime, [x.name for x in i.jobs]])

    # Loop over all Employees, Any who are over burdened we remove their jobs
    for i in People_Objects:
        if i.remainingtime < 0:
            Peopletobeassigned.append(i)
            Jobstobeassigned += i.jobs
            for j in i.jobs[:]:
                i.removejob(j)

    # Get the person with the most free time
    weakestlink = mf.getbiggesttimes(People_Objects)
    # Strip their jobs
    Jobstobeassigned += mf.stripjobs(People_Objects[weakestlink])
    # Add them to the pool
    Peopletobeassigned.append(People_Objects[weakestlink])

    # If we have less than 2
    # Get the next person with the most free time and do the same
    if len(Peopletobeassigned) < 2:
        weakestlink = mf.getlowesttimes(People_Objects)
        Jobstobeassigned += mf.stripjobs(People_Objects[weakestlink])
        Peopletobeassigned.append(People_Objects[weakestlink])


    # Spread our jobs randomly again
    mf.spreadJobsRandomly(Peopletobeassigned, Jobstobeassigned)
    print(" ")
    print(" ")


print("------")
print(f"Best score: {bestscore}")
print(f"Best Config: \n")
for i in bestconfig:
    print(i)
