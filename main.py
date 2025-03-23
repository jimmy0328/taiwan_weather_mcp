import os
import json
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise ValueError("請在 .env 檔案中設定 OPENWEATHER_API_KEY")

TAIWAN_CITIES = {
    "臺北市": {"lat": 25.0330, "lon": 121.5654},
    "新北市": {"lat": 25.0160, "lon": 121.4630},
    "桃園市": {"lat": 24.9936, "lon": 121.3009},
    "臺中市": {"lat": 24.1477, "lon": 120.6736},
    "臺南市": {"lat": 22.9999, "lon": 120.2270},
    "高雄市": {"lat": 22.6273, "lon": 120.3014},
    "基隆市": {"lat": 25.1283, "lon": 121.7392},
    "新竹市": {"lat": 24.8138, "lon": 120.9675},
    "嘉義市": {"lat": 23.4800, "lon": 120.4497},
    "宜蘭縣": {"lat": 24.7021, "lon": 121.7378},
    "新竹縣": {"lat": 24.8387, "lon": 121.0179},
    "苗栗縣": {"lat": 24.5602, "lon": 120.8214},
    "彰化縣": {"lat": 24.0759, "lon": 120.5446},
    "南投縣": {"lat": 23.9596, "lon": 120.6853},
    "雲林縣": {"lat": 23.7092, "lon": 120.4313},
    "嘉義縣": {"lat": 23.4518, "lon": 120.2555},
    "屏東縣": {"lat": 22.5519, "lon": 120.5488},
    "臺東縣": {"lat": 22.7583, "lon": 121.1445},
    "花蓮縣": {"lat": 23.9920, "lon": 121.6012},
    "澎湖縣": {"lat": 23.5711, "lon": 119.5793}
}

mcp = FastMCP("taiwan-weather")

@mcp.tool()
async def get_taiwan_weather(city: str) -> str:
    if city not in TAIWAN_CITIES:
        return "請提供有效的台灣縣市名稱"

    async with httpx.AsyncClient() as client:
        params = {
            "lat": TAIWAN_CITIES[city]["lat"],
            "lon": TAIWAN_CITIES[city]["lon"],
            "appid": API_KEY,
            "units": "metric",
            "lang": "zh_tw"
        }
        response = await client.get(
            "http://api.openweathermap.org/data/2.5/weather",
            params=params
        )
        response.raise_for_status()
        data = response.json()

        weather_info = {
            "縣市": city,
            "溫度": f"{data['main']['temp']}°C",
            "天氣": data["weather"][0]["description"],
            "濕度": f"{data['main']['humidity']}%",
            "風速": f"{data['wind']['speed']} m/s"
        }

        return json.dumps(weather_info, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    mcp.run()
