
######################################################################
# You will need these modules.
import csv
######################################################################
# Specification: opens file and reads all the records, returning a
# list of dictionaries, each one representing a line or record from
# the original data file. Use the Python CSV DictReader object
# (https://docs.python.org/3.6/library/csv.html) to input the data.
#
# As you read in values, you should preferentially convert those
# values to (i) int, (ii) float or, failing those, leave them as (iii)
# strings. Use the helper function convert() to perform the
# conversion.
#
# Produces a list of dictionaries, where each dictionary looks like, e.g.,
#    {'Country':'USA', 'ClassGrade':12, 'Gender':'Female', ... }
#
def getData(file='data.csv'):
    def convert(value):
        try:
            return(int(value))
        except:
            try:
                return(float(value))
            except:
                return(value)
    data = []
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            for key in row.keys():
                row[key] = convert(row[key])
            data.append(row)
            #print(len(data))
    print("Read {} records.".format(len(data)))
    return(data)

######################################################################
# Specification: takes a list of dictionaries such as those produced
# by getData() or select(), an outcome you wish to predict (an
# attribute from the original data file), and a set of field
# specifications upon which you wish to base your prediction.
#
# This function returns a deeply nested dictionary of dictionaries,
# where the "outer dictionary" has keys corresponding to possible
# outcomes (the second argument), each of which has a value that is a
# dictionary of dictionaries. These "inner dictionaries" have values
# that correspond to the field specifications (the third argument)
# which are themselves dictionaries ("distributions") of field
# value/count pairings. An example should make this clear.
#
# Assume you wish to predict gender from longest foot and height in
# centimeters. Here is the correct invocation:
#
#   train(getData('input.csv'), 'Gender', ('Longer_foot', ('Height_cm', 140, 199, 10)))
#
# where the outcome is 'Gender' which you desire to learn how to
# predict from 'Longer_foot' and 'Height_cm' alone (details of how to
# read the evidence tuple to follow; for now, just note that the
# outcome must be an attribute of the original data, as are the
# elements of the specified evidence tuple).
#
# Assuming input.csv contains 58 records with 'Gender' values (records
# with missing values for 'Gender' are ignored), of which 40 are male
# and 18 are female, we might get a result that looks like this:
#
#   {'Male':{'Longer_foot':{'Right_foot':13, 'Left_foot':27, 'Total':40}, 'Height_cm':{140:0, 150:2, ... 190:8, 'Total':38}, 'Total':40},
#    'Female':{'Longer_foot':{'Right_foot':8, 'Left_foot':5, 'Total':13}, 'Height_cm':{140:0, 150:4, ... 190:0, 'Total':16}, 'Total':18}}
#
# A few things are notable. First, note the extra 'Total' fields
# associated with the "inner dictionaries" associated each outcome for
# 'Gender'; these report the total number of their respective outcome
# in the input (40 males, 18 females).
#
# Second, note that the "distributions" (the innermost dictionaries)
# # also have 'Total' fields, which from which we can see that some
# # attribute values were also missing (e.g., only 38 of 40 males and 16
# # of the 18 females reported their heights).
#
# Both the outcome and the elements of the evidence tuple may be (i)
# an attribute name (in which case the attribute values are assumed to
# be strings, selected from a finite set of values, as for
# 'Longer_foot' in the example above) or (ii) a tuple consisting of an
# attribute name followed by a range() like specification (as for
# 'Height_cm' in the example above). In this latter case, the values
# are assumed to be numeric, and are separated into a fixed number of
# "bins" as specfied by the range() like specification.
#
# Missing values in the input records are ignored (but not tallied in
# the respective 'Total' fields). Also, numeric input values obtained
# when expecting a string (case i above) are converted to strings,
# while string values obtained when expecting a numeric value (case ii
# above) are, like missing values, ignored.
#
def train(D, outcome , evidence):

    import copy

    # 记录数据集字段的数据类型

    Attribution_Type = dict(copy.copy(D[0]))

    for key in Attribution_Type:

        Attribution_Type[key] = type(Attribution_Type[key])

    if outcome not in Attribution_Type:

        raise AttributeError('No attribution "%s" in DataSet' % outcome )



    evi_counter = {"Total": 0} #这个字典用于记录每个evidence的记数

    evi_attris = [] #这个字典用于记录evidence的字段

    numeric_attri_bin = {

    }#evidence是数值类型的话 记录最小分组 最大分组 与间隔

    unique_str_evi = {

    }#evidence是字符串类型的话 记录其不同的值

    for evi in evidence:

        #对于参数evidence,首先找到evidence的字段名字 evi_attri

        if isinstance(evi,str):

            evi_attri = evi

        elif isinstance(evi,tuple):

            evi_attri = evi[0]

        else:

            raise ValueError("Wrong value of argument evidence")


        evi_attris.append(evi_attri)


        #如果数据集里面没有这个字段,所以是无效的evidence
        if evi_attri not in Attribution_Type:

            raise AttributeError('No attribution "%s" in DataSet' % evi_attri)


        #evi_counter里面加入这个evidence，并开始记数
        evi_counter[evi_attri] = {"Total" : 0}


        #如果不是字符串字段
        if Attribution_Type[evi_attri] != str:

            start = evi[1] #找到数值字段的最小分组

            end  = evi[2] #最大分组

            interval = evi[3] #分组长度

            numeric_attri_bin[evi_attri] = [start,end,interval]

            #初始化每个分组的记数为0
            while  start <= end:

                evi_counter[evi_attri][start] = 0

                start += interval
        #如果是字符串字段
        else:
            unique_str_evi[evi_attri] = []

    results = {"Total":0}

    for record in D:

        record_outcome = record[outcome] #找到这条记录所要预测的值

        if record_outcome == "":

            continue

        if record_outcome not in results:

            results[record_outcome] = copy.deepcopy(evi_counter) #结果里面还没有出现预测的这个值，往字典里添加并开始记数evidence

            #输出类似结果为 {outcome1 :evi_counter,outcome2:evi_counter},但是每个outcome的记数字典是不一样的 所以要copy(evi_counter),evi_counter相当于记数字典的一个格式
        results[record_outcome]["Total"] += 1

        results["Total"] +=1
        #记数这条记录的evidence

        for evi_attri in evi_attris:

            record_evi_value = record[evi_attri]

            if record_evi_value == "":

                continue


            if evi_attri == "Height_cm" and isinstance(record_evi_value,str) :

                continue



            if Attribution_Type[evi_attri] != str:

                #数值evidence 进行分组
                bin_start,bin_end,bin_interval = numeric_attri_bin[evi_attri]


                if record_evi_value >= bin_start and record_evi_value <= bin_end:


                    bin_belong = bin_start + bin_interval * int((record_evi_value - bin_start)/bin_interval)

                    record_evi_value = bin_belong

                else:

                    continue


            else:

                unique_str_evi[evi_attri].append(record_evi_value)


            #如果这条记录的evidence的值还没有出现过
            if record_evi_value not in results[record_outcome][evi_attri]:

                results[record_outcome][evi_attri][record_evi_value] = 0 #初始化记数为0

            #记数增加1
            results[record_outcome][evi_attri][record_evi_value] += 1

            results[record_outcome][evi_attri]["Total"] += 1


    return results
######################################################################
# Specification: given a dictionary of dictionaries such as that
# produced by train() and a single input dictionary such as one of the
# records returned by getData(), return a dictionary consisting whose
# keys correspond to the values of the outcomes corresponding to the
# "outer dictionary" of S and their relative likelihood for the given
# input example.
#
def predict(S:dict, input:dict):

    outcomes = list(S.keys())

    outcomes.remove("Total")

    evidence = list(S[outcomes[0]].keys())

    outcome_count = [S[outcome]['Total'] for outcome in  outcomes]

    total_records = sum(outcome_count)

    #找到p(y)
    outcome_frequency =  dict([(outcomes[i], outcome_count[i] /total_records) for i in range(len(outcome_count))])

    #找到数值字段的分组信息
    numeric_attri_bin = {

    }
    for evi in evidence:

        if evi == "Total":

            continue

        evi_keys = list(S[outcomes[0]][evi].keys())


        if isinstance(evi_keys[0],str) == False:

            numeric_attri_bin[evi] = [min(evi_keys),max(evi_keys),evi_keys[1] - evi_keys[0]]

    for outcome in S:

        if outcome == "Total":

            continue

        for evi in evidence:

            if evi == "Total":

                continue

            evi_total = S[outcome][evi]['Total']

            for value in S[outcome][evi]:

                if value == "Total":

                    continue

                S[outcome][evi][value] = S[outcome][evi][value]/evi_total
                
    relative_likelihood = {}
    # 计算p(xi|y)p(y)
    for outcome in S:

        if outcome == "Total":

            continue
        # 找到p(y)
        relative_likelihood[outcome] = outcome_frequency[outcome]

        #找到p(x|y)
        for evi in evidence:

            if evi == "Total":

                continue


            evi_input_value = input[evi]


            if evi in numeric_attri_bin:

                bin_start, bin_end, bin_interval = numeric_attri_bin[evi]

                evi_input_value = bin_start + bin_interval * int((evi_input_value - bin_start) / bin_interval)

            if evi_input_value in S[outcome][evi]:

                relative_likelihood[outcome] *= S[outcome][evi][evi_input_value]

            else:
                relative_likelihood[outcome] = 0


    return relative_likelihood
D = getData()
results = train(D,outcome = "Gender" , evidence = ('Gender','Handed'))
print("train results:")
print(results)
#print(results.keys())
#print(results['Fly']['Total'])
#print(results['Fly']['Height_cm'])
#print(results['Fly']['Handed'])
#print(results['Fly']['Favourite_physical_activity'])
#print("sample")
sample = D[0]
#print(sample)
prob = predict(results,sample)
print("relative_likelihood")
print(prob)