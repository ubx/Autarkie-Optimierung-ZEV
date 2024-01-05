from datetime import datetime

import pandas as pd


def read_excel_data(file_path, sheet_name):
    try:
        # Read Excel file
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df.values.tolist()
    except Exception as e:
        print(f"An error occurred: {e}")


def get_timserie(file_path, sheet_name_lieferung, sheet_name_bezug):
    timserie_bezug = []
    timserie_lieferung = []
    timserie_ts = []
    data_list_lieferung = read_excel_data(file_path, sheet_name_lieferung)
    data_list_bezug = read_excel_data(file_path, sheet_name_bezug)
    for row_liferung, row_bezug in zip(data_list_lieferung, data_list_bezug):
        timserie_bezug.append(row_bezug[2])
        timserie_lieferung.append(row_liferung[2])
        timserie_ts.append(datetime.combine(row_bezug[0], row_bezug[1]))
    return timserie_lieferung, timserie_bezug, timserie_ts


if __name__ == '__main__':
    timserie_lieferung, timserie_bezug, timserie_ts = (
        get_timserie("data/Werte Eggenstrasse  3 Walperswil.xlsx", "Einspeisung Überschuss",
                     "Strombezug aus BKW-Netz"))
    pass
