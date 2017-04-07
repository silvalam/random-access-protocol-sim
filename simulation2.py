# Project 2 Part 2
# Simulation to compare TCP Congestion Control algorithms.
# Comparing exponential backoff and linear backoff.

import simpy
import random
from socket import *

class node:
	def __init__(self, lmbda, env):
		self.lmbda = lmbda
		self.S = 0
		self.N = 0
		self.L = 0
		self.env = env

	#enqueue packet
	def enqueue(self, env):
		while True:
			self.L += 1
			end_of_queueing_period = random.expovariate(self.lmbda)
			yield env.timeout(end_of_queueing_period)

class network:
	def __init__(self, env, queues):
		self.env = env
		self.listofnodes = queues

	def simulate(self, env, b): # if b = 0 then linear, else if b = 1 then exponential backoff
		global successful_transmissions 
		global envTimeSlot
		for i in range(10):
			env.process(self.listofnodes[i].enqueue(self.env))
	 	while True:
	 		rdy_to_transmit = 1
	 		for nde in listofnodes: # find competing nodes trying to transmit
	 			if nde.L and (nde.S <= envTimeSlot): # if node has something to send and is in this time slot
	 				rdy_to_transmit -= 1 # if ready to transmit is equal to zero, it's ready to transmit
	 				nde.S = envTimeSlot # give node the current period to transmit
	 				if rdy_to_transmit == 0:
	 					transmittingNode = nde # this node is allowed to transmit
	 				if not b: # decide if we are doing linear or exponential backoff
	 					nde.S += random.randint(0, min(nde.N, 1024)) 
	 				else:
	 					nde.S += random.randint(0, 2 ** min(nde.N, 10))
					nde.N += 1
			if rdy_to_transmitt == 0: # if no competing nodes then this node can send a packet
				transmittingNode.L -= 1 # one less packet to send from list of packets
				if transmittingNode.L >= 1: # if there are still packets to send
					transmittingNode.S = envTimeSlot + 1 # send the remaining packets in next time slot
					transmittingNode.N = 0 # reset because successfully sent a packet
				successful_transmissions += 1
			envTimeSlot += 1
			yield env.timeout(1)

lmbdas = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
for b in (0,1):
	if b:
		print "Exponential"
	else :
		print "Linear"
	for lmbda in lmbdas:
		listofnodes = []
		envTimeSlot = 0
		successful_transmissions = 0
		env = simpy.Environment()
		for j in range(10):
			listofnodes.append(node(lmbda, env))
		env.process(network(env, listofnodes).simulate(env,b))
		env.run(until=50000)
		throughput = successful_transmissions/float(envTimeSlot)
		print "{0} {1}".format(lmbda, throughput)