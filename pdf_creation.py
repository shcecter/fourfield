from fpdf import FPDF


PDF_MASK = [
            [('ОГ%', 'Левая'), ('ОГ%', 'Правая'), None, ('ЗГ%', 'Левая'), ('ЗГ%', 'Правая')],
            [('ОГ К', 'Кл'), ('ОГ К', 'Кп'), ('К%', 'КаОГ'), ('ЗГ К', 'Кл'), ('ЗГ К', 'Кп')],
            [('ОГ', 'Левый Носок'), ('ОГ', 'Правый Носок'),
             ('К%', 'КаЗГ'),
             ('ЗГ', 'Левый Носок'), ('ЗГ', 'Правый Носок')],
            [('ОГ КН:П', 'Левая'), ('ОГ КН:П', 'Правая'), None, ('ЗГ КН:П', 'Левая'), ('ЗГ КН:П', 'Правая')],
            [('ОГ', 'Левая Пятка'), ('ОГ', 'Правая Пятка'), None, ('ЗГ', 'Левая Пятка'), ('ЗГ', 'Правая Пятка')],
           ]


def create_pdf(pat_name, pdf_tbl, img_path):
    '''
    Принимает на вход имя пациента и таблицу, создаёт pdf, который заполняет из таблицы
    и добавляет изображение из папки 'tmp/' (для этого конкретного пациента)
    '''
    pat_idx = pdf_tbl[pdf_tbl[('Unnamed: 0_level_0', 'ФИО')] == pat_name].index

    pdf_mask = PDF_MASK

    perc = '{0:.2f} %'
    K = 'K = {0:.2f}'
    P_toe = 'P = {0:.2f}'
    coef = 'KH:П= {0:.2f}'
    P_heel = 'P = {0:.2f}'

    coef_asym_open = '<= Ka= {0:.2f} %'
    coef_asym_clos = 'Ka= {0:.2f} % =>'

    appearance_mask = [
                       [perc, perc, None, perc, perc],
                       [K, K, coef_asym_open, K, K],
                       [P_toe, P_toe, coef_asym_clos, P_toe, P_toe],
                       [coef, coef, None, coef, coef],
                       [P_heel, P_heel, None, P_heel, P_heel],
                      ]

    a4_w = 210 - 20
    cell_w = a4_w / 5
    cell_h = 12  # experimental

    title_w = a4_w
    title_h = 10

    title_patt = 'Ф.И.О.: {}'

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.add_font('ArialUni', '', 'supply/ARIALUNI.TTF', uni=True)
    pdf.set_font('ArialUni', '', 11)

    pdf.cell(title_w, title_h, title_patt.format(pat_name), 1, 1, 'L')

    # header
    pdf.cell(2*cell_w, cell_h, '(ОГ)', 1, 0, 'C')
    pdf.cell(cell_w, cell_h, '', 1, 0)
    pdf.cell(2*cell_w, cell_h, '(ЗГ)', 1, 1, 'C')

    row_counter = 0
    for app_row, data_row in zip(appearance_mask, pdf_mask):
        for app, data in zip(app_row, data_row):
            row_counter += 1
            newline = 1 if row_counter == 5 else 0
            if data:
                patient_cell_data = pdf_tbl.loc[pat_idx, data].values[-1]
                pdf.cell(cell_w, cell_h, app.format(patient_cell_data), 1, newline, 'C')
            else:
                pdf.cell(cell_w, cell_h, '', 1, newline, 'C')

        row_counter = 0

    total_weight = pdf_tbl.loc[pat_idx, ('Общий вес', 'Общий')].values[-1]
    pdf.cell(cell_w, cell_h, f"Общий вес: {total_weight:.2f}")
    pdf.ln()
    pat_img_path = img_path + pat_name + '.png'
    pdf.image(pat_img_path, x=0, w=210, h=205/2.1)

    pdf.output(f'output/{pat_name}.pdf', 'F')
