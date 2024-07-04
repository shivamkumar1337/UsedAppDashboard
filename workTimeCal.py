def time_to_minutes(time_str):
    """Convert HH:MM time string to minutes since midnight."""
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def minutes_to_time(minutes):
    """Convert minutes since midnight to HH:MM time string."""
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02d}:{minutes:02d}"

def convert_intervals_to_minutes(intervals):
    """Convert list of time intervals to list of intervals in minutes."""
    return [[time_to_minutes(start), time_to_minutes(end)] for start, end in intervals]

def convert_intervals_to_time(intervals):
    """Convert list of intervals in minutes to list of time intervals."""
    return [[minutes_to_time(start), minutes_to_time(end)] for start, end in intervals]

def remove_intersections(workTimeList, restTimeList):
    result = []
    i, j = 0, 0
    n, m = len(workTimeList), len(restTimeList)
    
    while i < n:
        start1, end1 = workTimeList[i]
        while j < m and restTimeList[j][1] < start1:
            j += 1
        
        if j == m or restTimeList[j][0] > end1:
            result.append([start1, end1])
            i += 1
        else:
            start2, end2 = restTimeList[j]
            
            if start2 <= end1 and end2 >= start1:
                if start1 < start2:
                    result.append([start1, start2])
                if end1 > end2:
                    workTimeList[i] = [end2, end1]
                    j += 1
                else:
                    i += 1
            else:
                result.append([start1, end1])
                i += 1

    return result

def calculate_total_work_time(intervals):
    total_minutes = 0
    for start, end in intervals:
        total_minutes += (end - start)
    return total_minutes


# workTimeList =  [ ["8:00", "10:00"], ["12:00", "13:00"], ["14:35", "17:00"], ["18:00","20:00"] ]
# restTimeList = [ ["9:00", "9:10"], ["10:00", "10:30"], ["15:00", "15:10"], ["15:30","15:40"] ]
workTimeList =  [ ["8:00", "11:00"], ["13:00", "15:00"], ["16:00", "20:00"]]
# workTimeList =  [ ["17:00", "23:00"]]
# workTimeList =  [ ["13:00", "23:00"]]
restTimeList = [ ["10:30", "10:45"], ["13:15", "13:30"], ["14:30", "14:40"], ["16:00","16:10"], ["17:20","17:30"] ]

workTimeList_minutes = convert_intervals_to_minutes(workTimeList)
restTimeList_minutes = convert_intervals_to_minutes(restTimeList)


result_minutes = remove_intersections(workTimeList_minutes, restTimeList_minutes)


result_times = convert_intervals_to_time(result_minutes)


total_work_minutes = calculate_total_work_time(result_minutes)
total_work_time = f"{total_work_minutes // 60} hours and {total_work_minutes % 60} minutes"

print(f"Work Intervals : {workTimeList}")
print(f"Rest Intervals : {restTimeList}")
print(f"Result : {result_times}")
print(f"Total work time : {total_work_time}")
