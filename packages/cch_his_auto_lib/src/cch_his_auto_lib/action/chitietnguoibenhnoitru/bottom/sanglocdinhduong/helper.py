def machedo(age_in_month: int) -> str:
    if age_in_month < 6:
        return "1BT sữa TT 700kcal"
    elif age_in_month < 12:
        return "2BT sữa TT 1000kcal"
    elif age_in_month < 12 * 4:
        return "3BT cơm cháo TT 1300kcal"
    elif age_in_month < 12 * 7:
        return "4BT cơm TT 1700kcal"
    elif age_in_month < 12 * 10:
        return "5BT cơm TT 2000kcal"
    else:
        return "6BT cơm TT 2500kcal"
