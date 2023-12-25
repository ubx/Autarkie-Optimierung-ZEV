import argparse
import matplotlib.pyplot as plt
import pandas as pd
import pathlib as pt

parser = argparse.ArgumentParser(
                    prog='Enery Plotter',
                    description='Plot the time evolution of power consumption measurements ')
parser.add_argument('in_file', type=str, nargs=1,
                    help='path to input xslx file')
parser.add_argument('tab', nargs='?', default='tab1',
                    help='tab name of within the excel file')

args = parser.parse_args()
in_path = args.in_file[0]
in_tab = args.tab

print(in_path, in_tab)

try:
    # Read Excel file
    df = pd.read_excel(in_path, sheet_name=in_tab)
except Exception as e:
    print(f"Could not read file: {e}")

fig, [ax_total, ax_power, ax_time] = plt.subplots(3,1, sharex=True)
df_diff = df.diff()

print(df.head())
ax_total.step(df['Time'], df_diff["Lieferung"], marker='o', markersize=1)
ax_total.step(df['Time'], df_diff["Bezug"], marker='o', markersize=1)

#df.plot('Time', 'Lieferung', ax=ax_total, marker='x')
#df.plot('Time', 'Bezug', ax=ax_total, marker='x')
ax_total.set_ylabel("Energy per Interval [kWh]")

power_out = df_diff["Lieferung"]*(3600) / (df_diff['Time'].dt.seconds)
power_in = df_diff["Bezug"]*(3600) / (df_diff['Time'].dt.seconds)

ax_power.step(df['Time'], power_out, marker='o', markersize=1)
ax_power.step(df['Time'], power_in, marker='o', markersize=1)
ax_power.set_ylabel("Power [kW]")

ax_time.plot(df['Time'], df_diff['Time'].dt.seconds, marker='.', color='green')
ax_time.set_ylabel("ΔT [s]")

fig.tight_layout()
plt.show()

