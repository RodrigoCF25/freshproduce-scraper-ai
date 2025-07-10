import csv
from typing import Iterator, Iterable, Collection, Dict, Any, Optional, Callable

class CSVHandler:
    @staticmethod
    def read(filepath : str, encoding: str = "utf-8") -> Iterator[Dict[str,Any]]:
        with open(filepath,"r",encoding=encoding,newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield row

    @staticmethod
    def read_as(filepath : str, constructor: Callable[[Dict[str, Any]], Any], encoding: str = "utf-8") -> Iterator[Any]:
        with open(filepath,"r",encoding=encoding,newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield constructor(row)

    @staticmethod
    def write(filepath:str, 
              data: Iterable[Dict[str,Any]], 
              field_names : Optional[Collection[str]] = None, 
              encoding: str = "utf-8"
    ) -> None:
        data = iter(data)
        first_row = next(data,None)
        if first_row is None:
            return
        
        if not field_names:
            field_names = list(first_row.keys())
        
        with open(filepath, encoding=encoding, newline='', mode="w") as file:
            writer = csv.DictWriter(file,fieldnames=field_names)
            writer.writeheader()
            writer.writerow(first_row)
            writer.writerows(data)