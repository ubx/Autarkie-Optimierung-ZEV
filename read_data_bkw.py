from datetime import datetime

import pandas as pd


def read_excel_data(file_path, sheet_name):
    try:
        # Read Excel file
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df.values.tolist()
    except Exception as e:
        print(f"An error occurred: {e}")


def get_timserie(file_path, sheet_name_lieferung, sheet_name_bezug, sheet_name_bezug_wr):
    timserie_bezug = []
    timserie_lieferung = []
    timserie_ts = []
    timserie_wr = []
    data_list_lieferung = read_excel_data(file_path, sheet_name_lieferung)
    data_list_bezug = read_excel_data(file_path, sheet_name_bezug)
    data_list_bezug_wr = read_excel_data(file_path, sheet_name_bezug_wr)
    for row_liferung, row_bezug, row_bezug_wr in zip(data_list_lieferung, data_list_bezug, data_list_bezug_wr):
        timserie_bezug.append(row_bezug[2])
        timserie_lieferung.append(row_liferung[2])
        timserie_ts.append(datetime.combine(row_bezug[0], row_bezug[1]))
        timserie_wr.append(row_bezug_wr[2])

    return timserie_lieferung, timserie_bezug, timserie_ts, timserie_wr
