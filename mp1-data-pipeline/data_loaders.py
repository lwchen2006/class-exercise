from pathlib import Path
 
import logging
import pandas as pd
import json
import yaml
 
 
# Use the logging configuration from Part 1.
logger = logging.getLogger(__name__)
 
 
def load_csv(filepath):
    """Load a CSV file into a DataFrame.
    filepath is a Path object.
    """
    df = pd.read_csv(filepath)
    logger.info("Loaded CSV file: %s (%d rows)", filepath, len(df))
    return df

def load_json(filepath):

def load_yaml(filepath):


def load_data(filepath):