import asyncio
import json
import websockets


class BinanceWebSocket:
    def __init__(self, symbol):
        self.symbol = symbol
        self.ws_url = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@trade"

    async def listen(self):
        """Connects to WebSocket and gets data about deals in real-time"""
        async with websockets.connect(self.ws_url) as ws:
            print(f"Connected to Binance WebSocket: {self.symbol.upper()}")
            while True:
                try:
                    data = await ws.recv()
                    trade = json.loads(data)
                    price = trade["p"]  # Deal price
                    volume = trade["q"]  # Deal Volume
                    print(f"💰 {self.symbol.upper()} | Price: {price} | Volume: {volume}")
                except Exception as e:
                    print(f"WebSocket Error: {e}")
                    break

    def run(self):
        """Launch WebSocket-client"""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listen())
