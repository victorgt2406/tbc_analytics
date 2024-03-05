from datetime import datetime

def compare_str_dates(str_date1:str, str_date2:str) -> bool | None:
    """
    Returns true if date1 is greater than date 2, false otherwise
    
    Dates need to be formated as ISO 8601 format.
    Ex: 2024-03-04T12:43:29Z
    """
    try:
        date1 = datetime.fromisoformat(str_date1)
        date2 = datetime.fromisoformat(str_date2)
        return date1 > date2
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"""WARNING Compare str dates: dates are not ISO 8601 formated
              \nDate1: {str_date1}, Date2 {str_date2}
              \n{e}""")
        return None
