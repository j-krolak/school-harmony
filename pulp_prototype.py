from pulp import *

class Teacher_Data:
    def __init__(self, name: str, hours: list[int]) -> None:
        self.hours = hours
        self.name = name



def get_solution(teachers_data: list[Teacher_Data] , minimal_dis: float, maximal_dis: float) -> bool | list[list[int]]:
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
        for hour in HOURS:
            # Set constraints for ratios of working hours to all hours
            model += lpSum([teachers_dict[teacher_id][hour] for hour in HOURS]) / len(teachers_data[teacher_id].hours) <= maximal_dis 
            model += lpSum([teachers_dict[teacher_id][hour] for hour in HOURS]) / len(teachers_data[teacher_id].hours) >= minimal_dis 

            if not hour in teachers_data[teacher_id].hours:
                # Set constraints to exclude hours when the employer doesn't work
                model += teachers_dict[teacher_id][hour] == 0

    # Set constraints to ensure that exactly one employer works each hour.
    for hour in HOURS:
        model += lpSum([ teachers_dict[teacher_id][hour] for teacher_id in TEACHERS]) == 1
    model += lpSum([teachers_dict[teacher_id][hour] for teacher_id in TEACHERS for hour in HOURS]) == MAX_HOURS
    
    model.solve(PULP_CBC_CMD(msg=0))

    # Checking if the solution is correct
    for teacher_id in TEACHERS: 
        counter = 0
        for hour in HOURS:
            val = value(teachers_dict[teacher_id][hour])

            if not val in [0, 1]:
                return False
            if val == 1:
                counter += 1
        
        if counter/ len(teachers_data[teacher_id].hours) > maximal_dis:
            return False
        
        if counter/ len(teachers_data[teacher_id].hours) < minimal_dis:
            return False

    result = []
    for teacher_id in TEACHERS: 
        result.append([])
        for hour in HOURS:
            if value(teachers_dict[teacher_id][hour]):
                result[teacher_id].append(hour)

    return result

def display_solution(teachers_data: list[Teacher_Data] ,optimal_values: (float, float)):
    optimal_solution = get_solution(teachers_data, optimal_values[0], optimal_values[1])
    for teacher_id in range(len(teachers_data)):
        print(f"{teachers_data[teacher_id].name}: ")
        for hour in optimal_solution[teacher_id]:
            print(hour, end=" ")
        print()

def find_optimal_solution(teachers_data: list[Teacher_Data]) -> (float, float): 
    step = 1/(max([len(teacher.hours) for teacher in teachers_data])+2)
    maximal_dis = 1

    while maximal_dis >= 0:
        possible_solution = get_solution(teachers_data, 0, maximal_dis)
        if not possible_solution:
            maximal_dis += step
            possible_solution = get_solution(teachers_data, 0, maximal_dis)
            break
        
        maximal_dis -= step
    

    minimal_dis = 0

    while minimal_dis <= 1:
        possible_solution = get_solution(teachers_data, minimal_dis, maximal_dis)
        
        if not possible_solution:
            minimal_dis -= step
            possible_solution = get_solution(teachers_data, minimal_dis, maximal_dis)
            break
        
        minimal_dis += step
    
    if maximal_dis > 1 or minimal_dis < 0:
        raise Exception("The correct solution doesn't exist!")
    return (minimal_dis,maximal_dis)

teachers_data = [
    Teacher_Data("Mr. X",[0, 1, 2, 3 , 4, 6, 8]),
    Teacher_Data("Mrs. Y", [2, 3, 5, 7])
]


optimal_values = find_optimal_solution(teachers_data)
display_solution(teachers_data, optimal_values)