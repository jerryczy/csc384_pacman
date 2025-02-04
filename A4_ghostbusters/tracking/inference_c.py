

# inference.py

# ------------

# Licensing Information: Please do not distribute or publish solutions to this

# project. You are free to use and extend these projects for educational

# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by

# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).

# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html



import util

import random

import busters

import game



class InferenceModule:

  """

  An inference module tracks a belief distribution over a ghost's location.

  This is an abstract class, which you should not modify.

  """

  

  ############################################

  # Useful methods for all inference modules #

  ############################################

  

  def __init__(self, ghostAgent):

    "Sets the ghost agent for later access"

    self.ghostAgent = ghostAgent

    self.index = ghostAgent.index



  def getJailPosition(self):

     return (2 * self.ghostAgent.index - 1, 1)

    

  def getPositionDistribution(self, gameState):

    """

    Returns a distribution over successor positions of the ghost from the given gameState.

    

    You must first place the ghost in the gameState, using setGhostPosition below.

    """

    ghostPosition = gameState.getGhostPosition(self.index) # The position you set

    actionDist = self.ghostAgent.getDistribution(gameState)

    dist = util.Counter()

    for action, prob in actionDist.items():

      successorPosition = game.Actions.getSuccessor(ghostPosition, action)

      dist[successorPosition] = prob

    return dist

  

  def setGhostPosition(self, gameState, ghostPosition):

    """

    Sets the position of the ghost for this inference module to the specified

    position in the supplied gameState.

    """

    conf = game.Configuration(ghostPosition, game.Directions.STOP)

    gameState.data.agentStates[self.index] = game.AgentState(conf, False)

    return gameState

  

  def observeState(self, gameState):

    "Collects the relevant noisy distance observation and pass it along."

    distances = gameState.getNoisyGhostDistances()

    if len(distances) >= self.index: # Check for missing observations

      obs = distances[self.index - 1]

      self.observe(obs, gameState)

      

  def initialize(self, gameState):

    "Initializes beliefs to a uniform distribution over all positions."

    # The legal positions do not include the ghost prison cells in the bottom left.

    self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]   

    self.initializeUniformly(gameState)

    

  ######################################

  # Methods that need to be overridden #

  ######################################

  

  def initializeUniformly(self, gameState):

    "Sets the belief state to a uniform prior belief over all positions."

    pass

  

  def observe(self, observation, gameState):

    "Updates beliefs based on the given distance observation and gameState."

    pass

  

  def elapseTime(self, gameState):

    "Updates beliefs for a time step elapsing from a gameState."

    pass

    

  def getBeliefDistribution(self):

    """

    Returns the agent's current belief state, a distribution over

    ghost locations conditioned on all evidence so far.

    """

    pass



class ExactInference(InferenceModule):

  """

  The exact dynamic inference module should use forward-algorithm

  updates to compute the exact belief function at each time step.

  """

  

  def initializeUniformly(self, gameState):

    "Begin with a uniform distribution over ghost positions."

    self.beliefs = util.Counter()

    for p in self.legalPositions: self.beliefs[p] = 1.0

    self.beliefs.normalize()

  

  def observe(self, observation, gameState):

    """

    Updates beliefs based on the distance observation and Pacman's position.

    

    The noisyDistance is the estimated manhattan distance to the ghost you are tracking.

    

    The emissionModel below stores the probability of the noisyDistance for any true 

    distance you supply.  That is, it stores P(noisyDistance | TrueDistance).



    self.legalPositions is a list of the possible ghost positions (you

    should only consider positions that are in self.legalPositions).



    A correct implementation will handle the following special case:

      *  When a ghost is captured by Pacman, all beliefs should be updated so

         that the ghost appears in its prison cell, position self.getJailPosition()



         You can check if a ghost has been captured by Pacman by

         checking if it has a noisyDistance of None (a noisy distance

         of None will be returned if, and only if, the ghost is

         captured).

         

    """

    noisyDistance = observation

    emissionModel = busters.getObservationDistribution(noisyDistance)

    pacmanPosition = gameState.getPacmanPosition()

    

    "*** YOUR CODE HERE ***"

    # Replace this code with a correct observation update

    # Be sure to handle the "jail" edge case where the ghost is eaten

    # and noisyDistance is None



    allPossible = util.Counter()

    if noisyDistance is None:

      allPossible[self.getJailPosition] = 1

    else:

      for position in self.legalPositions:

        allPossible[position] = self.beliefs[position] * emissionModel[util.manhattanDistance(position, pacmanPosition)]



    "*** END YOUR CODE HERE ***"



    allPossible.normalize()

    self.beliefs = allPossible

        

  def elapseTime(self, gameState):

    """

    Update self.beliefs in response to a time step passing from the current state.

    

    The transition model is not entirely stationary: it may depend on Pacman's

    current position (e.g., for DirectionalGhost).  However, this is not a problem,

    as Pacman's current position is known.



    In order to obtain the distribution over new positions for the

    ghost, given its previous position (oldPos) as well as Pacman's

    current position, use this line of code:



      newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))



    Note that you may need to replace "oldPos" with the correct name

    of the variable that you have used to refer to the previous ghost

    position for which you are computing this distribution. You will need to compute

    multiple position distributions for a single update.



    newPosDist is a util.Counter object, where for each position p in self.legalPositions,

    

    newPostDist[p] = Pr( ghost is at position p at time t + 1 | ghost is at position oldPos at time t )



    (and also given Pacman's current position).  You may also find it useful to loop over key, value pairs

    in newPosDist, like:



      for newPos, prob in newPosDist.items():

        ...



    *** GORY DETAIL AHEAD ***



    As an implementation detail (with which you need not concern

    yourself), the line of code at the top of this comment block for obtaining newPosDist makes

    use of two helper methods provided in InferenceModule above:



      1) self.setGhostPosition(gameState, ghostPosition)

          This method alters the gameState by placing the ghost we're tracking

          in a particular position.  This altered gameState can be used to query

          what the ghost would do in this position.

      

      2) self.getPositionDistribution(gameState)

          This method uses the ghost agent to determine what positions the ghost

          will move to from the provided gameState.  The ghost must be placed

          in the gameState with a call to self.setGhostPosition above.



    It is worthwhile, however, to understand why these two helper methods are used and how they

    combine to give us a belief distribution over new positions after a time update from a particular position

    """

    

    "*** YOUR CODE HERE ***"

    allPossible = util.Counter()



    for oldPosition in self.legalPositions:



      newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPosition))

      

      for newPos, prob in newPosDist.items():

        allPossible[newPos] += self.beliefs[oldPosition] * prob



    allPossible.normalize()

    self.beliefs = allPossible



  def getBeliefDistribution(self):

    return self.beliefs



class ParticleFilter(InferenceModule):

  """

  A particle filter for approximately tracking a single ghost.

  

  Useful helper functions will include random.choice, which chooses

  an element from a list uniformly at random, and util.sample, which

  samples a key from a Counter by treating its values as probabilities.

  """



  

  def __init__(self, ghostAgent, numParticles=300):

     InferenceModule.__init__(self, ghostAgent);

     self.setNumParticles(numParticles)

  

  def setNumParticles(self, numParticles):

    self.numParticles = numParticles



  

  def initializeUniformly(self, gameState):

    """

      Initializes a list of particles. Use self.numParticles for the number of particles.

      Use self.legalPositions for the legal board positions where a particle could be located.



      ** NOTE **

        the variable you store your particles in must be a list; a list is simply a collection

        of unweighted variables (positions in this case). Storing your particles as a Counter or

        dictionary (where there could be an associated weight with each position) is incorrect

        and will produce errors

    """

    "*** YOUR CODE HERE ***"

    self.particles = [random.choice(self.legalPositions) for i in range(self.numParticles)]



  

  def observe(self, observation, gameState):

    """

    Update beliefs based on the given distance observation. Make

    sure to handle the special case where all particles have weight

    0 after reweighting based on observation. If this happens,

    resample particles uniformly at random from the set of legal

    positions (self.legalPositions).



    A correct implementation will handle two special cases:

      1) When a ghost is captured by Pacman, **all** particles should be updated so

         that the ghost appears in its prison cell, self.getJailPosition()



         You can check if a ghost has been captured by Pacman by

         checking if it has a noisyDistance of None (a noisy distance

         of None will be returned if, and only if, the ghost is

         captured).

         

      2) When all particles receive 0 weight, they should be recreated from the

         prior distribution by calling initializeUniformly. The total weight

         for a belief distribution can be found by calling totalCount on

         a Counter object



    util.sample(Counter object) is a helper method to generate a sample from

    a belief distribution



    You may also want to use util.manhattanDistance to calculate the distance

    between a particle and pacman's position.

    """



    noisyDistance = observation

    emissionModel = busters.getObservationDistribution(noisyDistance)

    pacmanPosition = gameState.getPacmanPosition()

    "*** YOUR CODE HERE ***"
    if noisyDistance is None:
        self.particles = [self.getJailPosition() for i in range(self.numParticles)]
    else:
        weightedParticles = util.Counter()
        for particle in self.particles:
            weightedParticles[particle] += emissionModel[util.manhattanDistance(pacmanPosition, particle)]
        weightedParticles.normalize()
        if weightedParticles.totalCount() == 0:
            self.initializeUniformly(gameState)
        else:
            self.particles = [util.sample(weightedParticles) for i in range(self.numParticles)]

  def elapseTime(self, gameState):

    """

    Update beliefs for a time step elapsing.



    As in the elapseTime method of ExactInference, you should use:



      newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))



    to obtain the distribution over new positions for the ghost, given

    its previous position (oldPos) as well as Pacman's current

    position.



    util.sample(Counter object) is a helper method to generate a sample from a

    belief distribution

    """

    "*** YOUR CODE HERE ***"

    updatedParticles = list()

    for particle in self.particles:

        newParticles = self.getPositionDistribution(self.setGhostPosition(gameState, particle))

        updatedParticles.append(util.sample(newParticles))



    self.particles = updatedParticles



  def getBeliefDistribution(self):

    """

      Return the agent's current belief state, a distribution over

      ghost locations conditioned on all evidence and time passage. This method

      essentially converts a list of particles into a belief distribution (a Counter object)

    """

    "*** YOUR CODE HERE ***"

    beliefs = util.Counter()

    for particle in self.particles:

      beliefs[particle]+=1.0

    beliefs.normalize()

    return beliefs



class MarginalInference(InferenceModule):

  "A wrapper around the JointInference module that returns marginal beliefs about ghosts."



  def initializeUniformly(self, gameState):

    "Set the belief state to an initial, prior value."

    if self.index == 1: jointInference.initialize(gameState, self.legalPositions)

    jointInference.addGhostAgent(self.ghostAgent)

    

  def observeState(self, gameState):

    "Update beliefs based on the given distance observation and gameState."

    if self.index == 1: jointInference.observeState(gameState)

    

  def elapseTime(self, gameState):

    "Update beliefs for a time step elapsing from a gameState."

    if self.index == 1: jointInference.elapseTime(gameState)

    

  def getBeliefDistribution(self):

    "Returns the marginal belief over a particular ghost by summing out the others."

    jointDistribution = jointInference.getBeliefDistribution()

    dist = util.Counter()

    for t, prob in jointDistribution.items():

      dist[t[self.index - 1]] += prob

    return dist

  

class JointParticleFilter:

  "JointParticleFilter tracks a joint distribution over tuples of all ghost positions."



  def __init__(self, numParticles=600):

     self.setNumParticles(numParticles)

  

  def setNumParticles(self, numParticles):

    self.numParticles = numParticles

  

  def initialize(self, gameState, legalPositions):

    "Stores information about the game, then initializes particles."

    self.numGhosts = gameState.getNumAgents() - 1

    self.ghostAgents = []

    self.legalPositions = legalPositions

    self.initializeParticles()

    

  def initializeParticles(self):

    "Initializes particles randomly.  Each particle is a tuple of ghost positions. Use self.numParticles for the number of particles"

    "*** YOUR CODE HERE ***"

    self.particles = [tuple([random.choice(self.legalPositions) for i in range(self.numGhosts)]) for j in range(self.numParticles)]



  def addGhostAgent(self, agent):

    "Each ghost agent is registered separately and stored (in case they are different)."

    self.ghostAgents.append(agent)

    

  def elapseTime(self, gameState):

    """

    Samples each particle's next state based on its current state and the gameState.



    To loop over the ghosts, use:



      for i in range(self.numGhosts):

        ...



    Then, assuming that "i" refers to the index of the

    ghost, to obtain the distributions over new positions for that

    single ghost, given the list (prevGhostPositions) of previous

    positions of ALL of the ghosts, use this line of code:



      newPosDist = getPositionDistributionForGhost(setGhostPositions(gameState, prevGhostPositions),

                                                   i, self.ghostAgents[i])



    **Note** that you may need to replace "prevGhostPositions" with the

    correct name of the variable that you have used to refer to the

    list of the previous positions of all of the ghosts, and you may

    need to replace "i" with the variable you have used to refer to

    the index of the ghost for which you are computing the new

    position distribution.



    As an implementation detail (with which you need not concern

    yourself), the line of code above for obtaining newPosDist makes

    use of two helper functions defined below in this file:



      1) setGhostPositions(gameState, ghostPositions)

          This method alters the gameState by placing the ghosts in the supplied positions.

      

      2) getPositionDistributionForGhost(gameState, ghostIndex, agent)

          This method uses the supplied ghost agent to determine what positions 

          a ghost (ghostIndex) controlled by a particular agent (ghostAgent) 

          will move to in the supplied gameState.  All ghosts

          must first be placed in the gameState using setGhostPositions above.

          

          The ghost agent you are meant to supply is self.ghostAgents[ghostIndex-1],

          but in this project all ghost agents are always the same.

    """

    newParticles = []

    for oldParticle in self.particles:

      mutableOldParticle = list(oldParticle) # A list of ghost positions

      

      # now loop through and update each entry in newParticle...



      "*** YOUR CODE HERE ***"



      newParticle = [util.sample(getPositionDistributionForGhost(setGhostPositions(gameState, mutableOldParticle), i, self.ghostAgents[i])) for i in range(self.numGhosts)]



      "*** END YOUR CODE HERE ***"

      newParticles.append(tuple(newParticle))

    self.particles = newParticles



  def getJailPosition(self, i):

    return (2 * i + 1, 1);

  

  def observeState(self, gameState):

    """

    Resamples the set of particles using the likelihood of the noisy observations.



    As in elapseTime, to loop over the ghosts, use:



      for i in range(self.numGhosts):

        ...



    A correct implementation will handle two special cases:

      1) When a ghost is captured by Pacman, all particles should be updated so

         that the ghost appears in its prison cell, position self.getJailPosition(i)

         where "i" is the index of the ghost.



         You can check if a ghost has been captured by Pacman by

         checking if it has a noisyDistance of None (a noisy distance

         of None will be returned if, and only if, the ghost is

         captured).



      2) When all particles receive 0 weight, they should be recreated from the

          prior distribution by calling initializeParticles. After all particles

          are generated randomly, any ghosts that are eaten (have noisyDistance of 0)

          must be changed to the jail Position. This will involve changing each

          particle if a ghost has been eaten.



    ** Remember ** We store particles as tuples, but to edit a specific particle,

    it must be converted to a list, edited, and then converted back to a tuple. Since

    this is a common operation when placing a ghost in the jail for a particle, we have

    provided a helper method named self.getParticleWithGhostInJail(particle, ghostIndex)

    that performs these three operations for you.



    """ 

    pacmanPosition = gameState.getPacmanPosition()

    noisyDistances = gameState.getNoisyGhostDistances()

    if len(noisyDistances) < self.numGhosts: return

    emissionModels = [busters.getObservationDistribution(dist) for dist in noisyDistances]



    "*** YOUR CODE HERE ***"



    for i in range(self.numGhosts):

      if noisyDistances[i] is None:

        self.particles = [self.getParticleWithGhostInJail(particle, i) for particle in self.particles[:]]



    weightedParticles = util.Counter()



    for particle in self.particles:

      weightedParticle = 1.0

      for i in range(self.numGhosts):

        if noisyDistances[i] is not None:

          weightedParticle *= emissionModels[i][util.manhattanDistance(pacmanPosition, particle[i])]

      weightedParticles[particle] += weightedParticle



    weightedParticles.normalize()



    if weightedParticles.totalCount() == 0:

      self.initializeParticles()

      for i in range(self.numGhosts):

        if noisyDistances[i] is None:

          self.particles = [self.getParticleWithGhostInJail(particle, i) for particle in self.particles[:]]



    else:

      self.particles = [util.sample(weightedParticles) for i in range(self.numParticles)]





  def getParticleWithGhostInJail(self, particle, ghostIndex):

    particle = list(particle)

    particle[ghostIndex] = self.getJailPosition(ghostIndex)

    return tuple(particle)

  

  def getBeliefDistribution(self):

    dist = util.Counter()

    for part in self.particles: dist[part] += 1

    dist.normalize()

    return dist



# One JointInference module is shared globally across instances of MarginalInference 

jointInference = JointParticleFilter()



def getPositionDistributionForGhost(gameState, ghostIndex, agent):

  """

  Returns the distribution over positions for a ghost, using the supplied gameState.

  """



  # index 0 is pacman, but the students think that index 0 is the first ghost.

  ghostPosition = gameState.getGhostPosition(ghostIndex+1) 

  actionDist = agent.getDistribution(gameState)

  dist = util.Counter()

  for action, prob in actionDist.items():

    successorPosition = game.Actions.getSuccessor(ghostPosition, action)

    dist[successorPosition] = prob

  return dist

  

def setGhostPositions(gameState, ghostPositions):

  "Sets the position of all ghosts to the values in ghostPositionTuple."

  for index, pos in enumerate(ghostPositions):

    conf = game.Configuration(pos, game.Directions.STOP)

    gameState.data.agentStates[index + 1] = game.AgentState(conf, False)

  return gameState  
