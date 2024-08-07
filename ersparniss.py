import sys
from datetime import datetime


def berechne_ersparniss(timeserie_bezug, timeserie_lieferung, tarif_bezug, tarif_lieferung, batterie_max_cap):
    ersparniss = 0.0
    batterie_cur_cap = 0.0  # Aktuelle Kapazität der Batterie

    for bezug, lieferung in zip(timeserie_bezug, timeserie_lieferung):
        # Überprüfe, ob die Batterie Energie aufnehmen kann
        if lieferung > 0.0:
            lc = batterie_cur_cap
            batterie_cur_cap += min(lieferung, batterie_max_cap - batterie_cur_cap)
            ersparniss -= (batterie_cur_cap - lc) * tarif_lieferung

        # Wenn die Batterie entlädt, nutze sie zum Eigenverbrauch
        if bezug > 0.0:
            lc = batterie_cur_cap
            batterie_cur_cap -= min(bezug, batterie_cur_cap)
            ersparniss += (lc - batterie_cur_cap) * tarif_bezug

    return ersparniss, batterie_cur_cap * tarif_bezug


def von_bis(begin, end):
    return (
        f"von: {begin.day:02d}.{begin.month:02d}.{begin.year} {begin.hour:02d}:{begin.minute:02d}:{begin.second:02d}"
        f" bis {end.day:02d}.{end.month:02d}.{end.year} {end.hour:02d}:{end.minute:02d}:{end.second:02d}")


if __name__ == '__main__':
    provider = sys.argv[1] if len(sys.argv) > 1 else "bkw"
    format_string = "%d.%m.%Y %H:%M:%S"
    begin_time = datetime.strptime(sys.argv[2], format_string) if len(sys.argv) > 2 else None
    end_time = datetime.strptime(sys.argv[3], format_string) if len(sys.argv) > 3 else None

    if provider == "bkw":
        from read_data_bkw import get_timserie as timeserie

        file_path = 'data/2-werte-messpunkte-wr.xlsx'
        sheet_name0 = 'Einspeisung Überschuss'  ## Lieferung
        sheet_name1 = 'Strombezug aus BKW-Netz'  ## Bezung
        sheet_name2 = 'Eigenbedarf PVA'  ## Verbrauch PV-Anlage
    elif provider == "neovac" :
        from read_data_neovac import get_timserie as timeserie

        file_path = 'data/2-weg-messpunkt.xlsx'
        sheet_name0 = 'tab1'  ## Bezung und Lieferung
        sheet_name1 = None
        sheet_name2 = None
    else:
        print(f"{provider} is not a valid provider")

    timesrie_lieferung, timeserie_bezug, timeserie_ts, timeserie_wr = timeserie(file_path, sheet_name0, sheet_name1,
                                                                                sheet_name2)

    tarif_bezung = 0.3027  # Tarif für Bezug in CHF/kWh 2024 (https://www.strompreis.elcom.admin.ch/?category=H3)
    tarif_lieferung = 0.0824  # Tarif für Lieferung in CHF/kWh, 2023 (4.Q) mit HKN
    batterie_max_cap = 1.0  # Maximale Kapazität der Batterie in kWh
    ersparnisse = 0.0

    idx_begin = 0 if begin_time is None else min((i for i, val in enumerate(timeserie_ts) if val >= begin_time))
    idx_end = -1 if end_time is None else max((i for i, val in enumerate(timeserie_ts) if val <= end_time))
    timesrie_lieferung = timesrie_lieferung[idx_begin:idx_end]
    timeserie_bezug = timeserie_bezug[idx_begin:idx_end]

    print(f"Data from: {provider} / {von_bis(timeserie_ts[idx_begin], timeserie_ts[idx_end])}")
    print(f"Total Bezug: {sum(timeserie_bezug):.2f} kWh / Total Lieferung: {sum(timesrie_lieferung):.2f} kWh")
    if timeserie_wr is not None:
        print(f"Total Bezug WR: {sum(timeserie_wr[idx_begin:idx_end]):.2f} kWh")

    # todo -- Consider charging and discharging losses
    while True:
        opt_ersparnisse, rest = berechne_ersparniss(timesrie_lieferung, timeserie_bezug, tarif_bezung, tarif_lieferung,
                                                    batterie_max_cap)
        total_ersparnis = opt_ersparnisse + rest
        if total_ersparnis > ersparnisse:
            ersparnisse = total_ersparnis
            print(
                f"Total Ersparnis: {total_ersparnis:.2f} / Rest {rest:.2f} CHF mit {batterie_max_cap:.0f} kWh Batterie"
                f"  (Ersparnis/kWh {total_ersparnis / batterie_max_cap:.2f})")
            batterie_max_cap += 1.0
        else:
            break
