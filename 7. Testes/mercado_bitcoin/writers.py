import datetime
from email import message
import json 
import os


class DataTypeNotSupportedForIngestionException:
    def __init__(self, data) -> None:
        self.data = data
        self.message = f'Data type {data} is not supported for ingestion!'
        super().__init__(message)


class DataWriter:
    def __init__(self, api: str, coin: str) -> None:
        self.coin = coin
        self.api = api
        self.filename = f'{self.api}/{self.coin}/{datetime.datetime.now()}.json'

    
    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, 'a') as f:
            f.write(row)
    
    def write(self, data: [list, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + '\n') #dict -> json
        elif isinstance(data,list):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)
