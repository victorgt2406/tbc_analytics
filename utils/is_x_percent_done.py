def is_x_percent_done(i:int, list_length:int, percent):
    """
    Determines whether it's time to inform or alert based on the current index, the total length of the list,
    and the specified inform interval.
    """
    increment = list_length * (percent / 100.0)
    current_progress = i + 1
    if current_progress >= increment and current_progress <= list_length:
        if current_progress % increment < 1 or (list_length - current_progress) < increment:
            return True
    return False