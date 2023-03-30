import random
import sys
import csv 
import matplotlib.pyplot as plt

BINS = 100
def get_column_data(csv_path, column_name):
    #Open the CSV file for reading
    with open(csv_path, 'r') as f:
        #Create a CSV reader object
        reader = csv.reader(f)
        
        #Skip the header
        header = next(reader)
        data_index = header.index(column_name)

        #Create an empty list to store the data
        data = []

        #Loop through each row in the CSV file
        for row in reader:
            #Extract the value and append it to the data list
            row_data = row[data_index]
            if row_data != '':
                data.append(float(row[data_index]))
        return data
    
def equiwidth_histogram(data , column_name):
    min_value = min(data)
    max_value = max(data)
    print(f"minimum {column_name} = {min_value} maximum {column_name} = {max_value}")
    #split min_value and max_value into 100 even bins
    bin_size = (max_value - min_value) / BINS
    print("Bin size: ", bin_size)
    histogram = dict()
    for i in range(BINS):
        #Create a list of the data that falls into each bin
        bin_data = [x for x in data if x >= min_value + i * bin_size and x < min_value + (i+1) * bin_size]
        bin_min = round(min_value + i * bin_size, 2)
        bin_max = round(min_value + (i+1) * bin_size, 2)
        bin_range = f"[{bin_min:.2f}, {bin_max:.2f})"
        numtuples = len(bin_data)
        histogram[(bin_min, bin_max)] = numtuples
        print(f"bin:{i+1} range: {bin_range} numtuples: {numtuples}")
    return histogram

def equidepth_histogram_exp(data, column_name):
    # Sort the data
    sorted_data = sorted(data)
    data_len = len(data)
    print("data len:", data_len)
    bin_size = data_len // BINS # Use floor division for integer bin_size
    print("Bin size: ", bin_size)
    histogram = dict()
    # initialize variables for bin creation
    start = 0
    end = bin_size
    bins = []

    push_to_next_bin = []
    # create bins
    for i in range(BINS):
        if i == BINS - 1:  # last bin
            temp_list = sorted_data[start:]
            if len(push_to_next_bin) > 0:
                temp_list[:0] = push_to_next_bin
                push_to_next_bin = []
            bins.append(temp_list)
        else:
            temp_list = sorted_data[start:end]
            if len(push_to_next_bin) > 0:
                temp_list[:0] = push_to_next_bin
                push_to_next_bin = []
            start = end
            end += bin_size
            if temp_list[-1] == sorted_data[start]:
                j = -1
                while temp_list[j] == sorted_data[start]:
                    push_to_next_bin.append(temp_list.pop())
                    j = j-1
            bins.append(temp_list)
                    
    # print the range of the bins
    for i, bin in enumerate(bins):
        numtuples = len(bin)
        if i == BINS - 1:  # last bin
            print(f"bin:{i+1} range : [{bin[0]}, {bin[-1]}] numtuples: {numtuples}")
            histogram[(bin[0], bin[-1])] = numtuples
        else:
            print(f"bin:{i+1} range : [{bin[0]}, {bins[i+1][0]}) numtuples: {numtuples}")
            histogram[(bin[0], bins[i+1][0])] = numtuples
    
    return histogram

def equidepth_histogram(data, column_name):
    # Sort the data
    sorted_data = sorted(data)
    data_len = len(data)
    print("data len:", data_len)
    bin_size = data_len // BINS # Use floor division for integer bin_size
    print("Bin size: ", bin_size)
    histogram = dict()
    # initialize variables for bin creation
    start = 0
    end = bin_size
    bins = []

    push_to_next_bin = []
    # create bins
    for i in range(BINS):
        if i == BINS - 1:  # last bin
            bins.append(sorted_data[start:])
        else:
            bins.append(sorted_data[start:end])
            start = end
            end += bin_size
            
                    
    # print the range of the bins
    for i, bin in enumerate(bins):
        numtuples = len(bin)
        if i == BINS - 1:  # last bin
            print(f"bin:{i+1} range : [{bin[0]}, {bin[-1]}] numtuples: {numtuples}")
            histogram[(bin[0], bin[-1])] = numtuples
        else:
            print(f"bin:{i+1} range : [{bin[0]}, {bins[i+1][0]}) numtuples: {numtuples}")
            histogram[(bin[0], bins[i+1][0])] = numtuples
    
    return histogram

def calculate_overlap(bin_range, custom_range):
    bin_range_start, bin_range_end = bin_range
    custom_range_start, custom_range_end = custom_range
    percentage = None

    if bin_range_start >= custom_range_start and bin_range_end <= custom_range_end:
        percentage =  100
    elif bin_range_start < custom_range_start and bin_range_end > custom_range_end:
        percentage =  (custom_range_end - custom_range_start) / (bin_range_end - bin_range_start) * 100
    elif bin_range_start < custom_range_start and bin_range_end > custom_range_start:
        percentage =  (bin_range_end - custom_range_start) / (bin_range_end - bin_range_start) * 100
    elif bin_range_start < custom_range_end and bin_range_end > custom_range_end:
        percentage =  (custom_range_end - bin_range_start) / (bin_range_end - bin_range_start) * 100

    return percentage
    

def estimate_results(equiwidth_histogram_dict, equidepth_histogram_dict, a, b):
    custom_range = (a, b)
    overlap_equiwidth_tuples = [x for x in equiwidth_histogram_dict.keys() if (x[0] >= a and x[1] < b) or (x[0] <= a and x[1] > b) or (x[0] <= a and x[1] > a) or (x[0] < b and x[1] >= b)]
    overlap_equidepth_tuples = [x for x in equidepth_histogram_dict.keys() if (x[0] >= a and x[1] < b) or (x[0] <= a and x[1] > b) or (x[0] <= a and x[1] > a) or (x[0] < b and x[1] >= b)]
    # print("Overlap equidepth:", overlap_equidepth_tuples )
    estimated_equiwidth = 0
    for x in overlap_equiwidth_tuples:
        overlap_percentage = calculate_overlap(x,custom_range)
        estimated_equiwidth += equiwidth_histogram_dict[x] * overlap_percentage / 100
    print("Estimated equiwidth results:", estimated_equiwidth)
    estimated_equidepth = 0
    for x in overlap_equidepth_tuples:
        overlap_percentage = calculate_overlap(x, custom_range)
        estimated_equidepth += equidepth_histogram_dict[x] * overlap_percentage / 100
    print("Estimated equidepth results:", estimated_equidepth)

    return estimated_equiwidth, estimated_equidepth
    


def draw_bar_chart(histogram, column_name):
    # create a subplot
    #keys are tuples of (bin_min, bin_max) make them a string for plotting
    keys = [f"[{x[0]:.2f}, {x[1]:.2f})" for x in histogram.keys()]
    values = list(histogram.values())

    fig = plt.figure(figsize=(10, 5))

    # createt the bar plot with different colors to its bar 
    plt.bar(keys, values, color ='maroon', width = 0.4)

    plt.xlabel("Bins")
    plt.ylabel("Number of tuples")      
    plt.title(column_name)
    plt.show()

def testing(equiwidth_histogram_dict, equidepth_histogram_dict, num_of_tests):
    statistices = []
    for i in range(num_of_tests):
        a = random.uniform(min(data), max(data))
        b = random.uniform(a, max(data))
        print(f"For custom range:[{a},{b})")
        actual_result = [x for x in data if x >= a and x < b]
        estimated_equiwidth, estimated_equidepth = estimate_results(equiwidth_histogram_dict, equidepth_histogram_dict, a, b)
        print(f"Actual results: {len(actual_result)}")
        if abs(estimated_equiwidth - len(actual_result)) > abs(estimated_equidepth - len(actual_result)):
            statistices.append("depth")
            print("Equidepth is better")
        else:
            statistices.append("width")
            print("Equiwidth is better")
    print("Statistics:\n", "width: ", statistices.count("width"), "depth: ", statistices.count("depth"))
    if statistices.count("width") > statistices.count("depth"):
        print("Equiwidth is better")
    else:
        print("Equidepth is better")





if __name__ == "__main__":
    args = sys.argv
    #Check if there are 2 arguments (csv path and column name)
    csv_path = "acs2015_census_tract_data.csv"
    column_name = "Income"
    if len(args) == 3:
        csv_path = args[1]
        column_name = args[2]
    print("CSV path: ", csv_path)
    print("Column name: ", column_name)
    data = get_column_data(csv_path, column_name)
    #check how many time number 136250 is in the data
    print("\n136250:",data.count(136250))
    print("125156:",data.count(125156))
    equiwidth_histogram_dict = equiwidth_histogram(data, column_name)
    equidepth_histogram_dict = equidepth_histogram(data, column_name)
    # draw_bar_chart(equiwidth_histogram_dict, column_name)
    # draw_bar_chart(equidepth_histogram_dict, column_name)
    while(1):
        answer = input("Try custom range? (Y/n)? ")
        if answer == 'y' or answer == 'Y' or not answer.strip():
            a = float(input("Enter lower bound: "))
            b = float(input("Enter upper bound: "))

            print(f"For custom range:[{a},{b})")
            actual_result = [x for x in data if x >= a and x < b]
            estimate_results(equiwidth_histogram_dict, equidepth_histogram_dict, a, b)
            print(f"Actual results: {len(actual_result)}")

        elif answer == 'n' or answer == 'N':
            break
    
    testing(equiwidth_histogram_dict, equidepth_histogram_dict, 100)
    
