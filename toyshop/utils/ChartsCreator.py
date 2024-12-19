import random
import json
import matplotlib.pyplot as plt
import os

from faker import Faker

from django.conf import settings


class ChartsCreator:

    def __init__(self):
        self.__fixture_path = os.path.join(settings.BASE_DIR, 'utils', 'fixtures.json')
        self.__main_static_path = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'charts')

        self.__generate_fixtures__()
        self.__generate_charts__()


    def __generate_fixtures__(self):
        fake = Faker()
        cities = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
            'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'
        ]
        fixtures = []

        for _ in range(50):
            fixture = {
                'name': fake.name(),
                'age': random.randint(0, 100),
                'salary': random.randint(20000, 100000),
                'position': fake.job(),
                'city': random.choice(cities),
            }
            fixtures.append(fixture)

        with open(self.__fixture_path, 'w') as f:
            json.dump(fixtures, f, indent=4)

    def __generate_charts__(self):
        with open(self.__fixture_path, 'r') as f:
            data = json.load(f)

        ages = [item['age'] for item in data]
        salaries = [item['salary'] for item in data]
        cities = [item['city'] for item in data]

        plt.figure(figsize=(10, 6))
        plt.hist(ages, bins=10, color='skyblue', edgecolor='black')
        plt.title('Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        plt.text(0.5, 0.5, 'Королев Артeм', fontsize=20, color='gray', alpha=0.5, ha='center', va='center',
                 transform=plt.gca().transAxes)
        plt.savefig(os.path.join(self.__main_static_path, 'histogram.png'))

        plt.figure(figsize=(10, 6))
        plt.plot(range(len(salaries)), sorted(salaries), marker='o', color='green')
        plt.title('Salaries Trend')
        plt.xlabel('Index')
        plt.ylabel('Salary')
        plt.text(0.5, 0.5, 'Королев Артeм', fontsize=20, color='gray', alpha=0.5, ha='center', va='center',
                 transform=plt.gca().transAxes)
        plt.savefig(os.path.join(self.__main_static_path, 'line_chart.png'))

        city_counts = {city: cities.count(city) for city in set(cities)}
        plt.figure(figsize=(8, 8))
        plt.pie(city_counts.values(), labels=city_counts.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('City Distribution')
        plt.text(0.5, 0.5, 'Королев Артeм', fontsize=20, color='gray', alpha=0.5, ha='center', va='center',
                 transform=plt.gca().transAxes)
        plt.savefig(os.path.join(self.__main_static_path, 'pie_chart.png'))
