import openai
import os
import requests

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

AI_KEY = os.getenv('GPT_KEY')
openai.api_key = AI_KEY


class Chatbot(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    @commands.Cog.listener()
    async def on_ready(self):
        print('ChatBot.py is online.')


    #gpt model and how it behaves
    @commands.command()
    async def gpt(self, ctx, message, *, question):
        GPT_API_URL = 'https://api.openai.com/v1/chat/completions'  
    
        headers = {
        'Authorization': f'Bearer {AI_KEY}',
        'Content-Type': 'application/json'
    }
    
        data = {
        'model': 'gpt-4',
        'messages': [
        {
        'role': 'system',
        'content': "You are helpful assistant"
        }, {
        'role': 'user',
        'content': question
        }]
    }
    
        response = requests.post(GPT_API_URL, headers=headers, json=data)
    
        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content'].strip()
            await ctx.send(answer)
        else:
            error = response.json().get('error', 'Unknown error')
            await ctx.send(f'Error, could not get a response from GPT: {error}')

   



async def setup(client):
    await client.add_cog(Chatbot(client))