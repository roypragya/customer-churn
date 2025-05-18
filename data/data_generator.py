from faker import Faker
import pandas as pd
import random
from datetime import datetime

fake = Faker()
Faker.seed(42)

NUM_RECORDS = 100000
segments = ['silver', 'gold', 'platinum']
regions = ['North', 'South', 'East', 'West']
today = datetime.today().date()

data = []
for i in range(NUM_RECORDS):
    last_purchase = fake.date_between(start_date='-1y', end_date='today')
    total_spent = round(random.uniform(100, 2000), 2)
    visits = random.randint(1, 50)
    avg_spent_per_visit = round(total_spent / visits, 2)
    days_since_last_purchase = (today - last_purchase).days
    recent_buyer = int(days_since_last_purchase <= 30)
    segment = random.choices(segments, weights=[0.6, 0.3, 0.1])[0]
    region = random.choice(regions)

    churn_risk = (days_since_last_purchase > 90) + (avg_spent_per_visit < 40) + (visits < 5)
    churned = 1 if churn_risk >= 2 else 0

    data.append({
        'customer_id': i,
        'last_purchase': last_purchase,
        'total_spent': total_spent,
        'visits': visits,
        'avg_spent_per_visit': avg_spent_per_visit,
        'recent_buyer': recent_buyer,
        'segment': segment,
        'region': region,
        'churned': churned
    })

df = pd.DataFrame(data)
df.to_csv('data/sample_data.csv', index=False)
print("Synthetic dataset with segments and regions created.")