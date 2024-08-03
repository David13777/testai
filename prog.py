import json
from collections import Counter
import csv

# Шаг 1: Чтение данных из файла
with open('food_services.json', 'r', encoding='utf-8-sig') as file:
    data = json.load(file)

# Шаг 2: Анализ данных

# Определение района с наибольшим количеством заведений
district_counter = Counter()
for obj in data:
    district_counter[obj['District']] += 1

most_common_district = district_counter.most_common(1)[0]
print(f"{most_common_district[0]}: {most_common_district[1]}")

# Определение сети с наибольшим количеством заведений
network_counter = Counter()
for obj in data:
    if obj['IsNetObject'].lower() == 'да':
        network_counter[obj['OperatingCompany']] += 1

most_common_network = network_counter.most_common(1)[0]
print(f"{most_common_network[0]}: {most_common_network[1]}")

# Определение самого большого заведения для каждого вида
type_objects = {}
for obj in data:
    type_object = obj['TypeObject']
    if type_object not in type_objects:
        type_objects[type_object] = obj
    elif obj['SeatsCount'] > type_objects[type_object]['SeatsCount']:
        type_objects[type_object] = obj

sorted_type_objects = dict(sorted(type_objects.items()))

for type_object, obj in sorted_type_objects.items():
    print(f"{type_object}: {obj['Name']}, {obj['SeatsCount']}")

# Шаг 3: Сохранение данных
with open('largest_food_services_by_type.csv', 'w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['вид', 'название заведения', 'количество посадочных мест']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')

    writer.writeheader()
    for type_object, obj in sorted_type_objects.items():
        writer.writerow({
            'вид': type_object,
            'название заведения': obj['Name'],
            'количество посадочных мест': obj['SeatsCount']
        })