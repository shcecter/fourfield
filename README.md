# Описание
Данный скрипт предназначен для формирования отчета по четырёхпольному взвешиванию, отчёт включает в себя
таблицу показателей и графическое представление результатов взвешивания.
# Необходимые пакеты
При использовании anaconda distribution можно создать виртуальную среду:
 **conda create -n fourfield
 activate fourfield**

Далее необходимо установить:

- pandas  --  conda install pandas, conda install xlrd
- matplotlib -- conda install matplotlib
- numpy  --  conda install numpy
- [click](https://pypi.org/project/click/)
- [fpdf](https://pypi.org/project/fpdf/)

Для запуска скрипта необходимо находится в корневой папке скрипта: \
 cd *path_to_foufield*\
 activate fourfield\
 python fourfieldreport.py\

# Использование
Для работы изначальные данные по четырём полям необходимо добавить в табличном виде в .xlsx файл,
файл выбирается произвольно, однако должен соответствовать шаблону (см. 'data/data_template.xlsx').
## Вариант 1.
Использование для формирования отчёта для отдельного пациента:\\
- Добавить даные пациента в .xlsx файл (например 'data/data_template.xlsx')
- запустить скрипт: python fourfield.py -f "path_to_xlsx" -n Фамилия Имя Отчество
    
