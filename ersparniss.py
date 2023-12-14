from read_data import get_timserie


def berechne_ersparniss(timeserie_bezug, timeserie_lieferung, tarif_eigenverbrauchh, tarif_lieferung, batterie_max_cap):
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
            ersparniss += (lc - batterie_cur_cap) * tarif_eigenverbrauchh

    return ersparniss


file_path = 'data/2-weg-messpunkt.xlsx'  ## Bezung und Lieferung
sheet_name = 'tab1'
timserie_lieferung, timeserie_bezug, _ = get_timserie(file_path, sheet_name)

tarif_bezung = 0.221  # Tarif für Bezug in CHF/kWh
tarif_eigenverbrauchh = tarif_bezung * 0.8  # Tarif für Strom aus Batterie im ZEV in CHF/kWh
tarif_lieferung = 0.08  # Tarif für Lieferung in CHF/kWh
batterie_max_cap = 1.0  # Maximale Kapazität der Batterie in kWh
ersparnisse = 0.0

# Ersparnisse berechnen
# todo -- Consider charging and discharging losses
while True:
    opt_ersparnisse = berechne_ersparniss(timserie_lieferung, timeserie_bezug, tarif_eigenverbrauchh, tarif_lieferung,
                                          batterie_max_cap)
    if opt_ersparnisse > ersparnisse:
        ersparnisse = opt_ersparnisse
        print(f"Ersparnis: {opt_ersparnisse :.2f} CHF mit {batterie_max_cap:.0f} kWh Batterie")
        batterie_max_cap += 1.0
    else:
        break
