import sys

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

    def read_from_excel(file_path, sheet_name, print_time_diff=None):
        data_list = read_excel_data(file_path, sheet_name)
        last_bezung = 0.0
        last_lieferung = 0.0
        max_bezug_pwr = 0.0
        max_lieferung_pwr = 0.0
        max_period = 0.0
        last_timestamp = 0

        for row in data_list:
            if last_bezung > 0.0:
                current_bezug = (row[1] - last_bezung)
                current_ieferung = (row[2] - last_lieferung)
                periode = (row[0] - last_timestamp).total_seconds()
                per_periode = (3600 / periode)
                max_bezug_pwr = max(max_bezug_pwr, current_bezug * per_periode)
                max_lieferung_pwr = max(max_lieferung_pwr, current_ieferung * per_periode)
                max_period = max(max_period, periode)
                ts = row[0]
                if print_time_diff is None or periode > 1000.0:
                    print(f"Zeit: {ts.day:02d}.{ts.month:02d}.{ts.year} {ts.hour:02d}:{ts.minute:02d}:{ts.second:02d} "
                          f"Bezug: {current_bezug :.3f} [kWh] Lieferung: {current_ieferung :.3f} [kWh]  ZeitDiff: {periode}")
                    # print(f"Zeit: {ts.day:02d}.{ts.month:02d}.{ts.year} {ts.hour:02d}:{ts.minute:02d}:{ts.second:02d} "
                    #       f"Zeitdifferenz: {periode:.0f} [s]")
            last_timestamp = row[0]
            last_bezung = row[1]
            last_lieferung = row[2]
        print(
            f"Max Bezug Pwr: {max_bezug_pwr :.3f} [kW] Max Lieferung Pwr: {max_lieferung_pwr :.3f} [kW] Max Period: {max_period}")


    file_path = sys.argv[1] if len(sys.argv) > 1 else "data/2-weg-messpunkt.xlsx"
    sheet_name = sys.argv[2] if len(sys.argv) > 2 else "tab1"
    print_time_diff = float(sys.argv[3]) if len(sys.argv) > 3 else None

    print(f"Data for {file_path}")
    read_from_excel(file_path, sheet_name, print_time_diff)
