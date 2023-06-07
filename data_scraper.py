import requests
import pandas as pd 
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import os 

class BeeradvocateScraper:
    def __init__(self):
        self.base_url='https://www.beeradvocate.com'

    def save_csv(self):

        return

    def get_beer_styles(self):
        """
        getting the style, sub-style and the url that brings
        to the page that containt the list of the beers in that 
        substyle
        """
        beer_styles_url=self.base_url+'/beer/styles/'

        r=requests.get(beer_styles_url,'html.parser')

        soup = BeautifulSoup(r.text, 'html.parser')

        styles=soup.find_all('div',{'class':'stylebreak'})

        beers_style_type=[]
        for style in styles:
            # style name
            types_beer=style.find_all('a')

                #loop2
            for beer_type in types_beer:

                # style name
                style_name=style.b.text.replace('/','_')
                #beertype url 
                beer_type_url='https://www.beeradvocate.com'+beer_type["href"]
                #beertype name
                beer_type_name=beer_type.text.replace('/','_')

                beers_style_type.append(
                        {
                            'style_name':style_name,
                            'beer_type_url':beer_type_url,
                            'beer_type_name':beer_type_name
                        })

        df=pd.DataFrame(beers_style_type)
        df['beer_type_id']=df.beer_type_url.str.extract('(\d+)')
        return df

    def get_beer_style_info(self,style_folder_name='Beer_styles_data'):

        """
        Scrapes beer style stats and description and makes a csv file in 
        Data/Beer_styles_data as beer_styles.csv
        
        """

        os.makedirs(F"Data/{style_folder_name}", exist_ok=True)

        desctiption=[]
        stats=[]

        df_style=self.get_beer_styles()

        for url in tqdm(df_style.beer_type_url.values):
        
            r=requests.get(url,'html.parser')

            soup = BeautifulSoup(r.text, 'html.parser')

            beer_style=soup.find('div',{'id':"ba-content"})
            style_info=beer_style.select_one(":nth-child(1)").text

            stats.append(style_info.split('\n')[-3])
            desctiption.append(" ".join(style_info.split('\n')[0:-3]).strip())
        
        df_style['stats']=stats
        df_style['desctiption']=desctiption

        df_style.to_csv(f'Data/{style_folder_name}/beer_styles.csv',index=False)


    def get_beers_by_type(self,beer_type_url,start=0):
        row_data_list_tot=[]
        while True:
                url=beer_type_url+f'?sort=revsD&start={str(start)}'
                r=requests.get(url,'html.parser')
                #time.sleep(0.5)
                soup = BeautifulSoup(r.text, 'html.parser')

                table_soup=soup.table.find_all('tr')

                row_data_list=[]

                for e in table_soup:
                        row=e.find('td',{'class':'hr_bottom_light'})
                        if row is not None:
                                beer=e.find_all("td")
                                beer_company_page_url=beer[0].a.a['href']
                                beer_company_name=beer[0].a.a.text
                                beer_page=beer[0].a['href']
                                beer_name=beer[0].a.b.text
                                abv=beer[1].text
                                rating=beer[2].text.replace(',','')
                                avg=beer[3].text
                                last_active=beer[4].text
                                row_data={
                                        'beer_name':beer_name,
                                        'beer_page':beer_page,
                                        'beer_company_name':beer_company_name,
                                        'beer_company_page_url':beer_company_page_url,
                                        'abv':abv,
                                        'rating':rating,
                                        'avg':avg,
                                        'last_active':last_active
                                        }
                                row_data_list.append(row_data)
                start+=50
                row_data_list_tot.append(row_data_list)
                #stops if there are no more beers left for that style
                if len(row_data_list)==0:
                        break

        # list of list -> list 
        row_data_list_tot = [item for sublist in row_data_list_tot for item in sublist]

        return row_data_list_tot

    # in progress
    def get_beer_data(self,folder_name='BeerDataByStyle'):
        os.makedirs(F"Data/{folder_name}", exist_ok=True)

        scraped_styles=[]
        scraped_styles_time=[]

        for e in os.listdir(F"Data/{folder_name}"):
            scraped_styles.append(F"{e}")
            scraped_styles_time.append(os.path.getctime(F"Data/{folder_name}/{e}"))

        #if len(scraped_styles_time)!=0:
            #last_csv_file=scraped_styles[scraped_styles_time.index(max(scraped_styles_time))]
            #scraped_styles.remove(last_csv_file)
        #print(last_csv_file)
        



        df_style=self.get_beer_styles()

        df_style_left=df_style.loc[(df_style.beer_type_name+'.csv').isin(scraped_styles)==False]

        for i in tqdm( range(len(df_style_left))):

            df_i=df_style_left.iloc[i]

            beer_type_url=df_i.beer_type_url
            beer_type_url=df_i.beer_type_url  
            style_name=df_i.style_name                                         
            beer_type_name=df_i.beer_type_name   

            data=self.get_beers_by_type(beer_type_url,start=0) 
            df_beer=pd.DataFrame(data)

            df_beer['beer_type_url']=beer_type_url
            df_beer['style_name']=style_name
            df_beer['beer_type_name']=beer_type_name
            df_beer.to_csv(F"Data/{folder_name}/{beer_type_name}.csv",index=False)

    '''
    def get_beer_data_final(self):
        df_scrape=pd.read_csv('beer_data3.csv')

        #df_scrape['beer_id']=df_scrape.index
        df_scrape['beer_page_url']='https://www.beeradvocate.com'+df_scrape['beer_page']
        #df

        df_scrape



        last_backup=[]
        last_backup_time=[]


        folder_name='beer_data_final'
        folder_name='scraped_data'

        for e in os.listdir(folder_name):
            last_backup.append(F"{folder_name}/{e}")
            last_backup_time.append(os.path.getctime(F"{folder_name}/{e}"))


        if len(last_backup_time)==0:
            df_backup=pd.DataFrame()
        else:

            csv_file=last_backup[last_backup_time.index(max(last_backup_time))]
            df_backup=pd.read_csv(csv_file)



            df_scrape=df_scrape.loc[df_scrape.beer_id.isin(df_backup.beer_id.values)==False]






        #var 
        l=[]


        error_list=['Not listed','Needs more ratings']

        beer_page_urls=df_scrape.beer_page_url.values
        beer_ids=df_scrape.beer_id.values

        for i in tqdm(range(len(df_scrape))):


            #url=df_scrape.iloc[i].beer_page_url
            #beer_id=df_scrape.iloc[i].beer_id


            url=beer_page_urls[i]
            beer_id=beer_ids[i]
            r=requests.get(url,'html.parser')


            soup = BeautifulSoup(r.text, 'html.parser')

            beer_stats=soup.find('dl',{'class':'beerstats'})
            
            if beer_stats is None:
                print('error',url)
                continue

            stats_vals=beer_stats.find_all('dd')



            d={}
            for e in stats_vals:
                if e.span is not None:
                    if e.text in error_list:
                        pass
                    else:
                    d[e.span['title']]=e.span.text
                elif e.a is not None:
                    if 'title' not in e.a.attrs:
                        d['location']=e.text

                    else:
                        d[e.a['title']]=e.a.text

                    pass
                else:
                    pass

            #note
            note_soup=soup.find('div', {'style':'clear:both; margin:0; padding:0px 20px; font-size:1.05em;'})
            d['note']=note_soup.text

            reviews=soup.find_all('div',{'id':"rating_fullview_content_2"})
            reviews=[str(e) for e in reviews]
            d['reviews']=reviews
            
            d['beer_id']=beer_id



            l.append(d)

            if len(l)%1000==0:
                
                timestr = time.strftime("%Y%m%d-%H%M%S")
                df_backup=pd.concat([df_backup,pd.DataFrame(l)],ignore_index=True)

                df_backup.to_csv(F'{folder_name}/backup_{timestr}.csv',index=False)
                l=[]

                del_oldest=[]
                del_oldest_time=[]
                for csvs in os.listdir(folder_name):
                    del_oldest.append(F"{folder_name}/{csvs}")
                    del_oldest_time.append(os.path.getctime(F"{folder_name}/{csvs}"))
                if len(del_oldest_time)>=3:
                    del_csv_file=del_oldest[del_oldest_time.index(min(del_oldest_time))]
                    os.remove(del_csv_file)
                    
                

        df_backup=pd.concat([df_backup,pd.DataFrame(l)],ignore_index=True)
        df_backup.to_csv(F'{folder_name}/Beer_data_final.csv',index=False)

    '''