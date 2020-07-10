import pandas as pd
import matplotlib.pyplot as plt

import click

from plotting import plot_patient
from pdf_creation import create_pdf


# constants
output_path = 'output/'
tmp_path = 'tmp/'
name_label = ('Unnamed: 0_level_0', 'ФИО')


# importing data from excel file
def read_data(table_name):
    patients_df = pd.read_excel('data/'+table_name, sheet_name='4-х полка', header=[0, 1])
    return patients_df


def plot_one_patient(table, name=None, idx=None):
    '''Принимает на вход имя (как с excel) или индекс пациента, для которого нужен график'''
    patients = table
    if name:
        idx = patients[patients[name_label] == name].index[0]
    else:
        name = patients.loc[idx, ('Unnamed: 0_level_0', 'ФИО')]
    first_patient = patients.loc[idx, :]
    plot_patient(first_patient)
    plt.savefig(tmp_path+name+'.png', dpi=200)


def process_excel(table_name):
    table = read_data(table_name)
    pat_names = table.loc[:, name_label]

    for name in pat_names:
        plot_one_patient(name=name, table=table)
        create_pdf(pat_name=name, pdf_tbl=table, img_path=tmp_path)


@click.command()
@click.option('-f', '--filename', prompt='Введите имя файла (file_name.xlsx)', default='data_template.xlsx')
@click.option('-n', '--patient_name', default=None, nargs=3, type=str)
def start_app(filename, patient_name):
    if patient_name:
        data = read_data(filename)
        patient_name = ' '.join(patient_name)
        plot_one_patient(data, name=patient_name)
        create_pdf(patient_name, data, tmp_path)
    else:
        process_excel(filename)


if __name__ == '__main__':
    start_app()
