import dspy
from dspy.datasets import HotPotQA
import pandas as pd

def prepare_data():
    # file path for CSV
    file_path = './datasets/dataset.csv'
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Randomise order of data
    df = df.sample(frac=1)
    # Combine data from three columns into one
    df['summary'] = df.apply(lambda row: f'Received comment "{row["comment"]}", on {row["datetime"]}, via {row["metadata.channel"]}'
, axis=1)
    # Convert dataframe to list
    docs = df['summary'].head(200).tolist() # Only selecting 200 records due to hardware constraints on my system
    # Find aggregate data for metadata channels
    channel_counts = df['metadata.channel'].value_counts()
    #Create statements from aggregate data
    statements = [f"Total number of complaints via {channel} were: {count}" for channel, count in channel_counts.items()]
    # Combine data
    docs += statements+[f'Total number of complainsts via all channels were: {len(df)}']
    # Generate unique id for each record
    ids = list(range(0,len(docs)))
    return docs, ids
