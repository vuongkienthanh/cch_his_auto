def build_machedo(age_in_month: int) -> str:
    if age_in_month < 6:
        return "1BT sữa TT"
    elif age_in_month < 12:
        return "2BT sữa TT"
    elif age_in_month < 12 * 4:
        return "3BT cơm cháo TT"
    elif age_in_month < 12 * 7:
        return "4BT cơm TT"
    elif age_in_month < 12 * 10:
        return "5BT cơm TT"
    else:
        return "6BT cơm TT"
