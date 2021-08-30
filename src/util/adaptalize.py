# Adapt Functions

from pandas.core.frame import DataFrame


def get_weekday(day=None, index=False) -> str:
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

def get_weekday_revert(day=None, index=False) -> str:
    if day == 'Segunda-Feira':
        if index:
            return 0
        return 'Monday'
    elif day == 'Terça-Feira':
        if index:
            return 1
        return 'Tuesday'
    elif day == 'Quarta-Feira':
        if index:
            return 2
        return 'Wednesday'
    elif day == 'Quinta-Feira':
        if index:
            return 3
        return 'Thursday'
    elif day == 'Sexta-Feira':
        if index:
            return 4
        return 'Friday'
    elif day == 'Sábado':
        if index:
            return 5
        return 'Saturday'
    else:
        if index:
            return 6
        return 'Sunday'

def get_theme(theme) -> str:
    if theme == 'Escuro':
        return 'carto-darkmatter'
    elif theme == 'Claro':
        return 'carto-positron'
    else:
        return 'open-street-map'

def put_filter_data(data) -> DataFrame:
    data['Day of Week'] = data['Day of Week'].replace({
        'Sunday': 0, 
        'Monday': 1, 
        'Tuesday': 2, 
        'Wednesday': 3, 
        'Thursday': 4, 
        'Friday':5, 
        'Saturday':6
    })
    data['Period'] = data['Period'].replace({
        'Morning':0, 
        'Afternoon': 1, 
        'Night': 2, 
        'Dawn':3
    })
    data['Vehicle'] = data['Vehicle'].replace({
        'Others':0, 
        'Bike':1, 
        'Pedestrian': 2, 
        'Automobile': 3, 
        'Motorcycle':4, 
        'Truck':5, 
        'Bus':6
    })
    data['Victim'] = data['Victim'].replace({
        'Conductor': 0, 
        'Pedestrian': 1, 
        'Passenger':2
    })
    data['Type'] = data['Type'].replace({
        'Others': 0, 
        'Crash': 1, 
        'Run Over':2, 
        'Shock':3
    })
    data['Sex'] = data['Sex'].replace({
        'M':1, 
        'F':0
    })
    data = data.rename(columns={
        'Hour':'Temp'
    })
    data['Hour'] = data['Temp'].apply(lambda x: int(x.split(':')[0]))
    data['Minute'] = data['Temp'].apply(lambda x: int(x.split(':')[1]))
    data = data.drop(columns=['Temp'])
    return data

def get_filter_data(data) -> DataFrame:
    data['Day of Week'] = data['Day of Week'].replace({
        0:'Sunday', 
        1:'Monday', 
        2:'Tuesday', 
        3:'Wednesday', 
        4:'Thursday', 
        5:'Friday', 
        6:'Saturday'
    })
    data['Period'] = data['Period'].replace({
        0:'Morning', 
        1:'Afternoon', 
        2:'Night', 
        3:'Dawn'
    })
    data['Vehicle'] = data['Vehicle'].replace({
        0:'Others', 
        1:'Bike', 
        2:'Pedestrian', 
        3:'Automobile', 
        4:'Motorcycle', 
        5:'Truck', 
        6:'Bus'
    })
    data['Victim'] = data['Victim'].replace({
        0:'Conductor', 
        1:'Pedestrian', 
        2:'Passenger'
    })
    data['Type'] = data['Type'].replace({
        0:'Others', 
        1:'Crash', 
        2:'Run Over', 
        3:'Shock'
    })
    data['Sex'] = data['Sex'].replace({
        1:'M', 
        0:'F'
    })
    
    return data