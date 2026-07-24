from faker import Faker
import sys
from datetime import date
import random
from main_config import MainConfig
import argparse
import pathlib
from bisect import bisect_left


headers = [
    'ssn',
    'cc_num',
    'first',
    'last',
    'gender',
    'street',
    'city',
    'state', 
    'zip', 
    'lat', 
    'long', 
    'city_pop',
    'job', 
    'dob', 
    'acct_num', 
    'profile',
    'income_band',
    'education',
    'marital_status'
]


def make_cities():
    cities_low = {}   # < 50k
    cities_mid = {}   # 50k - 500k
    cities_high = {}  # > 500k

    with open('./demographic_data/locations_partitions.csv', 'r') as f:
        lines = f.readlines()[1:]
        tot = len(lines)
        for i, line in enumerate(lines):
            output = line.strip().split(',')[1].split('|')
            pop = float(output[-1])
            cdf = (i + 1) / float(tot)
            if pop < 50000:
                cities_low[cdf] = output
            elif pop <= 500000:
                cities_mid[cdf] = output
            else:
                cities_high[cdf] = output

    # In case any bucket is empty, fallback to all
    all_cities = {}
    for i, line in enumerate(lines):
        output = line.strip().split(',')[1].split('|')
        cdf = (i + 1) / float(tot)
        all_cities[cdf] = output

    return {
        'low': cities_low if cities_low else all_cities,
        'mid': cities_mid if cities_mid else all_cities,
        'high': cities_high if cities_high else all_cities
    }


def make_age_gender_dict():
    gender_age = {}
    prev = 0
    with open('./demographic_data/age_gender_demographics.csv', 'r') as f:
        for line in f.readlines()[1:]:
            l = line.strip().split(',')
            prev += float(l[3])
            gender_age[prev] = (l[2], float(l[1]))
        return gender_age


class Customer:
    'Randomly generates all the attributes for a customer'

    def __init__(self, config, seed_num=None):
        self.fake = Faker('en_US')
        self.fake_es = Faker('es_MX')
        if seed_num is not None:
            Faker.seed(seed_num)
            random.seed(seed_num)
        # turn all profiles into dicts to work with
        self.all_profiles = MainConfig(config).config

    def generate_race(self):
        # white (60%), hispanic (18%), black_asian (22%)
        r = random.random()
        if r < 0.60:
            return 'white'
        elif r < 0.78:
            return 'hispanic'
        else:
            return 'black_asian'

    def get_first_and_last_name(self, race):
        if race == 'hispanic':
            hispanic_first_male = ['Carlos', 'Jose', 'Juan', 'Luis', 'Miguel', 'Mateo', 'Alejandro', 'Santiago', 'Diego', 'Gabriel', 'Fernando', 'Francisco', 'Ricardo', 'Jorge', 'Javier', 'Rafael', 'Hector', 'Antonio', 'Manuel']
            hispanic_first_female = ['Maria', 'Sofia', 'Isabella', 'Camila', 'Valentina', 'Valeria', 'Mariana', 'Gabriela', 'Lucia', 'Ximena', 'Carmen', 'Ana', 'Rosa', 'Teresa', 'Juana', 'Elena', 'Adriana']
            hispanic_last = ['Rodriguez', 'Garcia', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Perez', 'Sanchez', 'Ramirez', 'Torres', 'Flores', 'Rivera', 'Gomez', 'Diaz', 'Reyes', 'Morales', 'Ortiz', 'Gutierrez']
            first = random.choice(hispanic_first_male) if self.gender == 'M' else random.choice(hispanic_first_female)
            last = random.choice(hispanic_last)
        elif race == 'black_asian':
            if random.random() < 0.5:
                # Asian names
                asian_first_male = ['David', 'Kevin', 'Alex', 'Jason', 'Michael', 'Brian', 'Andrew', 'Eric', 'Daniel', 'Justin']
                asian_first_female = ['Grace', 'Emily', 'Michelle', 'Jessica', 'Amanda', 'Hannah', 'Sarah', 'Rachel', 'Jennifer', 'Ashley']
                asian_last = ['Chen', 'Kim', 'Nguyen', 'Patel', 'Singh', 'Wang', 'Li', 'Yang', 'Zhang', 'Tran', 'Shah', 'Park', 'Lin', 'Wu']
                first = random.choice(asian_first_male) if self.gender == 'M' else random.choice(asian_first_female)
                last = random.choice(asian_last)
            else:
                # Black / African American names
                black_first_male = ['Jamal', 'Malik', 'Darnell', 'Treyvon', 'DeAndre', 'Tyrone', 'Terrell', 'Marquan', 'Kevon', 'Rashad', 'Xavier', 'Marcus']
                black_first_female = ['Aaliyah', 'Shanice', 'Ebony', 'Imani', 'Tamika', 'Keisha', 'Latoya', 'Nia', 'Tiana', 'Kiara', 'Jada', 'Jasmine']
                black_last = ['Washington', 'Jefferson', 'Jackson', 'Williams', 'Johnson', 'Banks', 'Booker', 'Rivers', 'Dorsey', 'Mosley']
                first = random.choice(black_first_male) if self.gender == 'M' else random.choice(black_first_female)
                last = random.choice(black_last)
        else:
            # White / standard US
            first = self.fake.first_name_male() if self.gender == 'M' else self.fake.first_name_female()
            last = self.fake.last_name()

        return first, last

    def generate_customer(self):
        self.gender, self.dob, self.age = self.generate_age_gender()
        self.race = self.generate_race()
        self.addy = self.get_random_location()
        first_name, last_name = self.get_first_and_last_name(self.race)
        customer_data = [
            self.fake.ssn(),
            self.generate_cc_num(),
            first_name,
            last_name,
            self.gender,
            self.fake.street_address()
        ] + self.addy + [
            self.generate_job(),
            self.dob,
            str(self.fake.random_number(digits=12)),
            self.find_profile(),
            self.generate_income_band(),
            self.generate_education(),
            self.generate_marital_status()
        ]
        return customer_data

    def generate_cc_num(self):
        # visa_mc (86%), amex (8%), discover (6%)
        r = random.random()
        if r < 0.86:
            if random.random() < 0.5:
                return '4' + ''.join([str(random.randint(0, 9)) for _ in range(15)])
            else:
                prefix = str(random.randint(51, 55))
                return prefix + ''.join([str(random.randint(0, 9)) for _ in range(14)])
        elif r < 0.94:
            prefix = random.choice(['34', '37'])
            return prefix + ''.join([str(random.randint(0, 9)) for _ in range(13)])
        else:
            return '6011' + ''.join([str(random.randint(0, 9)) for _ in range(12)])

    def get_first_name(self):
        if self.gender == 'M':
            return self.fake.first_name_male()
        else:
            return self.fake.first_name_female()

    def generate_age_gender(self):
        # Gender: M (49%), F (51%)
        gender = 'M' if random.random() < 0.49 else 'F'

        # DOB / Age distribution: 18-34 (29%), 35-59 (40%), 60+ (31%)
        r = random.random()
        if r < 0.29:
            age = random.randint(18, 34)
        elif r < 0.69:
            age = random.randint(35, 59)
        else:
            age = random.randint(60, 85)

        today = date.today()
        birth_year = today.year - age
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        dob = date(birth_year, month, day)

        return gender, dob.strftime("%Y-%m-%d"), age

    def generate_job(self):
        # professional_finance (13%), healthcare_ed_gov (19%), service_trade (27%), retired (21%), unemployed (20%)
        r = random.random()
        if r < 0.13:
            return random.choice(['Financial Analyst', 'Accountant', 'Software Engineer', 'Lawyer', 'Auditor', 'Investment Banker'])
        elif r < 0.32:
            return random.choice(['Registered Nurse', 'Teacher', 'Physician', 'Civil Servant', 'Professor', 'Pharmacist'])
        elif r < 0.59:
            return random.choice(['Retail Manager', 'Electrician', 'Chef', 'Mechanic', 'Plumber', 'Sales Associate', 'Driver'])
        elif r < 0.80:
            return 'Retired'
        else:
            return 'Unemployed'

    def generate_income_band(self):
        # <50k (30.6%), 50-100k (28.2%), 100k+ (41.2%)
        r = random.random()
        if r < 0.306:
            return '<50k'
        elif r < 0.588:
            return '50-100k'
        else:
            return '100k+'

    def generate_education(self):
        # hs_or_less (36.4%), some_college (24.9%), bachelor_plus (38.7%)
        r = random.random()
        if r < 0.364:
            return 'hs_or_less'
        elif r < 0.613:
            return 'some_college'
        else:
            return 'bachelor_plus'

    def generate_marital_status(self):
        # married (50.0%), never_married (33.0%), formerly_married (17.0%)
        r = random.random()
        if r < 0.50:
            return 'married'
        elif r < 0.83:
            return 'never_married'
        else:
            return 'formerly_married'

    # find location based on city_pop distribution: <50k (20%), 50-500k (50%), >500k (30%)
    def get_random_location(self):
        r = random.random()
        if r < 0.20:
            bucket = cities['low']
        elif r < 0.70:
            bucket = cities['mid']
        else:
            bucket = cities['high']

        num = random.random()
        lst = sorted(bucket.keys())
        pos = bisect_left(lst, num)
        if pos == 0:
            return bucket[lst[0]]
        if pos == len(lst):
            return bucket[lst[-1]]
        before = lst[pos - 1]
        after = lst[pos]
        if after - num < num - before:
            return bucket[after]
        else:
            return bucket[before]

    def find_profile(self):
        city_pop = float(self.addy[-1])

        match = []
        for pro in self.all_profiles:
            # -1 represents infinity
            if (self.gender in self.all_profiles[pro]['gender']
                and self.age >= self.all_profiles[pro]['age'][0]
                and (self.age < self.all_profiles[pro]['age'][1] 
                    or self.all_profiles[pro]['age'][1] == -1) 
                and city_pop >= self.all_profiles[pro]['city_pop'][0] 
                and (city_pop < self.all_profiles[pro]['city_pop'][1] 
                    or self.all_profiles[pro]['city_pop'][1] == -1)
                ):
                match.append(pro)
        if match == []:
            match.append('leftovers.json')

        # found overlap -- write to log file but continue
        if len(match) > 1:
            with open('profile_overlap_warnings.log', 'a') as f:
                f.write(f"{' '.join(match)}: {self.gender} {str(self.age)} {str(city_pop)}\n")
        return match[0]


def main(num_cust, seed_num, config, out_path):
    if num_cust <= 0 or seed_num is None or config is None:
        parser.print_help()
        exit(1)

    # setup output to file by redirecting stdout
    original_sys_stdout = sys.stdout
    if out_path is not None:
        f_out = open(str(out_path), 'w')
        sys.stdout = f_out

    # print headers
    print("|".join(headers))

    c = Customer(config=config, seed_num=seed_num)
    for _ in range(num_cust):
        customer_data = c.generate_customer()
        print("|".join(customer_data))


    # restore original sdtout when done
    if out_path is not None:
        sys.stdout = original_sys_stdout


cities = make_cities()
age_gender = make_age_gender_dict()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Customer Generator')
    parser.add_argument('count', type=int, help='Number of customers to generate', default=10)
    parser.add_argument('seed', type=int, nargs='?', help='Random generator seed', default=42)
    parser.add_argument('config', type=pathlib.Path, nargs='?', help='Profile config file (typically profiles/main_config.json")', default='./profiles/main_config.json')
    parser.add_argument('-o', '--output', type=pathlib.Path, help='Output file path', default=None)

    args = parser.parse_args()
    num_cust = args.count
    seed_num = args.seed
    config = args.config
    out_path = args.output

    main(num_cust, seed_num, config, out_path)


