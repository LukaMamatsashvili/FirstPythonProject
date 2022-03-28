from pymongo import MongoClient
import pandas as pd, matplotlib.pyplot as pl, threading


class Dataset:
    def __init__(self):  self.df = pd.read_excel('info.xlsx')  # dataframe that reads information from file

    def transfer(self):                                        # insert data into db
        client = MongoClient()                                 # creating db and collection
        db = client['DataSet']
        collection = db['DataSet']
        self.df.reset_index(inplace=True)                      # 1st row(title bar) is removed
        df_dct = self.df.to_dict('records')                    # dataframe is converted into dictionary
        collection.insert_many(df_dct)                         # data is inserted into db

    def output(self):                                          # diagram output using threading
        df1 = self.df[self.df['money'] > 1000]                 # data will be inserted from df into df1 according to a specific criteria
        grp1 = df1['month'].groupby(df1['month'])              # then it will be grouped by specific field
        grp1 = grp1.count()
        diagram = pd.DataFrame(grp1)                          # creating diagram
        diagram.plot(kind='bar')
        diagram.plot(kind='line')
        pl.show()
        file = open('info.txt', 'a')                           # creating new file with append mode
        def info():
            try: file.write(self.df.to_string())               # insert data into file as string
            except TypeError: print('\a\nERROR!')              # error exception
        t1 = threading.Thread(target=info)                     # threading
        t1.start()
        t1.join()


try:
    d = Dataset()
    d.transfer()
    d.output()
except TypeError: print('\a\nERROR!')