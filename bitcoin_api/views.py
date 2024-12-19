import json

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv


class BitcoinInfoView(APIView):
    def get_15m_price(self):
        blockchain_api = "https://blockchain.info/ticker"
        try:
            response = requests.get(blockchain_api)
            price = json.loads(response.content)["EUR"]["15m"]
            return price
        except Exception as e:
            raise ValueError(f"Failed to get 15m delayed price: {str(e)}")

    def get_date_month_ago(self):
        today = datetime.now()
        one_month_ago = today - timedelta(days=30)

        return one_month_ago.strftime('%Y-%m-%d')

    def get_exchange_rate(self):
        date = self.get_date_month_ago()

        load_dotenv()
        API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")

        url = f"https://api.exchangeratesapi.io/{date}?base=EUR&access_key={API_KEY}"

        try:
            response = requests.get(url)
            json_response = json.loads(response.content)
            return json_response["rates"]["GBP"]
        except Exception as e:
            raise ValueError(f"Failed to get exchange rate: {str(e)}")

    def get(self, request, *args, **kwargs):
        price_eur = self.get_15m_price()
        exchange_rate = self.get_exchange_rate()
        price_gbp = price_eur * exchange_rate

        return Response({'bitcoin_eur': price_eur, 'eur_to_gbp': exchange_rate, 'bitcoin_gbp': price_gbp}, status=status.HTTP_200_OK)



