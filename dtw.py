import sys
import time

# Calculates the DTW Distance between the two specified lists
def dtw_distance(s_list, t_list):
    dtw_matrix = [[0 for i in range(len(t_list))] for i in range(len(s_list))] 

    for i in range(1, len(s_list)):
        dtw_matrix[i][0] = float("inf")
    for i in range(1, len(t_list)):
        dtw_matrix[0][i] = float("inf")

    for i in range(1, len(s_list)):
        for j in range(1, len(t_list)):
            cost = (s_list[i] - t_list[j]) ** 2
            dtw_matrix[i][j] = cost + min(dtw_matrix[i-1][j], dtw_matrix[i][j-1], dtw_matrix[i-1][j-1])

    return dtw_matrix[len(s_list)-1][len(t_list)-1]

# Reads the data from the specified file and stores it in a list of lists
def read_data(f):
    data = []

    for line in f:
        data.append(line.split("\n")[0].split(" "))

    for i in range(len(data)):
        data[i] = list(map(float, data[i]))

    return data

def main(argv=sys.argv):
    if (len(argv) < 3):
        print('usage: %s train_file test_file' % argv[0])
        return False

    try:
        f = open(argv[1], 'r')  # Try to open the train file
    except OSError as e:
        print(e)
        return False
    else:
        # If successful, read the data and store it
        train_data = read_data(f)
        f.close()

    try:
        f = open(argv[2], 'r')  # Try to open the test file
    except OSError as e:
        print(e)
        return False
    else:
        # If successful, read the data and store it
        test_data = read_data(f)
        f.close()

    # Iterate over the test data, calculating the DTW Distance for every temporal sequence in the train data.
    # That's 240 ** 960! Takes a loong time...
    successes = 0
    start_time = time.time()
    for i in test_data:
        min_distance = float("inf")

        for j in train_data:
            dist = dtw_distance(i[1:], j[1:])

            if dist < min_distance:
                min_distance = dist
                test_class = j[0]

        if test_class == i[0]:
            successes = successes + 1
    elapsed_time = time.time() - start_time

    print("Performance: %d/%d = %.2f%%" % (successes, len(test_data), successes/len(test_data)*100))
    print("Time taken for the tests: %.2fs" % elapsed_time)

    return True

if __name__ == '__main__':
    main()