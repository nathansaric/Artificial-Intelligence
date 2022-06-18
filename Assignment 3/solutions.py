# =============================
# Student Names: Hannah Larsen, Nathan Saric
# Group ID: Group 13
# Date: March 27, 2022
# =============================
# solutions.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

'''Implement the methods from the classes in inference.py here'''

import util
from util import raiseNotDefined
import random
import busters
from distanceCalculator import manhattanDistance
import inference

def normalize(self):
    """
    Normalize the distribution such that the total value of all keys sums
    to 1. The ratio of values for all keys will remain the same. In the case
    where the total value of the distribution is 0, do nothing.
    >>> dist = DiscreteDistribution()
    >>> dist['a'] = 1
    >>> dist['b'] = 2
    >>> dist['c'] = 2
    >>> dist['d'] = 0
    >>> dist.normalize()
    >>> list(sorted(dist.items()))
    [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0)]
    >>> dist['e'] = 4
    >>> list(sorted(dist.items()))
    [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0), ('e', 4)]
    >>> empty = DiscreteDistribution()
    >>> empty.normalize()
    >>> empty
    {}
    """
    
    # Creating a new copy for total of the sum
    # of distributions so it doesn't get overwritten
    totalSum = self.total()

    # Case in which total is zero
    # Do nothing
    if (totalSum == 0):
        return
    # Alternative case where total is NOT zero
    # Normalize
    else:
        for i in self.keys():
            self[i] /= totalSum


def sample(self):
    """
    Draw a random sample from the distribution and return the key, weighted
    by the values associated with each key.
    >>> dist = DiscreteDistribution()
    >>> dist['a'] = 1
    >>> dist['b'] = 2
    >>> dist['c'] = 2
    >>> dist['d'] = 0
    >>> N = 100000.0
    >>> samples = [dist.sample() for _ in range(int(N))]
    >>> round(samples.count('a') * 1.0/N, 1)  # proportion of 'a'
    0.2
    >>> round(samples.count('b') * 1.0/N, 1)
    0.4
    >>> round(samples.count('c') * 1.0/N, 1)
    0.4
    >>> round(samples.count('d') * 1.0/N, 1)
    0.0
    """

    # Normalize to begin with, since we aren't necessarily guaranteed to have normalized values
    # -> as stated in question desc.
    self.normalize()

    # Initializing lists for later use
    orderedDist, totalList, keysList = [],[],[]
    
    # Making the ordered list in ascending numerical order by using sort function
    orderedDist = sorted(self.items())

    # Initializing total value to zero (will need to be incremented later on)
    total = 0
    
    # Iterating through the ordered distribution list
    # Adding the totals to the total list, and the keys to the key list
    for i in orderedDist:
        if (i[1] != 0):
            total += i[1]
            totalList.append(total)
            keysList.append(i[0])

    # Choosing a random number between [0.0 and 1.0)
    rand = random.random()

    # Iterating through the list of total values
    for j in range(len(totalList)):
        # Using the random number & totals list we created earlier to dictate
        # whether or not we return a sample in the list of keys at a specific position
        if (totalList[j] >= rand):
            return keysList[j]


def getObservationProb(self, noisyDistance, pacmanPosition, ghostPosition, jailPosition):
    """
    Return the probability P(noisyDistance | pacmanPosition, ghostPosition).
    """

    # Calculating the Manhattan distance between pacman's position and ghost's position
    manhat = manhattanDistance(pacmanPosition, ghostPosition)

    # Special cases for jailPosition (as defined in Question 2 instructions)
    if (ghostPosition == jailPosition and noisyDistance == None):
        return 1
    elif (ghostPosition != jailPosition and noisyDistance == None):
        return 0
    elif (ghostPosition == jailPosition and noisyDistance != None):
        return 0

    # Returning P(noisyDistance | pacmanPosition, ghostPosition)
    return busters.getObservationProbability(noisyDistance, manhat)


def observeUpdate(self, observation, gameState):
    """
    Update beliefs based on the distance observation and Pacman's position.
    The observation is the noisy Manhattan distance to the ghost you are
    tracking.
    self.allPositions is a list of the possible ghost positions, including
    the jail position. You should only consider positions that are in
    self.allPositions.
    The update model is not entirely stationary: it may depend on Pacman's
    current position. However, this is not a problem, as Pacman's current
    position is known.
    """

    # Creating a new instance of the discrete distribution object
    posDist = inference.DiscreteDistribution()

    # Iterating through all the positions and updating probability and belief distribution at a certain position
    # This includes all legal positions and the special case with the jailPosition
    for pos in self.allPositions:
        probability = self.getObservationProb(observation, gameState.getPacmanPosition(), pos, self.getJailPosition())
        posDist[pos] = self.beliefs[pos] * probability

    # Normalize the distribution and update beliefs
    posDist.normalize()
    self.beliefs = posDist


def elapseTime(self, gameState):
    """
    Predict beliefs in response to a time step passing from the current
    state.
    The transition model is not entirely stationary: it may depend on
    Pacman's current position. However, this is not a problem, as Pacman's
    current position is known.
    """

    # Creating a new instance of the discrete distribution object
    posDist = inference.DiscreteDistribution()

    # Iterating through all positions and obtaining the distribution over new 
    # positions for the ghost given its previous position
    for oldPos in self.allPositions:
        newPosDist = self.getPositionDistribution(gameState, oldPos)

        # Iterating through all positions and updating beliefs at every possible new position
        for newPos in newPosDist.keys():
            posDist[newPos] = (self.beliefs[oldPos] * newPosDist[newPos] + posDist[newPos])

    # Normalize the distribution and update beliefs
    posDist.normalize()
    self.beliefs = posDist 