import pandas as pd
from IPython.display import display
data =  \
    {
        "name" : ["nikhil", "dicks"],
        "age" : [26, 27]
    }
data_pandas = pd.DataFrame(data)
display(data_pandas[data_pandas.age == 26])