import datetime
import json
import os
import PyPDF2
import requests
import time
import webbrowser
from collection import defaultdict
from pathlib import Path

import google.generativeai as genai
import pandas as pd

# Defining paths
PARENT_DIR = Path(__file__).parent

# Defining current timestamp
def ct():
    return datetime.datetime.now()

