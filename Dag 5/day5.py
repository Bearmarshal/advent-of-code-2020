import io
import sys

def first(file_name):
    with io.open(file_name, mode = 'r') as infile:
        seat_ids = [int(line.replace('B', '1').replace('F', '0').replace('R', '1').replace('L', '0'), 2) for line in infile]
    print("First star: {}".format(max(seat_ids)))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        seat_ids = [int(line.replace('B', '1').replace('F', '0').replace('R', '1').replace('L', '0'), 2) for line in infile]
    seat_ids.sort()
    for i in range(len(seat_ids) - 2):
        if seat_ids[i + 1] == seat_ids[i] + 2:
            my_seat_id = seat_ids[i] + 1
    print("Second star: {}".format(my_seat_id))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])