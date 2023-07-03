def time_normalization(time: str) -> str:
    time = time.split(':')
    for i in [0, 1]: time[i] = '0' + time[i] if len(time[i]) == 1 else time[i]
    time = ":".join(time)
    return time

