import re
import pandas as pd
import os
import usaddress


class Parser(object):
    def __init__(self, file=None):
        self.file = file
        self.codes = pd.read_csv(os.path.dirname(__file__)+"/../csv/police_codes.csv")
        self.street_crimes = []
        self.crime_count = None

    def parse_lines(self):
        street = None
        line_count = 0
        count_df = self.codes.copy()
        count_df['count'] = 0
        with open(self.file, "r") as f:
            for line in f:
                line = line.split(":", maxsplit=1)
                line[1] = line[1].split("\n")[0]

                street_check = self.find_address(line[1])
                if street_check or line_count > 3:
                    street = street_check
                    line_count = 0

                crime = self.codes['code'].apply(lambda x: self.contains_code(str(x), str(line[1])))
                if street:
                    self.format_address_crime_tuple(street, crime)
                crime = crime.astype(int)
                count_df['count'] = count_df['count'].add(crime)
                line_count += 1
        self.crime_count = count_df

    def format_address_crime_tuple(self, address, crime):
        formatted_address = address['AddressNumber'] + " " + address['StreetName'] + " " + address['StreetNamePostType']
        crime_df = self.codes.copy()
        crime_df = crime_df[crime]
        crime_meaning = crime_df['meaning']
        for meaning in crime_meaning:
            self.street_crimes.append((formatted_address, meaning))

    def get_crime_count(self):
        return self.crime_count

    def get_street_crimes(self):
        return self.street_crimes

    @staticmethod
    def find_address(string):
        address = usaddress.parse(string)
        address_dict = {i: j for j, i in address}
        if 'AddressNumber' in address_dict and 'StreetName' in address_dict and 'StreetNamePostType' in address_dict:
            return address_dict
        return None

    @staticmethod
    def contains_code(code, line):
        return f' {code} ' in f' {line} ' or f' {code.replace("-", " ")} ' in f' {line} '







