class EventManager:
    eventDictionary = {}
    eventDictionaryReturn = {}

    def __init__(self):
        pass
    
    # commence a ecouter un evenement
    @staticmethod
    def StartListening(eventName:str, listener):
        if eventName in EventManager.eventDictionary:
            EventManager.eventDictionary[eventName].append(listener)
        else:
            EventManager.eventDictionary[eventName] = [listener]

    # arrete d'ecouter un evenement
    @staticmethod
    def StopListening(eventName:str, listener):
        if eventName in EventManager.eventDictionary:
            EventManager.eventDictionary[eventName].remove(listener)
            if len(EventManager.eventDictionary[eventName]) == 0:
                EventManager.eventDictionary.pop(eventName)

    #fait jouer un evenement
    @staticmethod
    def TriggerEvent(eventName:str, parametre):
        returnValue = []

        if eventName in EventManager.eventDictionary:
            for func in EventManager.eventDictionary[eventName]:
                returnValue.append(func(parametre))
            if len(returnValue) == 1:
                return returnValue[0]
            else:
                return returnValue
        return None