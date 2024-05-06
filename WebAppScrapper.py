# importirani biblioteki i framework
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st


# funkcija koja prakja request kon serverot za prezemanje na url, kade ja prezema sodrzhinata na sajtot prezemajki
# site elementi koi imaat class atributi
def scrape_data(url, class_name, element):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find_all(class_=class_name)
    return [item.get_text(separator=' ') for item in data if item.name == element]


# funkcija koja gi ekstraktira samo podatocite od elementite so class atributi
def extract_attributes_elements(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    class_attributes = set()

    for tag in soup.find_all(class_=True):
        classes = tag['class']
        for c in classes:
            class_attributes.add(c)

    html_elements = set([tag.name for tag in soup.find_all()])

    return list(class_attributes), list(html_elements)

# kod vo koj e vnesen UI na aplikacijata


st.title('Web Scraping App')
url = st.text_input('Enter the URL of the website:')
# uslov koj se ispolnuva dokolku e vnesen url
if url:
    class_attributes, html_elements = extract_attributes_elements(url)
    selected_class = st.selectbox('Select Class Attribute:', class_attributes)
    selected_element = st.selectbox('Select HTML Element:', html_elements)
# if ciklus koj proveruva dali url-to e validno so funkcija samo da gi prikazhi ekstraktiranite podatoci od sajtot
if st.button('Scrape Data'):
    if url and selected_class and selected_element:
        scraped_data = scrape_data(url, selected_class, selected_element)
        st.write(scraped_data)
    else:
        st.write('Please enter a valid URL and select both a Class Attribute and an HTML Element.')

# if ciklus koj se aktivira dokolku gornite funkcii/so dopolnitelna funkcija koja pokraj ekstrakcija, vrshi
# generiranje i download na tie podatoci vo csv format
if st.button('Scrape'):
    scraped_data = scrape_data(url, selected_class, selected_element)

    df = pd.DataFrame(scraped_data, columns=[selected_element])
    csv = df.to_csv(index=False)

    st.download_button(label='Download CSV', data=csv, file_name='scraped_data.csv', mime='text/csv')
