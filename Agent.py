import random


VARIANTS = ['a', 'b']
T = 10

class Agent:
    def __init__(self, lamb, H, ideolect, id, isAdult):
        self.ideolect = ideolect
        self.lamb = lamb
        self.H = H
        self.id = id
        self.isAdult = isAdult

    def reproduction(self):
        utternace = random.choices(VARIANTS, weights=self.ideolect, k=T)
        return utternace

    def retention(self, personal_utterance, other_utterance, other_agent, weights):
        pers = {}
        other = {}
        for i in VARIANTS:
            pers[VARIANTS.index(i)] = personal_utterance.count(i)
            other[VARIANTS.index(i)] = other_utterance.count(i)
            self.ideolect[VARIANTS.index(i)] = (self.ideolect[VARIANTS.index(i)] 
                + (self.lamb / T) * ((pers[VARIANTS.index(i)] * weights[VARIANTS.index(i)]) + (self.lamb *self.H) 
                        * (other[VARIANTS.index(i)] * weights[VARIANTS.index(i)]))) / (1 + self.lamb * (1 + (self.lamb *self.H)))