''' This script opens a file called health_stats.json, reads the contents, and displays them as a graph'''
import json
import plotly.express as px
import pandas as pd

def read_file(filename):
    ''' This function opens a file and reads the contents as JSON
        Example file:
        {"Depression":"4","Fatigue":"4","Headache":"6","Mental Focus":"6","Overall Body":"4","Overall Mental":"6","Pain":"6","Stomach Pain":"4","Timestamp":"2022-05-28 16201858818510"}
        {"Depression":"9","Fatigue":"10","Headache":"2","Mental Focus":"2","Overall Body":"8","Overall Mental":"2","Pain":"0","Stomach Pain":"8","Timestamp":"2022-05-28 16203258832033"}
    '''
    health_stats = []
    with open(filename, 'r') as file:
        for(line) in file:
            health_stats.append(json.loads(line))
   
    return health_stats

def group_by_key(json_data):
    ''' For each key in the dictionary, create a list of values for that key
    Example data:
        [{"Depression":"4","Fatigue":"4","Headache":"6","Mental Focus":"6","Overall Body":"4","Overall Mental":"6","Pain":"6","Stomach Pain":"4","Timestamp":"2022-05-28 16201858818510"},
        {"Depression":"9","Fatigue":"10","Headache":"2","Mental Focus":"2","Overall Body":"8","Overall Mental":"2","Pain":"0","Stomach Pain":"8","Timestamp":"2022-05-28 16203258832033"}]
    '''
    # create a list of keys
    keys = list(json_data[0].keys())

    by_key = {}
    for key in keys:
        # if the key is not in the dictionary, add it
        if key not in by_key: by_key[key] = []

        for row in json_data:
            if key in row:
                by_key[key].append(row[key])
            else:
                by_key[key].append(0)

    return by_key


def display_graph(json_list, keys):
    ''' For each key in the dictionary, create a list of values for that key
        and display the graph
    Example data:
        [{"Depression":"4","Fatigue":"4","Headache":"6","Mental Focus":"6","Overall Body":"4","Overall Mental":"6","Pain":"6","Stomach Pain":"4","Timestamp":"2022-05-28 16201858818510"},
        {"Depression":"9","Fatigue":"10","Headache":"2","Mental Focus":"2","Overall Body":"8","Overall Mental":"2","Pain":"0","Stomach Pain":"8","Timestamp":"2022-05-28 16203258832033"}]
    '''

    df = pd.DataFrame(json_list)
    # convert the timestamp to a date time object
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H%M%S%f')
    df = pd.melt(df, id_vars=['Timestamp'])

    df['Timestamp'] = pd.DatetimeIndex(df['Timestamp']).normalize()
    df['value'] = df['value'].dropna().astype(int)
    df = df.groupby(['Timestamp', 'variable'], as_index=False).mean()

    titles = ['Mental Focus', 'Depression', 'Anger Irritation', 'Dwelling', 'Happiness', 'Motivation', 'Overall Mental', 'Fatigue', 'Pain', 'Stomach Pain', 'Headache', 'Overall Body']
    fig = px.bar(df, x='Timestamp', y='value', 
        color='variable', 
        facet_col='variable', facet_col_wrap=1, facet_row_spacing=0.02,
        category_orders={'variable': titles}
        )
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1])) # remove the variable name from each title
    
    fig.for_each_yaxis(lambda y: y.update(title = ''))
    fig.show()

def main():
    ''' This function opens a file and reads the contents'''
    filename = '/Users/jisaac/Documents/health_stats.json'
    health_data = read_file(filename)

    # create a list of keys
    keys = list(health_data[-1].keys())

    # display the contents as a graph
    display_graph(health_data, keys)

main()