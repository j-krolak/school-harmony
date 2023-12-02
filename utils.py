from pulp import *

NUM_OF_DUTY_HOURS = 1

class TeacherData:
    def __init__(self, name: str, hours: list[int]) -> None:
        self.hours = hours
        self.name = name

def get_shift_weight(shift: int):
    ten_minutes_shift = [0, 1, 3, 4]
    long_shift = [2]

    if shift % 8 in ten_minutes_shift:
        return 10
    if shift % 8 in long_shift:
        return 20
    return 5
    



def get_solution(teachers_data: list[TeacherData] , minimal_dis: float, maximal_dis: float) -> bool | list[list[int]]:
    TEACHERS = range(len(teachers_data))
    MAX_HOURS = 0 

    for teacher in teachers_data:
        for hour in teacher.hours:
            MAX_HOURS = max(MAX_HOURS, hour)
    MAX_HOURS += 1
    HOURS = range(MAX_HOURS)


    model = LpProblem("Optimisation")

    teachers_dict = LpVariable.dicts("Teachers", (TEACHERS,HOURS), cat=LpBinary)

    for teacher_id in TEACHERS: 
        # Set constraints for ratios of working hours to all hours
        model += lpSum([get_shift_weight(hour) * teachers_dict[teacher_id][hour] for hour in HOURS]) / sum(get_shift_weight(shift) for shift in teachers_data[teacher_id].hours) <= maximal_dis 
        model += lpSum([get_shift_weight(hour) * teachers_dict[teacher_id][hour] for hour in HOURS]) /sum(get_shift_weight(shift) for shift in teachers_data[teacher_id].hours) >= minimal_dis 

        for hour in HOURS:

            if not hour in teachers_data[teacher_id].hours:
                # Set constraints to exclude hours when the employer doesn't work
                model += teachers_dict[teacher_id][hour] == 0

    # Set constraints to ensure that exactly NUM_OF_DUTY_HOURS employer works each hour.
    for hour in HOURS:
        model += lpSum([ teachers_dict[teacher_id][hour] for teacher_id in TEACHERS]) == NUM_OF_DUTY_HOURS
    model += lpSum([teachers_dict[teacher_id][hour] for teacher_id in TEACHERS for hour in HOURS]) == MAX_HOURS * NUM_OF_DUTY_HOURS
    
    model.solve(PULP_CBC_CMD(msg=0))

    # Checking if the solution is correct
    for teacher_id in TEACHERS: 
        counter = 0
        for hour in HOURS:
            val = value(teachers_dict[teacher_id][hour])

            if not val in [0, 1]:
                return False
            if val == 1:
                counter += get_shift_weight(hour)
        
        if counter /sum(get_shift_weight(shift) for shift in teachers_data[teacher_id].hours) > maximal_dis:
            return False
        
        if  counter /sum(get_shift_weight(shift) for shift in teachers_data[teacher_id].hours) < minimal_dis:
            return False

    result = []
    for teacher_id in TEACHERS: 
        result.append([])
        for hour in HOURS:
            if value(teachers_dict[teacher_id][hour]):
                result[teacher_id].append(hour)

    return result

def display_solution(teachers_data: list[TeacherData] ,optimal_values: (float, float)):
    optimal_solution = get_solution(teachers_data, optimal_values[0], optimal_values[1])
    for teacher_id in range(len(teachers_data)):
        print(f"{teachers_data[teacher_id].name}: ")
        for hour in optimal_solution[teacher_id]:
            print(get_shift_weight(hour), end=" ")
        print()

# TODO: Find optimal values using binary search!
def find_optimal_solution(teachers_data: list[TeacherData]) -> (float, float): 
    step = 1/max([sum(get_shift_weight(shift) for shift in teacher.hours ) for teacher in teachers_data])
    maximal_dis = 1

    while maximal_dis >= 0:
        possible_solution = get_solution(teachers_data, 0, maximal_dis)
        if not possible_solution:
            maximal_dis += step
            possible_solution = get_solution(teachers_data, 0, maximal_dis)
            break
        if maximal_dis - step >= 0:
            maximal_dis -= step
        else:
            break
    

    minimal_dis = 0

    while minimal_dis <= 1:
        possible_solution = get_solution(teachers_data, minimal_dis, maximal_dis)
        
        if not possible_solution:
            minimal_dis -= step
            possible_solution = get_solution(teachers_data, minimal_dis, maximal_dis)
            break
        
        if minimal_dis + step  <= 1:
            minimal_dis += step
        else:
            break
    
    if maximal_dis > 1 or minimal_dis < 0:
        raise Exception("The correct solution doesn't exist!")
    return (minimal_dis,maximal_dis)

