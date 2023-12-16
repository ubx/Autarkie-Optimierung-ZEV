import pandas as pd

def read_excel_data(file_path, sheet_name):
    try:
        # Read Excel file
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df.values.tolist()
    except Exception as e:
        print(f"An error occurred: {e}")

def get_timserie(file_path, sheet_name):
    timserie_bezug = []
    timserie_lieferung = []
    timserie_ts = []
    data_list = read_excel_data(file_path, sheet_name)
    last_bezung = 0.0
    last_lieferung = 0.0
    for row in data_list:
        if last_bezung > 0.0:
            current_bezug = (row[1] - last_bezung)
            current_ieferung = (row[2] - last_lieferung)
            timserie_bezug.append(current_bezug)
            timserie_lieferung.append(current_ieferung)
            timserie_ts.append(row[0])
        last_bezung = row[1]
        last_lieferung = row[2]
    return timserie_lieferung, timserie_bezug, timserie_ts


if __name__ == '__main__':
    file_path = 'data/2-weg-messpunkt.xlsx'
    sheet_name = 'tab1'
    data_list = read_excel_data(file_path, sheet_name)

    last_bezung = 0.0
    last_lieferung = 0.0
    max_bezug_pwr = 0.0
    max_lieferung_pwr = 0.0
    last_timestamp = 0
    for row in data_list:
        if last_bezung > 0.0:
            current_bezug = (row[1] - last_bezung)
            current_ieferung = (row[2] - last_lieferung)
            periode = (row[0] - last_timestamp).total_seconds()
            per_periode = (3600 / periode)
            max_bezug_pwr = max(max_bezug_pwr, current_bezug * per_periode)
            max_lieferung_pwr = max(max_lieferung_pwr, current_ieferung * per_periode)
            print(
                f"Zeit {row[0]} Bezug: {current_bezug :.3f} [kWh] Lieferung: {current_ieferung :.3f} [kWh]  ZeitDiff: {periode}")
        last_timestamp = row[0]
        last_bezung = row[1]
        last_lieferung = row[2]

    print(f"Max Bezug Pwr: {max_bezug_pwr :.3f} [kW] Max Lieferung Pwr: {max_lieferung_pwr :.3f} [kW]")