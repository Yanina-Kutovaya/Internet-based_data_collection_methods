# Создать приложение, которое будет из готового файла с данными «Сбербанка» выводить результат по параметрам:
# - тип данных
# - интервал дат
# - oбласть
# Визуализировать выводимые данные с помощью графика

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('opendata.csv', encoding="windows-1251")

i = 12   # Число от 0 до 14, соответствующее типу данных
j = 78  # Число от 0 до 83, соответствующее названию региона
t1 = '2018-02-04'  # >= '2013-01-15' наало периода
t2 = '2019-01-16'  # <= '2019-01-15' конец периода

dtype_cond = df['name'] == df.name.unique()[i]
region_cond = df['region'] == df.region.unique()[j]
time_cond = (df['date'] > t1) & (df['date'] < t2)

result = df[dtype_cond & region_cond & time_cond]
print(result)

plt.plot(result.date, result.value)
plt.ylabel('value')
plt.xlabel('time')
plt.title(f'{result.name.unique()[0]}. {result.region.unique()[0]}')
plt.show()