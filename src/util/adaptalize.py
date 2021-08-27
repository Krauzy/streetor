# Adapt Functions

def get_weekday(day=None, index=False):
    if day == 'Monday':
        if index:
            return 0
        return 'Segunda-Feira'
    elif day == 'Tuesday':
        if index:
            return 1
        return 'Terça-Feira'
    elif day == 'Wednesday':
        if index:
            return 2
        return 'Quarta-Feira'
    elif day == 'Thursday':
        if index:
            return 3
        return 'Quinta-Feira'
    elif day == 'Friday':
        if index:
            return 4
        return 'Sexta-Feira'
    elif day == 'Saturday':
        if index:
            return 5
        return 'Sábado'
    else:
        if index:
            return 6
        return 'Sunday'