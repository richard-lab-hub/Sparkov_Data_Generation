import csv
from datetime import datetime
from collections import Counter

import os

# Load Customer Data
customers_file = "output_data/customers.csv" if os.path.exists("output_data/customers.csv") else "./Sparkov_Data_Generation/output_data/customers.csv"
transactions_file = "output_data/transactions.csv" if os.path.exists("output_data/transactions.csv") else "./Sparkov_Data_Generation/output_data/transactions.csv"

# Demographic dictionaries used in generator
HISPANIC_SURNAMES = {'Rodriguez', 'Garcia', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Perez', 'Sanchez', 'Ramirez', 'Torres', 'Flores', 'Rivera', 'Gomez', 'Diaz', 'Reyes', 'Morales', 'Ortiz', 'Gutierrez'}
ASIAN_SURNAMES = {'Chen', 'Kim', 'Nguyen', 'Patel', 'Singh', 'Wang', 'Li', 'Yang', 'Zhang', 'Tran', 'Shah', 'Park', 'Lin', 'Wu'}
BLACK_FIRSTNAMES = {'Jamal', 'Malik', 'Darnell', 'Treyvon', 'DeAndre', 'Tyrone', 'Terrell', 'Marquan', 'Kevon', 'Rashad', 'Xavier', 'Marcus', 'Aaliyah', 'Shanice', 'Ebony', 'Imani', 'Tamika', 'Keisha', 'Latoya', 'Nia', 'Tiana', 'Kiara', 'Jada', 'Jasmine'}

def classify_race(first, last):
    if last in HISPANIC_SURNAMES:
        return 'Hispanic'
    elif last in ASIAN_SURNAMES:
        return 'Asian'
    elif first in BLACK_FIRSTNAMES:
        return 'Black'
    else:
        return 'White'

print("=" * 60)
print("       SYNTHETIC DATASET ATTRIBUTE DISTRIBUTION REPORT")
print("=" * 60)

# Analyze Customers
with open(customers_file, 'r') as f:
    customers = list(csv.DictReader(f, delimiter='|'))

cust_count = len(customers)
print(f"\n--- CUSTOMER ATTRIBUTES (Total Customers: {cust_count}) ---")

# Gender
genders = Counter(c['gender'] for c in customers)
print("\n[1] Gender Distribution:")
for k, v in genders.items():
    print(f"  - {k}: {v} ({v/cust_count*100:.1f}%)")

# Race / Name Ethnicity
races = Counter(classify_race(c['first'], c['last']) for c in customers)
print("\n[2] Name Ethnicity / Race Distribution:")
for k, v in races.items():
    print(f"  - {k}: {v} ({v/cust_count*100:.1f}%)")

# Income Band
incomes = Counter(c['income_band'] for c in customers)
print("\n[3] Income Band Distribution:")
for k, v in incomes.items():
    print(f"  - {k}: {v} ({v/cust_count*100:.1f}%)")

# Education
educations = Counter(c['education'] for c in customers)
print("\n[4] Education Distribution:")
for k, v in educations.items():
    print(f"  - {k}: {v} ({v/cust_count*100:.1f}%)")

# Marital Status
maritals = Counter(c['marital_status'] for c in customers)
print("\n[5] Marital Status Distribution:")
for k, v in maritals.items():
    print(f"  - {k}: {v} ({v/cust_count*100:.1f}%)")

# Age Groups
current_year = datetime.now().year
age_groups = Counter()
for c in customers:
    birth_year = int(c['dob'].split('-')[0])
    age = current_year - birth_year
    if age < 35:
        age_groups['18-34'] += 1
    elif age <= 59:
        age_groups['35-59'] += 1
    else:
        age_groups['60+'] += 1

print("\n[6] Age Group Distribution:")
for k in ['18-34', '35-59', '60+']:
    v = age_groups[k]
    print(f"  - {k}: {v} ({v/cust_count*100:.1f}%)")

# City Population
pops = Counter()
for c in customers:
    pop = float(c['city_pop'])
    if pop < 50000:
        pops['<50k (Rural)'] += 1
    elif pop <= 500000:
        pops['50k-500k (Suburban)'] += 1
    else:
        pops['>500k (Urban)'] += 1

print("\n[7] City Population Distribution:")
for k, v in pops.items():
    print(f"  - {k}: {v} ({v/cust_count*100:.1f}%)")


# Analyze Transactions
print("\n" + "=" * 60)
with open(transactions_file, 'r') as f:
    tx_reader = csv.DictReader(f, delimiter='|')
    
    tx_count = 0
    frauds = 0
    merchant_sizes = Counter()
    velocities = Counter()
    amounts = Counter()

    for t in tx_reader:
        tx_count += 1
        if t['is_fraud'] == '1':
            frauds += 1
        
        merchant_sizes[t['merchant_size']] += 1
        
        vel = int(t['transaction_velocity'])
        if vel <= 1:
            velocities['0-1'] += 1
        elif vel <= 4:
            velocities['2-4'] += 1
        else:
            velocities['5+'] += 1

        amt = float(t['amt'])
        if amt < 10:
            amounts['<$10'] += 1
        elif amt <= 100:
            amounts['$10-100'] += 1
        else:
            amounts['>$100'] += 1

print(f"--- TRANSACTION ATTRIBUTES (Total Transactions: {tx_count:,}) ---")

print(f"\n[1] Fraud Rate:")
print(f"  - Fraud: {frauds} ({frauds/tx_count*100:.4f}%)")
print(f"  - Legit: {tx_count - frauds} ({(tx_count - frauds)/tx_count*100:.4f}%)")

print("\n[2] Merchant Size Distribution:")
for k, v in merchant_sizes.items():
    print(f"  - {k}: {v:,} ({v/tx_count*100:.1f}%)")

print("\n[3] Transaction Velocity Distribution:")
for k in ['0-1', '2-4', '5+']:
    v = velocities[k]
    print(f"  - {k}: {v:,} ({v/tx_count*100:.1f}%)")

print("\n[4] Transaction Amount Buckets:")
for k in ['<$10', '$10-100', '>$100']:
    v = amounts[k]
    print(f"  - {k}: {v:,} ({v/tx_count*100:.1f}%)")

print("=" * 60)