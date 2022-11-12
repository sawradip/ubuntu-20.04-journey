import os
import time
import random

MAX_VALID_FACT_TRIES = 20
MAX_VALID_PREDICATE_TRIES = 5
MAX_FACTS_INIT_STATE = 50
MAX_FACTS_GOAL_STATE = 10
# ELITISM_FACTOR = 2
# MUTATION_PROBABILITY = 40
# MULTITHREADS = True
CACHEDPLOTS = False
# DESIRED_STORY_ARC = "++++--"

###################################################################################
#############################    GenerateInitialPopulation    #####################
###################################################################################

# GetRandomValidObject
def CheckUniquePredicateAndParameterInstance(state, predicatename, parameterindex, value):
    for i, p in enumerate(state):
        if p['name'] == predicatename:
            if p['parameters'][parameterindex] == value:
                return True
    return False

# GenerateRandomFact
def GetRandomValidObject(objects, objecttype, state, predicate, parameter, parameterindex):
    for i in range(MAX_VALID_FACT_TRIES):
        randobj = random.randrange(len(objects))
        if objects[randobj]['type'] == objecttype :
            if parameter['unique']:
                if not CheckUniquePredicateAndParameterInstance(state, predicate['name'], parameterindex, objects[randobj]['name']):
                    return objects[randobj]['name']
            else:
                return objects[randobj]['name']

# GenerateRandomFact
def CheckRepetedPredicateAndParameters(state, predicate):
    for i, p in enumerate(state):
        if p['name'] == predicate['name']:
            totalmatch = 0
            for ii in range(len(predicate['parameters'])):
                if p['parameters'][ii] == predicate['parameters'][ii]:
                    totalmatch = totalmatch + 1

            if totalmatch == len(predicate['parameters']):
                return True
    return False        

# GenerateRandomFact
def CheckOpositePredicateAndParameter(state, allpredicates, predicate)  :
    for i, p in enumerate(allpredicates):
        if p['name'] == predicate['name']:
            if p['oposite']:
                for ii, ps in enumerate(state):
                    if ps['name'] == p['oposite']:
                        totalmatch = 0
                        for iii in range(len(predicate['parameters'])):
                            if ps['parameters'][iii] == predicate['parameters'][iii]:
                                totalmatch = totalmatch + 1
                        if totalmatch == len(predicate['parameters']):
                            return True
    return False

# GenerateIndividual
def GenerateRandomFact(objects, predicates, state, isinit, isgoal):
    for x in range(MAX_VALID_PREDICATE_TRIES):
        randpredicate = random.randrange(len(predicates))
        validlocation = True        # To check if randomly seleted predicate is valid for initial/final state

        if isinit:
            if not predicates[randpredicate]['initialstate']:
                # Selected predicate is not valid for initialstate
                validlocation = False

        if isgoal:
            if not predicates[randpredicate]['goalstate']:
                # Selected predicate is not valid for goalstate
                validlocation = False

        if validlocation:
            predParam = []
            # Iterate and select all the parameters of the chosen predicate
            for i, p in enumerate(predicates[randpredicate]['parameters']):
                factParam = GetRandomValidObject(objects, p['type'], state, predicates[randpredicate], p, i)
                if not factParam:
                    return None
                predParam.append(factParam)

            genPredicate = {'name': predicates[randpredicate]['name'],
                            'parameters' : predParam}
            if not CheckRepetedPredicateAndParameters(state, genPredicate):
                if not CheckOpositePredicateAndParameter(state, predicates, genPredicate):
                    return genPredicate

# GenerateInitialPopulation
def GenerateIndividual(worldObjects, worldPredicates, worldStaticPredicates, individualID):
    init = []
    goal = []
    numinitfacts = random.randrange(1, MAX_FACTS_INIT_STATE + 1)
    numgoalfacts = random.randrange(1, MAX_FACTS_GOAL_STATE + 1)

    for i, f in enumerate(worldStaticPredicates):
        init.append(f)
    
    isinit = True
    isgoal = False
    for i in range(numinitfacts):
        randomfact = GenerateRandomFact(worldObjects, worldPredicates, init, isinit, isgoal)
        if randomfact:
            init.append(randomfact)

    isinit = False
    isgoal = True
    for i in range(numgoalfacts):
        randomfact = GenerateRandomFact(worldObjects, worldPredicates, goal, isinit, isgoal)
        if randomfact:
            goal.append(randomfact)

    return {
        'initialstate': init,
        'goalstate' : goal,
        'id' : individualID,
        'plan' : "",
        'evaluation' : -1
    }

# RunGeneticAlgorithm
def GenerateInitialPopulation(worldObjects, worldPredicates, worldStaticPredicates, populationSize):
    currentPopulation = []
    for i in range(populationSize):
        individual = GenerateIndividual(worldObjects, worldPredicates, worldStaticPredicates, i)
        currentPopulation.append(individual)
    return currentPopulation

##################################################################################################
##################################################################################################


##################################################################################################
####################    EvaluatePopulation    ####################################################
##################################################################################################

def EvaluatePopulation(populationID, population, worldObjects, worldStaticPredicates, worldEvents):
    POPULATION_FOLDER = os.path.join('data', f'population{populationID}')
    if not os.path.isdir(POPULATION_FOLDER):
        os.makedirs(POPULATION_FOLDER)

    for i in range(len(population)):
        if 


def RunGeneticAlgorithm(worldObjects, worldPredicates, worldStaticPredicates, worldEvents, populationSize, numGenerations):
    currentPopulation = GenerateInitialPopulation(worldObjects, worldPredicates, worldStaticPredicates, populationSize)
    i = 1
    while True:
        start_time = time.time()
        EvaluatePopulation(i, currentPopulation, worldObjects, worldStaticPredicates, worldEvents)
    
    return currentPopulation
