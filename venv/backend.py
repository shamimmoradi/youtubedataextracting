from logging import exception
import os 
from googleapiclient.discovery import build
import pandas as pd
from requests import request
from xlsxwriter import Workbook
import google_auth_oauthlib.flow



api_key  = 'AIzaSyCAFgPXIllbbdaQBxumy1BRbJOwmQCp3NM'
youtube = build('youtube','v3', developerKey=api_key)

# function to get channels name
def get_channel_id (youtube,topic):
    all_id = []
    try :
        
        request = youtube.search().list(
        part="snippet",
        maxResults=200,
        type="channel",
        q= topic
    )
        response = request.execute()
        for i in range(len(response['items'])) :
            data = response['items'][i]['snippet']['channelId'] 
            all_id.append(data)
        return all_id
    except Exception as e:
        print(e)

def get_channel_stats(youtube,channel_ids) :
    try :
        all_data = []
        request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id= ','.join(channel_ids)
        
        )
        response = request.execute()
        for i in range(len(response['items'])):
            if response['items'][i]['statistics']['hiddenSubscriberCount'] == False :
                data = dict(Channel_link="https://www.youtube.com/channel/" + response['items'][i]['id'],
                            Channel_name=response['items'][i]['snippet']['title'],
                            Subscribers=response['items'][i]['statistics']['subscriberCount'])

            elif response['items'][i]['statistics']['hiddenSubscriberCount'] == True :
                data = dict(Channel_link="https://www.youtube.com/channel/" + response['items'][i]['id'],
                            Channel_name=response['items'][i]['snippet']['title'],
                            Subscribers= 'hiddenSubscriber')



            all_data.append(data)
        
        return all_data
    except Exception as e:
        print(e)

def make_excel(data):
    try :
        channel_data = pd.DataFrame(data)
        writer = pd.ExcelWriter("channeldata.xlsx", engine='xlsxwriter')
        channel_data.to_excel(writer, sheet_name='Sheet1' , index = False)
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        writer.save()
        
    except Exception as e:
        print(e)





if __name__ == "__main__":
    topic = input('insert a topic :')
    channel_ids = get_channel_id(youtube,topic)
    channels_stats = get_channel_stats(youtube , channel_ids)
    excel_data = make_excel(channels_stats)
    
