import pandas as pd

data = pd.read_csv('Bitcoin_addresses_LATEST.txt', sep=" ", header=None)
data.columns = ["address"]

print(data)

print(data['address'].to_numpy()[data['address'].to_numpy() == '77771111111111111111111114oLvT2'])
print(data['address'].to_numpy()[data['address'].to_numpy() == '1111111111111111111114oLvT2'])

#print( data['address'].to_numpy()[data['code1'].to_numpy() == code].item() )

#print('1111111111111111111114oLvT2' in data['address'].unique())
