"""
This describes the steps needed to run the evolution in the latent space from Python:

Python code for CMA-ES is not currently included in the repository. 
Instead, it must be installed by following the instructions here:
https://pypi.python.org/pypi/cma
Basically, run:
python -m pip install cma

Next, the Python code requires the Java code to be compiled into
an executable jar file. Currently, the main class of such jar file
creation should be ch.idsia.scenarios.MainRun, but we may change
this (for example, to ch.idsia.scenarios.GANEvaluator). In Eclipse, this
can be done with the export command in the File menu.

Either way, the Java class that we choose to run must accept
raw json Strings and also print out fitness eval info in order
for the Python program to capture the fitness scores.

Currently, CMAMarioGan.py can be run in Python. It requires command
line parameters specifying the Keras model, just like generator.py.
Specifically, try:
python CMAMarioGan.py generator.json generator.h5

This will run the program, and you will see Mario levels evaluated,
but currently, the levels are not generated by the GAN. This is why
the Java program needs to accept a different type of command line
parameters.
"""

# Imports for the GAN
import sys
import json
import numpy
from keras.models import model_from_json
# Imports for evolution
import cma
# for communicating with Java
from subprocess import call

def marioAStarGAN(x):
	z = numpy.array(x)
	z = numpy.reshape(z,[-1,16]) # Not entirely clear why this is needed
	# Take latent vector and generate level
	levels = model.predict(z).argmin(-1)
	# TODO: Launch Mario Java with levels[0]
	# TODO: Add the json representation of the level as a command-line parameter
	call(["java","-jar","marioaiDagstuhl/marioaiDagstuhl.jar", "-lf ["+levels[0]+"]"])
	# TODO: Have Java program output fitness score to stdout
	# TODO: Capture that output in Python and return from this function
	return 0 # TODO: Change
	
if __name__ == '__main__':
	global model # for use in fitness calculation
	# Code from Adam's original generator.py to load a saved model
	_, architecture_filename, weights_filename = sys.argv
	with open(architecture_filename) as f:
		model = model_from_json(f.read())
	model.load_weights(weights_filename, True)
	# Run CMA-ES
	es = cma.CMAEvolutionStrategy(16 * [0], 1/math.sqrt(16))
	es.optimize(marioAStarGAN)
