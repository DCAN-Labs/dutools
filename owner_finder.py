from pathlib import Path
import argparse
import pandas


parser = argparse.ArgumentParser(description='Pass an agedu report to this and it will collect the owners of the dirs/files')
parser.add_argument('--csv', help="""Input csv, formatted with columns: Size, Path""", type=str)
parser.add_argument('--output', help='Where you want this file written to', type=str)
args = parser.parse_args()

agedu = Path(args.csv)
if not args.output:
    output_path = agedu.stem + '_with_owners.csv'
else:
    output_path = args.output

if agedu.is_file():
    dataframe = pandas.read_csv(args.csv)
    dataframe['Owner'] = 'N/A'
    dataframe['Group'] = 'N/A'
    dataframe['Contacted'] = 'no'
    for index, row in dataframe.iterrows():
        try:
            space = Path(row['Path'])
            dataframe.at[index,'Owner'] = space.owner()
            dataframe.at[index,'Group'] = space.group()
        except (KeyError, PermissionError):
            pass

    print(dataframe)
    dataframe.to_csv(output_path, index=False, sep="\t")
else:
    print("Try passing a valid file to the --csv argument?")

