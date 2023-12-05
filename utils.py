from pulp import *

#TODO: Create UI for customizing this values
NUM_OF_SHIFTS = 7
NAMES_OF_SHIFTS = ["Wejście A", "Wejście C", "Szatnia", "Piętro 1 - Hol", "Piętro 1 - Stara część", "Piętro 2 - Hol", "Piętro 2 - stara część", "Patio"]
DELTA = 1/400
DAYS = ["Pn", "Wt", "Śr", "Czw", "Pi"]
HOURS  = ["8:45-8:55", "9:40-9:50", "10:35-10:55", "11:40-11:50", "12:35-12:45", "13:30-13:35", "14:20-14:25", "15:10-15:15"]

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
    
def shift_index_to_str(index: int) -> str:
    day = shift_index_to_day(index)
    hour = shift_index_to_hour(index)
    return f"{day} {hour}"

def shift_index_to_hour(index: int) -> str:
    return HOURS[index % 8]

def shift_index_to_day(index: int) -> str:
    return DAYS[index // 8]

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

    # Set constraints to ensure that exactly NUM_OF_SHIFTS employer works each hour.
    for hour in HOURS:
        model += lpSum([ teachers_dict[teacher_id][hour] for teacher_id in TEACHERS]) == NUM_OF_SHIFTS
    model += lpSum([teachers_dict[teacher_id][hour] for teacher_id in TEACHERS for hour in HOURS]) == MAX_HOURS * NUM_OF_SHIFTS
    
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
        all = 0
        for hour in teachers_data[teacher_id].hours:
            all += get_shift_weight(hour)
        x = 0
        for hour in optimal_solution[teacher_id]:
            x += get_shift_weight(hour)

        print(f"Optimal ratio: {round(x/all, 4)}")


def solution_to_dict(teachers_data: list[TeacherData], optimal_values: (float, float)) -> dict[str, list[int]]:
    optimal_solution = get_solution(teachers_data, optimal_values[0], optimal_values[1])
    result = {}
    for teacher_id in range(len(teachers_data)):
        result[teachers_data[teacher_id].name] = []
        for hour in teachers_data[teacher_id].hours:
            if hour in optimal_solution[teacher_id]:
                result[teachers_data[teacher_id].name].append(hour)
    return result


def find_optimal_minimal(teachers_data: list[TeacherData], high=1) -> float:
    low = 0
    mid = (low+high)/2

    while( high - low > DELTA):
        possible_solution = get_solution(teachers_data, mid, 1)
        if not possible_solution:
            high = mid - DELTA
            mid = (low+high)/2
        else:
            low = mid
            mid = (low+high)/2

    return low

def find_optimal_maximal(teachers_data: list[TeacherData], low=0) -> float:
    high = 1
    mid = (low+high)/2

    while( high - low > DELTA):
        possible_solution = get_solution(teachers_data, mid, 1)
        if not possible_solution:
            low = mid + DELTA
            mid = (low+high)/2
        else:
            high = mid
            mid = (low+high)/2

    return high



def find_optimal_solution(teachers_data: list[TeacherData]) -> (float, float): 
    minimal_dis = find_optimal_minimal(teachers_data)
    maximal_dis = find_optimal_maximal(teachers_data, minimal_dis)

    if maximal_dis > 1 or minimal_dis < 0 or not get_solution(teachers_data,minimal_dis, maximal_dis):
        return (1, 1)
    return (minimal_dis,maximal_dis)

