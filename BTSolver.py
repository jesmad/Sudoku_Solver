import SudokuBoard
import Variable
import Domain
import Trail
import Constraint
import ConstraintNetwork
import time
import random

class BTSolver:

	# ==================================================================
	# Constructors
	# ==================================================================

	def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
		self.network = ConstraintNetwork.ConstraintNetwork(gb)
		self.hassolution = False
		self.gameboard = gb
		self.trail = trail

		self.varHeuristics = var_sh
		self.valHeuristics = val_sh
		self.cChecks = cc

	# ==================================================================
	# Consistency Checks
	# ==================================================================

	# Basic consistency check, no propagation done
	def assignmentsCheck ( self ):

		#modConstraints = self.network.getModifiedConstraints()
		#variables = set()
		#assignedVars = set()

		""""
		for c in modConstraints:
			for v in c.vars:
				variables.add(v.getName())
				if v.isAssigned():
					#v.setModified(False)
					assignedVars.add(v.getName())
		#
		print("variables: {}".format(variables))

		print("These should be the most recently assigned vars...")
		print("assignedVars: {}".format(assignedVars))
		"""
		for c in self.network.getConstraints():
			if not c.isConsistent():
				return False
		return True

	"""
		Part 1 TODO: Implement the Forward Checking Heuristic

		This function will do both Constraint Propagation and check
		the consistency of the network

		(1) If a variable is assigned then eliminate that value from
			the square's neighbors.

		Note: remember to trail.push variables before you change their domain
		Return: true is assignment is consistent, false otherwise
	"""
	def forwardChecking ( self ):

		#I think I need to perform constraint propagation here like before?
		#Do I need to assign values that only have one possible choice immediately.
		#But doesn't MRV already get the variables with the lowest domain size first?
		#If I have another list here to get the variables with a single value only and assign those and propagate
		#here?
		#Correction: Do not assign variables in forwardChecking()
		
		#varsWithOneValue = [var for var in self.network.getVariables() if var.size() == 1 and not var.isAssigned()]
		#for var in varsWithOneValue:
		#	var.assignValue(var.getValues()[0])
	
		for var in self.network.getVariables():
			if var.isAssigned() and var.isModified():
				var_value = var.getAssignment()
				neighbors = self.network.getNeighborsOfVariable(var)
				#neighbors = sorted(neighbors, key= (lambda t:t.size()))
				for n in neighbors:
					containsVal = n.getDomain().contains(var_value)
					if containsVal and n.size() == 1:
						#modConstraints = self.network.getModifiedConstraints()
						return False

					elif containsVal and n.size() != 1:
						self.trail.push(n)
						n.removeValueFromDomain(var_value)

					########205 with the elif condiiton
					#elif not containsVal and n.size() == 1 and not n.isAssigned():
						#self.trail.placeTrailMarker()
						#self.trail.push( n )

						#####1111
						#n.assignValue(n.getValues()[0])
						#self.forwardChecking()
						#####
						#####7949
						#n.assignValue(n.getValues()[0])
						#if self.checkConsistency():
						#	self.solve()
						#####

		modConstraints = self.network.getModifiedConstraints()
		return True

	"""
		Part 2 TODO: Implement both of Norvig's Heuristics

		This function will do both Constraint Propagation and check
		the consistency of the network

		(1) If a variable is assigned then eliminate that value from
			the square's neighbors.

		(2) If a constraint has only one possible place for a value
			then put the value there.

		Note: remember to trail.push variables before you change their domain
		Return: true is assignment is consistent, false otherwise
	"""
	def norvigCheck ( self ):
		#print("Inside norvig")
		for var in self.network.getVariables():
			if var.isAssigned() and var.isModified():
				var_value = var.getAssignment()
				#print("###########Propagating {} with value {}".format(var.getName(), var_value))
				neighbors = self.network.getNeighborsOfVariable(var)
				vecinos = [var.getName() for var in neighbors]
				#print("vecinos: {}".format(vecinos))
				#print("About to remove the value from the neighbors...")
				for n in neighbors:
					#print("neighbor (n)...")
					#print()
					#print("{}: {} with size {}".format(n.getName(), n.getValues(), n.size()))

					containsVal = n.getDomain().contains(var_value)
					#print("{} contains value? {}".format(n.getName(), containsVal))
					#print("var is assigned? {}".format(n.isAssigned()))
					if containsVal and n.size() == 1:
						#print("neighbor already has the value")
						return False

					elif containsVal and n.size() != 1:
						# I think i need to call self.network.getModifiedConstraints()
						#
						#print("neighbor will be removed of value")
						self.trail.push(n)
						n.removeValueFromDomain(var_value)
						if n.size() == 1:
							#print("neighbor has size 1 now")
							remainingValue = n.getValues()[0]
							n.assignValue(remainingValue)
							#print("About to recurse")
							#n.setModified(False)
							var.setModified(False)	#####Try removing this next time
							self.norvigCheck()
					
					#I think this elif case here will never run
					#because the MAD and MRV heuristics would have chosen this variable
					#to assign first, since it has a size of 1.
					elif containsVal == False and n.size() == 1 and n.isAssigned() == False:
						#print("neighbor has one value left")
						self.trail.push(n)
						remainingValue = n.getValues()[0]
						n.assignValue(remainingValue)
						var.setModified(False)
						self.norvigCheck()
					"""
					elif containsVal == False and n.size() == 1 and var.isAssigned() == False:
						print("neighbor has domain of size 1")
						self.trail.push(var)
						remainingValue = var.getValues()[0]
						var.assignValue(remainingValue)
						#n.setModified(False)
						print("about to recurse")
						self.norvigCheck()
						#if self.checkConsistency():
						#	self.solve()
					"""
		modConstraints = self.network.getModifiedConstraints()
		return True

	"""
		 Optional TODO: Implement your own advanced Constraint Propagation

		 Completing the three tourn heuristic will automatically enter
		 your program into a tournament.
	 """
	def getTournCC ( self ):
		for var in self.network.getVariables():
			if var.isAssigned() and var.isModified():
				var_value = var.getAssignment()
				#print("###########Propagating {} with value {}".format(var.getName(), var_value))
				neighbors = self.network.getNeighborsOfVariable(var)
				vecinos = [var.getName() for var in neighbors]
				#print("vecinos: {}".format(vecinos))
				#print("About to remove the value from the neighbors...")
				for n in neighbors:
					#print("neighbor (n)...")
					#print()
					#print("{}: {} with size {}".format(n.getName(), n.getValues(), n.size()))

					containsVal = n.getDomain().contains(var_value)
					#print("{} contains value? {}".format(n.getName(), containsVal))
					#print("var is assigned? {}".format(n.isAssigned()))
					if containsVal and n.size() == 1:
						#print("neighbor already has the value")
						return False

					elif containsVal and n.size() != 1:
						# I think i need to call self.network.getModifiedConstraints()
						#
						#print("neighbor will be removed of value")
						self.trail.push(n)
						n.removeValueFromDomain(var_value)
						if n.size() == 1:
							#print("neighbor has size 1 now")
							remainingValue = n.getValues()[0]
							n.assignValue(remainingValue)
							#print("About to recurse")
							#n.setModified(False)
							var.setModified(False)	#####Try removing this next time
							self.norvigCheck()
					
					#I think this elif case here will never run
					#because the MAD and MRV heuristics would have chosen this variable
					#to assign first, since it has a size of 1.
					elif containsVal == False and n.size() == 1 and n.isAssigned() == False:
						#print("neighbor has one value left")
						self.trail.push(n)
						remainingValue = n.getValues()[0]
						n.assignValue(remainingValue)
						var.setModified(False)
						self.norvigCheck()
					"""
					elif containsVal == False and n.size() == 1 and var.isAssigned() == False:
						print("neighbor has domain of size 1")
						self.trail.push(var)
						remainingValue = var.getValues()[0]
						var.assignValue(remainingValue)
						#n.setModified(False)
						print("about to recurse")
						self.norvigCheck()
						#if self.checkConsistency():
						#	self.solve()
					"""
		modConstraints = self.network.getModifiedConstraints()
		return True

	# ==================================================================
	# Variable Selectors
	# ==================================================================

	# Basic variable selector, returns first unassigned variable
	def getfirstUnassignedVariable ( self ):
		for v in self.network.variables:
			if not v.isAssigned():
				return v

		# Everything is assigned
		return None

	"""
		Part 1 TODO: Implement the Minimum Remaining Value Heuristic

		Return: The unassigned variable with the smallest domain
	"""
	def getMRV ( self ):
		#Get unassigned variables from the board
		uVariables = [var for var in self.network.getVariables() if not var.isAssigned()]
		
		#If there are no variables left, return None because all the variables of the board
		#have been assigned
		if len(uVariables) == 0:
			return None

		#Sort the variables by their domain size, in ascending order
		uVariables = sorted(uVariables, key=(lambda v: v.size()))
		
		#Return the first element of the list because it has the smallest domain
		return uVariables[0]

	"""
		Part 2 TODO: Implement the Minimum Remaining Value Heuristic
					   with Degree Heuristic as a Tie Breaker

		Return: The unassigned variable with, first, the smallest domain
				and, second, the most unassigned neighbors
	"""
	def MRVwithTieBreaker ( self ):
		#print("INSIDE MRVTIEBREAKER")
		#Get unassigned variables from the board
		uVariables = [var for var in self.network.getVariables() if not var.isAssigned()]

		#All the variables of the board have been assigned 
		if len(uVariables) == 0:
			return None

		#Sort the variables by their domain size, in ascending order
		uVariables = sorted(uVariables, key = (lambda v: v.size()))
		#test1 = [(var.getName(), var.size()) for var in uVariables]
		#print("test1: {}".format(test1))

		#Use the first variable of the list to see if there are ties present (i.e. the variable w/ the minimum remaining values)
		firstVar = uVariables[0]

		#List of vars with the same "small" size
		varsSameSize = [var for var in uVariables if var.size() == firstVar.size()]
		
		#Add the var into this list
		#varsSameSize.append(firstVar)
		#test2 = [(var.getName(), var.size()) for var in varsSameSize]
		#print("test2: {}".format(test2))

		#Return the unassigned variable with the smallest domain
		if len(varsSameSize) == 1:
			return uVariables[0]

		myPairs = []
		for var in varsSameSize:
			data = None			#(var, degree)
			neighbors = [v for v in self.network.getNeighborsOfVariable(var) if not v.isAssigned()]
			data = (var, len(neighbors), var.getName())
			myPairs.append(data)

		myPairs = sorted(myPairs, key=(lambda t: -t[1]))
		#test3 = [(v[2], v[1]) for v in myPairs]
		#print("test3: {}".format(test3))

		#print("returning...: {}".format(myPairs[0][2]))

		return myPairs[0][0]

	"""
		 Optional TODO: Implement your own advanced Variable Heuristic

		 Completing the three tourn heuristic will automatically enter
		 your program into a tournament.
	 """
	def getTournVar ( self ):
		uVariables = [var for var in self.network.getVariables() if not var.isAssigned()]
		
		if len(uVariables) == 0:
			return None

		uVariables = sorted(uVariables, key=(lambda v : v.size()))

		return uVariables[0]

	# ==================================================================
	# Value Selectors
	# ==================================================================

	# Default Value Ordering
	def getValuesInOrder ( self, v ):
		values = v.domain.values
		return sorted( values )

	"""
		Part 1 TODO: Implement the Least Constraining Value Heuristic

		The Least constraining value is the one that will knock the least
		values out of it's neighbors domain.

		Return: A list of v's domain sorted by the LCV heuristic
				The LCV is first and the MCV is last
	"""
	def getValuesLCVOrder ( self, v ):
		lcv = []				#[(v_value_1, num_remain_values_neighbors),(v_value_2, num_values_neihbros), ...]
		result = []				#[value_v_1, value_v_2, ...]

		#Values of variable v
		values = v.getValues()
		
		#if len(values) == 1:
		if len(values) < 2:
			return values

		#Get neighbors of v
		neighbors = self.network.getNeighborsOfVariable(v)

		for val in values:
			val_result = None	#(value, resultingNumberOfValuesOfAllNeighbors)
			numValues = 0		#Counter for the size of each neihgbor's domain after removing val from it 
			for n in neighbors:
				domainOfNeighbor = n.getValues().copy()
				if val in domainOfNeighbor:
					domainOfNeighbor.remove(val)
				
				numValues += len(domainOfNeighbor)
			
			val_result = (val, numValues)
			lcv.append(val_result)

		#Sort the list of tuples so that the first element is the least constraining value
		lcv = sorted(lcv, key=(lambda t: -t[1]))
		
		#Trying to improve backtracks by sorting by both the value and the number of remaining values of all the neighbors
		#lcv = sorted(lcv, key=(lambda t: (-t[1], t[0])))

		#Extract the values from the sorted list and return the values
		for element in lcv:
			result.append(element[0])
		
		return result
	

	"""
		 Optional TODO: Implement your own advanced Value Heuristic

		 Completing the three tourn heuristic will automatically enter
		 your program into a tournament.
	 """
	def getTournVal ( self, v ):
		values = v.domain.values
		return sorted(values)

	# ==================================================================
	# Engine Functions
	# ==================================================================

	def solve ( self ):
		if self.hassolution:
			return

		# Variable Selection
		v = self.selectNextVariable()
		#print("NEXT VARIABLE...")
		#print(v)

		# check if the assigment is complete
		if ( v == None ):
			for var in self.network.variables:

				# If all variables haven't been assigned
				if not var.isAssigned():
					print ( "Error" )

			# Success
			self.hassolution = True
			return

		# Attempt to assign a value
		for i in self.getNextValues( v ):
			#print("IN FOR LOOP...")
			#print(v)
			#print("i: {}".format(i))

			# Store place in trail and push variable's state on trail
			self.trail.placeTrailMarker()
			self.trail.push( v )

			# Assign the value
			v.assignValue( i )
			#print("Assignment occurred...")
			#print(v)

			# Propagate constraints, check consistency, recurse
			if self.checkConsistency():
				#print("CHECKED CONSISTENCY...")
				#print("var: {} was consistent w/ value {}".format(v.getName(), i))
				#print(self.getSolution())
				self.solve()

			# If this assignment succeeded, return
			if self.hassolution:
				return

			# Otherwise backtrack
			#print("Backtracking...")
			self.trail.undo()

	def checkConsistency ( self ):
		if self.cChecks == "forwardChecking":
			return self.forwardChecking()

		if self.cChecks == "norvigCheck":
			return self.norvigCheck()

		if self.cChecks == "tournCC":
			return self.getTournCC()

		else:
			return self.assignmentsCheck()

	def selectNextVariable ( self ):
		if self.varHeuristics == "MinimumRemainingValue":
			return self.getMRV()

		if self.varHeuristics == "MRVwithTieBreaker":
			return self.MRVwithTieBreaker()

		if self.varHeuristics == "tournVar":
			return self.getTournVar()

		else:
			return self.getfirstUnassignedVariable()

	def getNextValues ( self, v ):
		if self.valHeuristics == "LeastConstrainingValue":
			return self.getValuesLCVOrder( v )

		if self.valHeuristics == "tournVal":
			return self.getTournVal( v )

		else:
			return self.getValuesInOrder( v )

	def getSolution ( self ):
		return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)
