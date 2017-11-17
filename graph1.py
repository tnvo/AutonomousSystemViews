import matplotlib.pyplot as plt

# open file and read line starting from line 6 (before are all comments)
inputFile = open('20150801.as2types.txt', 'r')
readFile = inputFile.readlines()
readFile = readFile[6:]
data = []

for line in readFile:
    field = line.split('|')
    field[-1] = field[-1].rstrip()
    data.append(field)

# initialize count
tCount = 0
cCount = 0
eCount = 0
totalCount = 0

# looking for matching fields
for x in data:
    if x[2] == 'Transit/Access':
        tCount += 1
    elif x[2] == 'Content':
        cCount += 1
    elif x[2] == 'Enterpise':
        eCount += 1
    totalCount += 1

    # Calculate percentage for enterprise
    tPer = tCount/totalCount;
    # Calculate percentage for transit/access
    cPer = cCount/totalCount;
    # Calculate percentage for content
    ePer = eCount/totalCount;

    dataArray = [tPer, cPer, ePer]

labels = ['Transit/Access', 'Content', 'Enterprise']
plt.pie(dataArray, labels=labels, autopct = "%1.3f%%")
plt.title('Graph 1 - % of AS Distribution')
plt.show()

inputFile.close()
