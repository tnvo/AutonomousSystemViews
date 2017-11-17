from math import pow

# Graph 1 = distribution of AS classes - 20150801 dataset - see Graph1 Code
# Graph 2 = historygram of AS node degree dist in historygram - 20170991
# Graph 3 = historgram of IP space assigned to each AS - routeviews
# Graph 4 = Recreate pie chart show % distr of ASes to 3 classes

# p2c link: <provider-AS>|<customer-AS>| -1 |<source>
# p2p link: <peer-AS>|<peer-AS>| 0 |<source>
# node degrees= # customers + # peers + # providers
# ASes to which ASi is a provider (direct customers of ASi)
# IP prefixes associated with ASi.
# 2.1 - AS Classes Distribution - uses a different file - code is in separate folder
# This file contain 2.2, 2.3, 2.4, and extra credit portions
# This file will take the different data set, run through it, analyze it and export files with relevant info we'll use

def read_files(data, prefix):
    #Example:
    # 0 | 1 | 2 | 3
    # 5690|40191|0|bgp
    # 5690|395127|-1|bgp
    # 0 and -1 is in index[2]
    fileIn = "20170901.as-rel2.txt"
    # Create a list to lookup data for determining provider node
    # This list negates the need to reopen the file
    lookupProvider = []
    #open AS file and read through each line, splitting each by pipe
    with open(fileIn) as file:
        for line in file:
            # Don't need this bc with takes care of closing file at the end, and it's reading + printing 1 line at a time 
            # line = line.rstrip('\n')
            index = line.split('|')
            indexQ = [] # this local list is inserted into the lookup Queue
            if index[0] not in data:
                data[index[0]] = {'as_links': {'p2c': [],
                                               'p2p': [],
                                               'prov': []
                                              },
                                       'degree': 0,
                                       'class': 'NA',
                                       'prefix': [], # if data doesn't exist
                                       'length': 'NA'
                                 }
            # figure out the link
            # customer (p2c link)]

            if index[2] == '-1':
                data[index[0]]['as_links']['p2c'].append(index[1])
            # peers - p2p-link
            elif index[2] == '0':
                data[index[0]]['as_links']['p2p'].append(index[1])
            # create a lookup list for the provider from this parsed line
            indexQ.append(index[0])
            indexQ.append(index[1])
            indexQ.append(index[2])
            lookupProvider.append(indexQ)
    file.close()

    print ("Starting to look up providers")
    # Iterate in parent loop through each a_s value of data at index 0
    for a_s in data:
        # Iterate through each node of the lookup list
        for x in lookupProvider:
            # If the AS value is a customer at offset 1, then add its provider
            # to key value list for 'prov' in data
            if a_s == x[1]:
                data[a_s]['as_links']['prov'].append(x[0])
                # Provider of the node are also added to list

    # open NEW route file
    # Example:
    # 0         1   2
    # 1.3.45.0	24	133741_133948
    # 1.3.54.0	24	133741
    # 36.85.84.0	24	7713_65245 <- prefix_as

    # fileIn = "routeviews-rv2-20171105-1200.txt"
    # with open(fileIn) as file:
    #     for line in file:
    #         # going through the file line by line
    #         index = line.split()
    #         # seperating the weird format if it does exist
    #         prefix_as = index[2].split('_')
    #         # getting the range of the IP prefixes
    #         # once split, index[0] is min and index[1] is max
    #         for a_s in prefix_as:
    #             if ',' in a_s:
    #                 set_as = a_s.split(',')
    #                 for sub_as in set_as:
    #                     if sub_as in data:
    #                         data[sub_as]['prefix'] = index[0]
    #                         data[sub_as]['length'] = index[1]
    #             elif a_s in data:
    #                 data[a_s]['prefix'] = index[0]
    #                 data[a_s]['length'] = index[1]
    # file.close()


    # print("Open route file again for degree...")
    fileIn = "routeviews-rv2-20171105-1200.txt"
    with open(fileIn) as file:
        for line in file:
            # going through the file line by line
            index = line.split()
            # seperating the weird format if it does exist
            prefix_as = index[2].split('_')
            # getting the range of the IP prefixes
            # once split, index[0] is min and index[1] is max
            for a_s in prefix_as:
                # also seperating out some lines that has the comma to split them
                #if ',' in a_s:
                set_as = a_s.split(',')
                # after split, use each of the value and add it to array
                # sub_as is under the AS set and is subsequent to the as list
                for sub_as in set_as:
                    if sub_as not in data:
                        data[sub_as] = {'as_links': {'p2c': [],
                                                'p2p': [],
                                                'prov': []
                                                },
                                                'degree': 0,
                                                'class': 'NA',
                                                'prefix': [],
                                                'length': 'NA'}
                if not data[sub_as]['prefix'].count(index[0] + '/' + index[1]):
                    data[sub_as]['prefix'].append(index[0] + '/' + index[1])
                    prefix.add(index[0] + '/' + index[1])


                    # through the different scenarios, this step will
                    # add all the values to the array, the close the file once it's done

    file.close()

# create a new file with info that we actually use
def write_new_file(data, t1, n_prefix):
    output_data_file = "AS.txt"
    with open(output_data_file, "w+") as w:
        # writing each line to a new txt file
        # print at the 1st line of new text file
        print('AS | Node Degree | Node Degree (With Providers) | Prefix Count | AS Class', file=w)
        # going through each line in our dataset and print out useful info
        for a_s in data:
            # no. of customers
            p2c_len = len(data[a_s]['as_links']['p2c'])
            # no. of peers
            p2p_len = len(data[a_s]['as_links']['p2p'])
            # no. of providers
            prov_len = len(data[a_s]['as_links']['prov'])
            # degrees
            deg = data[a_s]['degree']
            # prov degrees:
            degWProv = data[a_s]['degreeProv']
            # prefixes
            pre = len(data[a_s]['prefix'])
            # length
            d_len = data[a_s]['length']
            # d_class
            d_class = data[a_s]['class']
            # printing each of the array from the json file created above and dump it to a text file separated by columns
            print('AS: {} | Node Degree: {} | Node Degree(+Prov): {} | IP Prefix: {} | AS Class: {} | Customers: {} | Peers: {} | Providers: {}'.format(a_s, deg, degWProv, pre, d_class, p2c_len, p2p_len, prov_len), file=w)
    # done - closing the file
    w.close()

    # 2.3 writing out t1 to new file
    output_data_file = "2.3 - t1_inference.txt"
    with open(output_data_file, "w+") as w:
        # size of T1 list and first (or up to) 10 ASes that were added to S
        # out of range error (only produce 5 results), can't use range
        # should be 10, but it was only returning 5 and have an error for out of range
        # so setting it at 5 for now
        for a_s in range(10):
            if t1[a_s]:
        #for a_s in t1:
            # look for the top 10 largest clique
            #if t1.index(a_s) == 10:
                #break
                # print them to a new file with the AS numbers
                # this AS number can be used against the organization files
                # to figure out the company name & org info
                print('#{} - {}'.format(a_s + 1, t1[a_s]), file=w)
        print('{}'.format(len(t1)), file=w)
    # done - closing the file
    w.close()

    # extra credit portion
    # writing out customer cones info
    # this is extra credit
    print ("Beginning to write out customer cones file")
    # this will print both table 4.1 & 4.2 e.c to cCone.txt
    output_data_file = "cCones.txt"
    with open(output_data_file, "w+") as w:
        # header of the file
        print('2.4 Extra Credit Result', file=w)
        # 2.4 - E.C Part 1 - Sorted by cone size based on #'s of ASes
        #sorting by cone size
        print('----------------------------------------------', file=w)
        print('TABLE 1 - SORTING BASED ON SIZE', file=w)
        print('Rank | AS# | AS name | AS degree | #s ASes | IP Prefix | IPs | Percent ASes | IP Prefix | Ips', file=w)
        size_rank = sorted(data, key=lambda k: data[k]['cCone']['cone_size'], reverse=True)
        # sorting by IP
        ip_rank = sorted(data, key=lambda k: data[k]['cCone']['ip_Pct'], reverse=True)
        # get only the top 15 values
        for a_s in size_rank[:15]:
            # rank, AS#, AS name, AS degree, #'s ASes, IP Prefix, IPs, % ASes, IP Prefix, Ips
            print('{} | {} | {} | {} | {} | {} | {} | {} | {} | {}'.format(size_rank.index(a_s) + 1, a_s,
                                                                  'Org_Name', data[a_s]['degree'],
                                                                  data[a_s]['cCone']['cone_size'],
                                                                  len(data[a_s]['cCone']['prefix']),
                                                                  data[a_s]['cCone']['ips'],
                                                                  data[a_s]['cCone']['as_Pct'],
                                                                  data[a_s]['cCone']['prefix_Pct'],
                                                                  data[a_s]['cCone']['ip_Pct']), file=w)

        # print out 4.2 table
        print('\n\n----------------------------------------------\n', file=w)
        print('TABLE 2 - SORTING BASED ON IP PERCENTAGE', file=w)
        print('Rank | AS# | AS name | AS degree | #s ASes | IP Prefix | IPs | Percent ASes | IP Prefix | Ips', file=w)
        for a_s in ip_rank[:15]:
            print('{} | {} | {} | {} | {} | {} | {} | {} | {} | {}'.format(ip_rank.index(a_s) + 1, a_s,
                                                                  'Org_Name', data[a_s]['degree'],
                                                                  data[a_s]['cCone']['cone_size'],
                                                                  len(data[a_s]['cCone']['prefix']),
                                                                  data[a_s]['cCone']['ips'],
                                                                  data[a_s]['cCone']['as_Pct'],
                                                                  data[a_s]['cCone']['prefix_Pct'],
                                                                  data[a_s]['cCone']['ip_Pct']), file=w)
        w.close()



# 2.2 - Historgram of node degree
# figure out the numbers of node degree in the dataset
def n_degree(data):
    for a_s in data:
        data[a_s]['degree'] = len(data[a_s]['as_links']['p2c']) + len(data[a_s]['as_links']['p2p'])
        data[a_s]['degreeProv'] = len(data[a_s]['as_links']['p2c']) + len(data[a_s]['as_links']['p2p'])+len(data[a_s]['as_links']['prov'])
        # Classifying and figuring out
        # Enterprise ASes: any AS with degree less or equal to two and no customers or peers.
        if data[a_s]['degree'] <= 2 and len(data[a_s]['as_links']['p2c']) == 0 and len(data[a_s]['as_links']['p2p']) == 0:
            data[a_s]['class'] = 'Enterprise'
        # Content AS: Any AS with no customers and at least one peer.
        elif len(data[a_s]['as_links']['p2c']) == 0 and len(data[a_s]['as_links']['p2p']) >= 1:
            data[a_s]['class'] = 'Content'
        # Transit AS: Any AS with at least one customer.
        elif len(data[a_s]['as_links']['p2c']) >= 1:
            data[a_s]['class'] = 'Transit'


# Sort to rank all ASes according to their degree and place them to set R later
# def sort_degree(data):
#     print("Begin sorting...")
#     as_list = list(data.keys())
#     sorted_as = []
#     print("Preparing to sort through all AS degrees...")
#     while as_list:
#         maximum = as_list[0]
#         for a_s in as_list:
#             if data[a_s]['degree'] > data[maximum]['degree']:
#                 maximum = a_s
#         sorted_as.append(maximum)
#         as_list.remove(maximum)
#     print("Finishing the sorting process for AS degrees...")
#     return sorted_as

# 2.3 - Inference of T1 ASes
def t1(data):
    # rank all ASes according to degree
    # initialize S
    R = sorted(data, key=lambda t: data[t]['degree'], reverse=True)
    S = [R[0]]
    #next_as = 1
    #connected = True
    print ("Applying simple greedy heuristic now...")
    # running simple greedy heuristic
    # If AS2 is connected to AS1, add it to S
    # If AS3 is connected to AS1 and AS2, add it to S.
    # while connected:
    #     for a_s in S:
    #         if (R[next_as] not in data[a_s]['as_links']['p2p']) and (R[next_as] not in data[a_s]['as_links']['p2c'] and (a_s not in data[R[next_as]]['as_links']['p2p']) and (a_s not in data[R[next_as]]['as_links']['p2c'])):
    #             connected = False
    #             break
    #     if connected:
    #         S.append(R[next_as])
    #         next_as += 1
    for node in R[1:]:
        connected = True
        for a_s in S:
            if (node not in data[a_s]['as_links']['p2p']) and (node not in data[a_s]['as_links']['p2c'] and (a_s not in data[node]['as_links']['p2p']) and (a_s not in data[node]['as_links']['p2c'])):
                connected = False
                break
        if connected:
            S.append(node)
    return S

# p2c customers cone links
# calculate # of cone
def n_cone(all, n_ips, n_prefix):
    print("Almost there....")
    def dfs(data, current_node, visited=None):
        if current_node in data:
            for child in data[current_node]['as_links']['p2c']:
                dfs(data, child, visited)
        return visited.add(current_node)

    print("Half way done with cone stuffs ...")

    for a_s in all:
        # print("dfs-ing a_s: {}".format(a_s))
        n_cone = set()
        n_pref = set ()
        dfs(all, a_s, visited=n_cone)
        # cCone = customer cone
        all[a_s]['cCone'] = {}
        all[a_s]['cCone']['cone'] = n_cone
        all[a_s]['cCone']['cone_size'] = len(n_cone)

        # running through loop for prefixes in customer cone
        for cone_a_s in all[a_s]['cCone']['cone']:
            if cone_a_s in all:
                for x in all[cone_a_s]['prefix']:
                    n_pref.add(x)
        all[a_s]['cCone']['prefix'] = n_pref

        ips = 0
        for pref in all[a_s]['cCone']['prefix']:
            # print (pref)
            sbits = int(pref.split('/')[1])
            ips += pow(2, 32 - sbits)
        all[a_s]['cCone']['ips'] = ips
        all[a_s]['cCone']['as_Pct'] = len(all[a_s]['cCone']['cone']) / len(all)
        all[a_s]['cCone']['prefix_Pct'] = len(all[a_s]['cCone']['prefix']) / len(n_prefix)
        all[a_s]['cCone']['ip_Pct'] = all[a_s]['cCone']['ips'] / n_ips

# Calling and running function from above now
print("Running functions now (0%)")
# Run functions
# all of the data now
all = {}
all_prefixes = set()
print("Reading files")
read_files(all, all_prefixes)

# IP + IP prefixes Count
# For 2.3 - IP Classes distribution
print("Calculating IPs (10%)")
n_ips = 0
for pf in all_prefixes:
    sbits = int(pf.split('/')[1])
    n_ips += pow(2, 32 - sbits)

print("Calculating number of node degree... (20%)")
n_degree(all)

print("Running t1 (30%)")
print("This step might take awhile... (40%)")
t1 = t1(all)

print("Running numbers of cone... (50%)")
print("Might take another little while... (55%)")
n_cone(all, n_ips, all_prefixes)

print("Writing useful data to a new file... (90%)")
write_new_file(all, t1, n_ips)

print("Finished (100%)")
