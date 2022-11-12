
import xmltodict
import pprint
import json

from genetics import RunGeneticAlgorithm


# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(json.dumps(doc))

def LoadEvents(eventsref):
    allevents = []
    if eventsref:
        for i, evt in enumerate(eventsref['event']):
            allevents.append({'name': evt['@name'],
                            'tension': evt['@tension']})
        return allevents

def LoadWorldObjects(worldobjref):
    allobj = []
    if worldobjref:
        for i, obj in enumerate(worldobjref['object']):
            allobj.append({'name': obj['@name'],
                        'type' : obj['@type']})
        return allobj

def LoadStaticPredicates(worldstaticref):
    allpredicates = []
    if worldstaticref:
        for i, pre in enumerate(worldstaticref['predicate']):
            pparameters = []
            if isinstance(pre['parameter'], list):
                for ip, param in enumerate(pre['parameter']):
                    pparameters.append(param['@value'])
                allpredicates.append({'name': pre['@name'],
                                    'parameters': pparameters })
            else:
                allpredicates.append({'name': pre['@name'],
                                    'parameters': [pre['parameter']['@value']]} )

        
        return allpredicates

def LoadWorldPredicates(worldpreref):
    allpredicates = []
    if worldpreref:
        for i, pre in enumerate(worldpreref['predicate']):
            inivalid = False
            goalvalid = False
            if pre['@initialstate'] == 'true':
                inivalid = True
            if pre['@goalstate'] == 'true':
                goalvalid = True
            if isinstance(pre['parameter'], list):
                pparameters = []
                for ip, param in enumerate(pre['parameter']):
                    if '@unique' in param.keys():
                        pparameters.append({ 'type': param['@type'], 'unique': (param['@unique'] == 'true')})
                    else:
                        pparameters.append({ 'type': param['@type'], 'unique' : False})
                allpredicates.append({ 'name': pre['@name'], 
                                        'parameters': pparameters,
                                        'initialstate': inivalid,
                                        'goalstate': goalvalid,
                                        'oposite' : '@oposite' in pre.keys()})
            else:
                pparameters = []
                param = pre['parameter']
                if '@unique' in param.keys():
                    pparameters.append({ 'type': param['@type'], 'unique': (param['@unique'] == 'true')})
                else:
                    pparameters.append({ 'type': param['@type'], 'unique' : False})
                allpredicates.append({ 'name': pre['@name'], 
                                        'parameters': pparameters,
                                        'initialstate': inivalid,
                                        'goalstate': goalvalid,
                                        'oposite' : '@oposite' in pre.keys()})
        return allpredicates

def Main():
    import random
    import time
    random.seed(time.time())

    with open('context.xml') as fd:
        doc = xmltodict.parse(fd.read())

    contextxml = doc['world']

    worldobjref = contextxml['objects']
    worldObjects = LoadWorldObjects(worldobjref)
    # pprint.pprint(worldObjects)

    worldpreref = contextxml['predicates']
    worldPredicates = LoadWorldPredicates(worldpreref)
    # pprint.pprint(worldPredicates)

    worldstaticref = contextxml['static']
    worldStaticPredicates = LoadStaticPredicates(worldstaticref)
    # pprint.pprint(worldStaticPredicates)

    worldeventsref = contextxml['events']
    worldEvents = LoadEvents(worldeventsref)
    # pprint.pprint(worldEvents)

    populationSize = 100
    numGenerations = 50
    population = RunGeneticAlgorithm(worldObjects, worldPredicates, worldStaticPredicates, worldEvents, populationSize, numGenerations)
    pprint.pprint(population)
if __name__ == '__main__':
    Main()