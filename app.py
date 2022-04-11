from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', attrs={'class':'coingecko-table table-responsive'})
rows = table.find_all('th', attrs={'class':'font-semibold text-center'})
row_length = len(rows)

temp = [] #initiating a list 

for i in range(3, row_length):
#insert the scrapping process here

	# get date
	period = rows[i].get_text()

	# get volume
	volume = table.find_all('td', attrs={'class':'text-center'})[i].get_text()
	if volume == "\nN/A\n":
		# print(volume)
		continue
	temp.append((period, volume)) 

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns = ['period', 'volume'])
# print(data.head())

# #insert data wrangling here

data['volume'] = data['volume'].str.replace(",","")
data['volume'] = data['volume'].str.replace("$","")
data['volume'] = data['volume'].str.replace("\n","")
data['volume'] = data['volume'].astype('float64')
data['period'] = data['period'].astype('datetime64')

data = data.set_index('period')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["volume"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)