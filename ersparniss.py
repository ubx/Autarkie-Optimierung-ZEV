from read_data import get_timserie


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

    return ersparniss


file_path = 'data/2-weg-messpunkt.xlsx'  ## Bezung und Lieferung
sheet_name = 'tab1'
timesrie_lieferung, timeserie_bezug, timeserie_ts = get_timserie(file_path, sheet_name)

tarif_bezung = 0.2905    # Tarif für Bezug in CHF/kWh 2024
tarif_lieferung = 0.0824 # Tarif für Lieferung in CHF/kWh, 2023 mit HKN
batterie_max_cap = 1.0   # Maximale Kapazität der Batterie in kWh
ersparnisse = 0.0

# Ersparnisse berechnen
# todo -- Consider charging and discharging losses
while True:
    opt_ersparnisse = berechne_ersparniss(timesrie_lieferung, timeserie_bezug, tarif_bezung, tarif_lieferung,
                                          batterie_max_cap)
    if opt_ersparnisse > ersparnisse:
    ###if batterie_max_cap < 1500:
        ersparnisse = opt_ersparnisse
        print(f"Ersparnis: {opt_ersparnisse :.2f} CHF mit {batterie_max_cap:.0f} kWh Batterie")
        batterie_max_cap += 1.0
    else:
        break
