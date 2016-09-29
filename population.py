"""
population.py
~~~~~~~~~~~~~
This stores a fixed set of genomes, and provides methods to
create new generations based on the existing one.
"""
import random
from itertools import product
from genome import Genome
from operator import attrgetter

SIZE = 100
BAD_SCORE = 1000

class Population:
	def __init__(self, operations):
		self.genomes = []
		self.create_new_population(operations)
		self.sort_population()
		self.reap_population()

	def __str__(self):
		genomes_string = ""
		for genome in self.genomes:
			genomes_string += str(genome)
		return genomes_string

	def create_new_population(self, operations):
		permutations = product(operations, repeat=len(operations))
		for _ in range(SIZE * 1000):
			random.shuffle(operations)
			genome = Genome(operations[:])
			genome.score = calculate_fitness(genome.operations)
			self.genomes.append(genome)

	def sort_population(self):
		"""
		Sorts the population based on the fitness score
		"""
		self.genomes.sort(key = attrgetter('score'), reverse = False)

	def reap_population(self):
		"""
		Keeps only the first SIZE individuals
		"""
		self.genomes = self.genomes[:100]

	def reproduce_population(self):
		"""
		The miracle of life
		"""
		pass

def calculate_fitness(permutation):
	penalization = 0
	if not is_valid_permutation(permutation):
		penalization = BAD_SCORE
	make_span = calculate_makespan(permutation)
	score = make_span + penalization
	return score


def is_valid_permutation(permutation):
	operation_done = {}
	for op in permutation:
		operation_done[op] = 0

	for op in permutation:
		for dep in op.dependencies:
			if operation_done[dep] == 0:
				return False
		operation_done[op] = 1
	return True

def calculate_makespan(permutation):
	cummulative_machine_times = {}
	operations_end_time = {}
	jobs_end_time = {}

	for operation in permutation:
		#initialize variables with 0 if does not exist
		if not operation in operations_end_time:
			operations_end_time[operation] = 0

		if not operation.machine in cummulative_machine_times:
			cummulative_machine_times[operation.machine] = 0

		#Check if the operation has dependencies
		if operation.dependencies:

			#initialize time of the operation to the max value of dependencies
			max_time_dependencies = operations_end_time[operation.dependencies[0]]
			for dependent_operation in operation.dependencies:
				if operations_end_time[dependent_operation] > max_time_dependencies:
					max_time_dependencies = operations_end_time[dependent_operation]
			operations_end_times[operation] = max_time_dependencies


		#Calculate time
		if operations_end_time[operation] < cummulative_machine_times[operation.machine]:
			cummulative_machine_times[operation.machine] += operation.duration
			operations_end_time[operation] = cummulative_machine_times[operation.machine]
		else:
			operations_end_time[operation] += operation.duration
			cummulative_machine_times[operation.machine] = operations_end_time[operation]

		"""Save the time of each operation.
		 So, at the end you have the last one is the one saved """
		jobs_end_time[operation.job_id] = operations_end_time[operation]



	"""Return a map mapping each job with the corresponding end time,
	 and the biggest time of the jobs"""
	return jobs_end_time, jobs_end_time[max(jobs_end_time, key=jobs_end_time.get)]
