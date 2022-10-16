from typing import Optional
from fastapi import FastAPI,Response
import requests
from bs4 import BeautifulSoup
import pandas as pd
from fastapi.responses import FileResponse
import plotly.express as px
import json
from fastapi.testclient import TestClient

#uvicorn main:app --host 0.0.0.0 --port 10000


app = FastAPI()



def obtenerDatos(fecha=''):

	print((fecha))
	if len(fecha)==0:
		url = "https://tarifaluzhora.es/"
	else:
		dia = fecha.split('-')[0]
		mes = fecha.split('-')[1]
		año = fecha.split('-')[2]
		#https://tarifaluzhora.es/?tarifa=pcb&fecha=14%2F10%2F2022

		url = "https://tarifaluzhora.es/?tarifa=pcb&fecha="+dia+"%2F"+mes+"%2F"+año

	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")


	return soup


@app.get("/")
async def root():



	soup =obtenerDatos()

	#print(type(df['precio'][0]))

	resultsDia = soup.find(id="price_summary")

	###### Día Consulta

	#print(resultsDia)
	resultsfecha = resultsDia.find("div", class_="gauge_day")

	dia = resultsfecha.find_all("span",class_="sub_text")
	#print("dia fecha",dia)
	for day in dia:
		print(day.text)



	###### Precio hora y día consulta
	resultsPrecioInstantaneo = resultsDia.find("div", class_="gauge_hour")
	horaInstante = resultsPrecioInstantaneo.find_all("h2",class_="title")
	precioInstante = resultsPrecioInstantaneo.find_all("span",class_="sub_text")
	#print(precioInstante)
	#print(horaInstante)

	for precio in precioInstante:
		print(precio.text.replace('\n',''))
	for hora in horaInstante:
		print(hora.text.split("Precio a las")[1].replace('\n',''))


	###### Precio más alto
	resultsPrecioMasBajo = resultsDia.find("div", class_="gauge_low")

	horaMasBajo = resultsPrecioMasBajo.find_all("span",class_="main_text")
	precioMasBajo = resultsPrecioMasBajo.find_all("span",class_="sub_text")


	#print(horaMasBajo)
	#print(precioMasBajo)
	for precio in precioMasBajo:
		print(precio.text.replace('\n',''))
	for hora in horaMasBajo:
		print(hora.text)

	####### Precio más bajo
	resultsPrecioMasAlto = resultsDia.find("div", class_="gauge_hight")

	horaMasAlto = resultsPrecioMasAlto.find_all("span",class_="main_text")
	precioMasAlto = resultsPrecioMasAlto.find_all("span",class_="sub_text")

	for precio in precioMasAlto:
		print(precio.text.replace('\n',''))
	for hora in horaMasAlto:
		print(hora.text)
	#print(horaMasAlto)
	#print(precioMasAlto)

	obtenerDatos("02-02-2022")



	#return FileResponse("yourfile.png", media_type="image/jpeg", filename="vector_image_for_you.png")
	return {"message": "Hello there"}

	#fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 1])



@app.get("/precioluz")
def precioluz():
	soup =obtenerDatos()

	results = soup.find(id="hour_prices")
	#print(results.prettify())

	horas = results.find_all("span", itemprop="description")
	precios = results.find_all("span", itemprop="price")
	monedas = results.find_all("meta", itemprop="priceCurrency")
	#monedas = results.find( itemprop="priceCurrency")

	monedasList = []
	preciosList = []
	horasList = []

	#print(precios)

	for moneda in monedas:
		#print(moneda.get('content'))
		monedasList.append(moneda.get('content'))
	for precio in precios:
		#print(precio.text)
		preciosList.append(precio.text.split(' €/kWh')[0])


	for hora in horas:
		print(hora.text.split(':')[0])
		horasList.append(hora.text.split(':')[0])

	df = pd.DataFrame(list(zip(monedasList, preciosList,horasList)), 
	           columns =['Moneda', 'precio','hora'])
	#print(df.sort_values(by=['hora']))
	print(df)

	df['precio']=(df['precio']).astype("float32")
	js = df.to_json(orient = 'records')
	#js = companyDataArval.dataFrameCompany.tail().to_json(orient = 'records')
	jsonObjectData = json.loads(js)
	print(jsonObjectData)



	resultsDia = soup.find(id="price_summary")

	###### Día Consulta

	#print(resultsDia)
	resultsfecha = resultsDia.find("div", class_="gauge_day")

	dia = resultsfecha.find_all("span",class_="sub_text")
	#print("dia fecha",dia)
	for day in dia:
		print(day.text)


	entry = {'dia': day.text}

	jsonObjectData.append(entry)
	return jsonObjectData



	return jsonObjectData




@app.get("/precioluz/{fecha}")
def precioluz(fecha:str):

	soup =obtenerDatos(fecha)

	results = soup.find(id="hour_prices")
	#print(results.prettify())

	horas = results.find_all("span", itemprop="description")
	precios = results.find_all("span", itemprop="price")
	monedas = results.find_all("meta", itemprop="priceCurrency")
	#monedas = results.find( itemprop="priceCurrency")

	monedasList = []
	preciosList = []
	horasList = []

	#print(precios)

	for moneda in monedas:
		#print(moneda.get('content'))
		monedasList.append(moneda.get('content'))
	for precio in precios:
		#print(precio.text)
		preciosList.append(precio.text.split(' €/kWh')[0])


	for hora in horas:
		print(hora.text.split(':')[0])
		horasList.append(hora.text.split(':')[0])

	df = pd.DataFrame(list(zip(monedasList, preciosList,horasList)), 
	           columns =['Moneda', 'precio','hora'])
	#print(df.sort_values(by=['hora']))
	print(df)

	df['precio']=(df['precio']).astype("float32")
	js = df.to_json(orient = 'records')
	#js = companyDataArval.dataFrameCompany.tail().to_json(orient = 'records')
	jsonObjectData = json.loads(js)

	print(jsonObjectData)

	#print(type(df['precio'][0]))

	resultsDia = soup.find(id="price_summary")

	###### Día Consulta

	#print(resultsDia)
	resultsfecha = resultsDia.find("div", class_="gauge_day")

	dia = resultsfecha.find_all("span",class_="sub_text")
	#print("dia fecha",dia)
	for day in dia:
		print(day.text)


	entry = {'dia': day.text}

	jsonObjectData.append(entry)
	return jsonObjectData



@app.get("/grafico/precioluz/")
def precioluzGrafico():
	soup =obtenerDatos()

	results = soup.find(id="hour_prices")
	#print(results.prettify())

	horas = results.find_all("span", itemprop="description")
	precios = results.find_all("span", itemprop="price")
	monedas = results.find_all("meta", itemprop="priceCurrency")
	#monedas = results.find( itemprop="priceCurrency")

	monedasList = []
	preciosList = []
	horasList = []

	#print(precios)

	for moneda in monedas:
		#print(moneda.get('content'))
		monedasList.append(moneda.get('content'))
	for precio in precios:
		#print(precio.text)
		preciosList.append(precio.text.split(' €/kWh')[0])


	for hora in horas:
		print(hora.text.split(':')[0])
		horasList.append(hora.text.split(':')[0])




	df = pd.DataFrame(list(zip(monedasList, preciosList,horasList)), 
	           columns =['Moneda', 'precio','hora'])
	#print(df.sort_values(by=['hora']))
	#print(df)

	df['precio']=(df['precio']).astype("float32")

	resultsDia = soup.find(id="price_summary")

	###### Día Consulta

	#print(resultsDia)
	resultsfecha = resultsDia.find("div", class_="gauge_day")

	dia = resultsfecha.find_all("span",class_="sub_text")
	#print("dia fecha",dia)
	for day in dia:
		print(day.text)

	fig = px.bar(df,x='hora',y='precio', title = day.text)
	img_bytes = fig.to_image(format="png")
	#print(img_bytes)

	#figura= fig.write_image("yourfile.png") 
	#return Response(content=figura, media_type="image/png")
	return Response(content=img_bytes, media_type="image/png")







