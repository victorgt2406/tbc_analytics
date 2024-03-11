def is_x_percent_done(i:int, list_length:int, percent) -> bool:
    """
    Determines whether it's time to inform or alert based on the current index, the total length of the list,
    and the specified inform interval.
    """
    # increment = list_length * (percent / 100.0)
    # current_progress = i + 1
    # if current_progress >= increment and current_progress <= list_length:
    #     if current_progress % increment < 1 or (list_length - current_progress) < increment:
    #         return True
    # return False
    step = list_length * (percent / 100.0)
    trigger_points = [round(step * n) for n in range(1, int(100/percent)+1)]
    current_index = i + 1
    return current_index in trigger_points or current_index == list_length