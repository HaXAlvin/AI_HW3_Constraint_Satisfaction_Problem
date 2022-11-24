import json
import argparse
from collections import defaultdict
from copy import deepcopy



def course_schedule_solver() -> list:
    global COURSE_ORDER
    order = COURSE_ORDER
    print(order)
    # BEGIN_YOUR_CODE
    output = []
    in_node_record = defaultdict(list) # {node: [in_node]}
    for i in range(numCourses):
        in_node_record[i] = []
    for i in prerequisites:
        in_node_record[i[0]].append(i[1])

    rerun = False
    while(rerun or any([i==[] for i in in_node_record.values()])):
        rerun = False
        for leave,in_node in in_node_record.items():
            in_node_record[leave] = [i for i in in_node if i not in output] # remove the node that has been output
            if len(in_node) == 0: # find the leave node
                output.append(leave)
                del in_node_record[leave]
                rerun = True
                break
    if len(in_node_record) == 0:
        return output
    # END_YOUR_CODE
    return []


if __name__ == '__main__':
    COURSE_ORDER = []

    parser = argparse.ArgumentParser()
    parser.add_argument('--course_file_path', '-f', type=str, default='q2_sample_input.json')

    args = parser.parse_args()
    with open(args.course_file_path, "r+") as fs:
        course_schedule_info = json.load(fs)
        numCourses = course_schedule_info['numCourses']
        prerequisites = course_schedule_info['prerequisites']

    COURSE_ORDER = [-1 for x in range(numCourses)]
    course_order = course_schedule_solver()

    print("COURSE ORDER:")
    print(course_order)

    result_dict = {
        "result": course_order
    }

    with open('course_schedule_result.json', 'w+') as fs:
        fs.write(json.dumps(result_dict, indent=4))
