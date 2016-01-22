import pdb
import matplotlib.pyplot as plt

file_dir = 'data/'
data = []

###########################
# Load Similiarity Values #
###########################

similarity_file = open(file_dir + 'similarity.txt', 'r')

for line in similarity_file:
	if line != '\n':
		point = line[:-1]
		doc, simvalue = point.split(',')
		doc = int(doc.translate(None, '('))
		simvalue = float(simvalue.translate(None, ') '))
		data.append((doc, simvalue))

similarity_file.close()

###########################

#################
# Plot Creation #
#################

plt.axis([0, 11000, -1, 1])
plt.ylabel('Similiarity Value')
plt.xlabel('Document Number')
plt.title('Query: smoke free')

for datum in data:
	plt.plot(datum[0], datum[1], 'ro')

plt.show()

#################
