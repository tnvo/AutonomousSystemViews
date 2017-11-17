# Graph 2.2

# p2c link: <provider-AS>|<customer-AS>| -1 |<source>
# p2p link: <peer-AS>|<peer-AS>| 0 |<source>
# node degrees= # customers + # peers + # providers
# ASes to which ASi is a provider (direct customers of ASi)
# IP prefixes associated with ASi.


def read_files(data):
    fileIn = "20170901.as-rel2.txt"

    #Example:
    # 0 | 1 | 2 | 3
    # 5690|40191|0|bgp
    # 5690|395127|-1|bgp
    # 0 and -1 is in index[2]

    # Create a list to lookup data for determining provider node
    # This list negates the need to reopen the file
    lookupProvider = []

    #open AS file and read through each line, splitting each by pipe

    with open(fileIn) as file:

        for line in file:
            line = line.rstrip('\n')
            index = line.split('|')
            indexQ = [] # this local list is inserted into the lookup Queue


            if index[0] not in data:

                data[index[0]] = {'as_links': {'p2c': [],
                                               'p2p': [],
                                               'pro': []
                                              },
                                       'prefix': 'NA', # if data doesn't exist
                                       'length': 'NA'}
            # figure out the link
            # customer (p2c link)
            if index[2] == '-1':
                data[index[0]]['as_links']['p2c'].append(index[1])
                # create a lookup list for the provider from this parsed line
                indexQ.append(index[0])
                indexQ.append(index[1])
                indexQ.append(index[2])
                lookupProvider.append(indexQ)

            # peers - p2p-link
            elif index[2] == '0':
                data[index[0]]['as_links']['p2p'].append(index[1])
    file.close()
    print ("Print lookupProvider")
    # Iterate in parent loop through each a_s value of data at index 0
    for a_s in data:
        # Iterate through each node of the lookup list
        for x in lookupProvider:
            # If the AS value is a customer at offset 1, then add its provider
            # to key value list for 'pro' in data
            if a_s == x[1]:
                data[a_s]['as_links']['pro'].append(x[0])

    # open NEW route file
    # Example:
    # 0         1   2
    # 1.3.45.0	24	133741_133948
    # 1.3.54.0	24	133741
    # 36.85.84.0	24	7713_65245 <- prefix_as

    fileIn = "routeviews-rv2-20171105-1200.txt"
    with open(fileIn) as file:
        for line in file:
            index = line.split()
            prefix_as = index[2].split('_')
            # getting the range of the IP prefixes
            # once split, index[0] is min and index[1] is max
            for a_s in prefix_as:
                if ',' in a_s:
                    set_as = a_s.split(',')
                    for sub_as in set_as:
                        if sub_as in data:
                            data[sub_as]['prefix'] = index[0]
                            data[sub_as]['length'] = index[1]
                elif a_s in data:
                    data[a_s]['prefix'] = index[0]
                    data[a_s]['length'] = index[1]
    file.close()

# create a new file with info that we actually use
def write_new_file(data):
    output_data_file = "AS_Node_Count.txt"
    with open(output_data_file, "w+") as w:
        # writing each line to a new txt file
        for a_s in data:
            print('AS: {} | n_node_degree: {}'.format(a_s, data[a_s]['degree'], data[a_s]['prefix'] + '/' + data[a_s]['length']), file=w)
    w.close()

# 2.2 - Historgram of node degree
# figure out the numbers of node degree in the dataset
def n_degree(data):
    for a_s in data:
        data[a_s]['degree'] = len(data[a_s]['as_links']['p2c']) + len(data[a_s]['as_links']['p2p'])+len(data[a_s]['as_links']['pro'])

# Calling and running function from above now
print("Running functions now")
# Run functions
# all of the data now
all = {}

print("Reading files")
read_files(all)

print("Calculating number of node degree...")
n_degree(all)

print("Writing useful data to a new file...")
write_new_file(all)

print("Finished")
