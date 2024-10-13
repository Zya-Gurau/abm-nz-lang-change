import random

VARIANTS = ['a', 'b']
#numer of token in an utterance
T = 10

class Agent:
    """
        Defines an agent for use in the simulation
        Ideolect: (list) reproduction probabilities for each variant 
        lamb: (float) determines the weighting given to new tokens over old tokens
        h: (float) interaction parameter
        id: (int) unique number identifying the agent
        isAdult: (bool) shows if agent is adult
    """
    
    def __init__(self, lamb, H, ideolect, id, isAdult):
        self.ideolect = ideolect
        self.lamb = lamb
        self.H = H
        self.id = id
        self.isAdult = isAdult

    def reproduction(self):
        """
            Creates an utternace of tokens of length T based on probabilites in ideolect
        """

        utternace = random.choices(VARIANTS, weights=self.ideolect, k=T)
        return utternace

    def retention(self, personal_utterance, other_utterance, weights):
        """
            Modify reproduction probabilites based on own utterance and interlocutor utterance
        """

        pers = {}
        other = {}
        for i in VARIANTS:
            pers[VARIANTS.index(i)] = personal_utterance.count(i)
            other[VARIANTS.index(i)] = other_utterance.count(i)
            self.ideolect[VARIANTS.index(i)] = (self.ideolect[VARIANTS.index(i)] 
                + (self.lamb / T) * ((pers[VARIANTS.index(i)] * weights[VARIANTS.index(i)]) + (self.lamb *self.H) 
                        * (other[VARIANTS.index(i)] * weights[VARIANTS.index(i)]))) / (1 + self.lamb * (1 + (self.lamb *self.H)))