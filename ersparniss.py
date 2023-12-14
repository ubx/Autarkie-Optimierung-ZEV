from read_data import get_timserie


def berechne_ersparniss(timeserie_bezug, timeserie_lieferung, tarif_eigenverbrauchh, tarif_lieferung, batterie_max_cap):
    ersparniss = 0.0
    batterie_min_cap = 0.0  # Minimale Kapazität der Batterie in kWh
    batterie_current_cap = batterie_max_cap  # Aktuelle Kapazität der Batterie

    for bezug, lieferung in zip(timeserie_bezug, timeserie_lieferung):
        # Überprüfe, ob die Batterie Energie aufnehmen kann
        if lieferung > 0 and batterie_current_cap < batterie_max_cap:  ## todo -- this may overload the battery!!
            batterie_current_cap += lieferung
            ersparniss -= lieferung * tarif_lieferung

        # Wenn die Batterie entlädt, nutze sie zum Netzbezug
        if bezug > 0 and batterie_current_cap > batterie_min_cap:
            batterie_current_cap -= bezug
            ersparniss += bezug * (tarif_eigenverbrauchh)  ## todo -- without battery charge losses!!

    return ersparniss


file_path = 'data/2-weg-messpunkt.xlsx'  ## Bezung und Lieferung
sheet_name = 'tab1'
timserie_lieferung, timeserie_betzg = get_timserie(file_path, sheet_name)

tarif_bezung = 0.221  # Tarif für Bezug in CHF/kWh
tarif_eigenverbrauchh = tarif_bezung * 0.8  # Tarif für Strom aus Batterie im ZEV in CHF/kWh
tarif_lieferung = 0.08  # Tarif für Lieferung in CHF/kWh
batterie_max_cap = 5.0  # Maximale Kapazität der Batterie in kWh

# Ersparnisse berechnen
ersparnisse = berechne_ersparniss(timserie_lieferung, timeserie_betzg, tarif_eigenverbrauchh, tarif_lieferung,
                                  batterie_max_cap)
print(f"Ersparnis: {ersparnisse :.2f} CHF mit {batterie_max_cap:.0f} kWh Batterie")

# Evaluate the optimale battery capacity
while True:
    batterie_max_cap += 1.0
    opt_ersparnisse = berechne_ersparniss(timserie_lieferung, timeserie_betzg, tarif_eigenverbrauchh, tarif_lieferung,
                                          batterie_max_cap)
    if opt_ersparnisse > ersparnisse:
        ersparnisse = opt_ersparnisse
        print(f"Ersparnis: {opt_ersparnisse :.2f} CHF mit {batterie_max_cap:.0f} kWh Batterie")
    else:
        print(f"Maximale Ersparnis: {opt_ersparnisse :.2f} CHF mit {batterie_max_cap:.0f} kWh Batterie")
        break
