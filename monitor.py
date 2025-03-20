from selenium import webdriver
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests


def send_line_message(user_id, message):
    channel_access_token = 'AlmZ1EpoyauQtdM45RGpDvMCxFAxNanpAdCkm5WlcLJvhIeOaDmfw9IpB5RszpeTXNMzXUVJjTz95ehZ+DlecVeWPHqQK50kzBGBF4jw/jAQJW4P4GmpAUvrCGYVFoeRXJqTGBJKOJLZWGCMeGTcZQdB04t89/1O/w1cDnyilFU='  # 替換為你的 Channel Access Token
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {channel_access_token}',
    }
    payload = {
        'to': user_id,
        'messages': [{
            'type': 'text',
            'text': message,
        }],
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("消息已成功發送！")
    else:
        print("發送消息失敗！", response.text)



def convert_date(date_str):
    # 提取年份、月份和日期
    year = date_str[:3]     # 提取前3位作為年份
    month = int(date_str[3:5])  # 提取4-5位作為月份
    day = int(date_str[5:7])    # 提取6-7位作為日

    # 返回格式化的日期字符串
    return f"{year}年{month}月{day}日"

def convert_locate(date_str):
    # 提取年份、月份和日期
    name = date_str[:2]     # 提取前3位作為年份
    # 返回格式化的日期字符串
    return name




def open_and_operate(args):
   
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless=new")  
    chrome_options.add_argument('--disable-gpu')  
    chrome_options.add_argument('--no-sandbox') 
    
    driver = webdriver.Chrome(options=chrome_options)
    
  
    driver.get(args[0])
    
    wait = WebDriverWait(driver, 10)  # 最多等待 10 秒
    wait.until(EC.visibility_of_element_located((By.NAME, 'licenseTypeCode')))
    driver.find_element(By.NAME, "licenseTypeCode").send_keys('普通重型機車')

    driver.find_element(By.ID, "expectExamDateStr").send_keys(args[1])

    Select(driver.find_element(By.NAME, "dmvNoLv1")).select_by_visible_text(args[2]) 

    driver.find_element(By.NAME, "dmvNo").send_keys(args[3])
    

    driver.find_element(By.XPATH, "//a[@onclick='query();']").click()
    
    driver.find_element(By.XPATH, "/html/body/div[11]/div/center/a[3]").click()

    target_date = convert_date(args[1])  # 你可以換成你想要查詢的日期

   
    rows = driver.find_elements(By.XPATH, '//*[@id="trnTable"]/tbody/tr')
    for row in rows:
        try:
            # 查找並取得日期
            date = row.find_element(By.XPATH, './/td[1]').text
        
            # 如果日期不符合，直接跳過這一行
            if target_date not in date:
                continue
            # 查找第二個欄位中的場次描述信息，檢查是否為重考生場次
            session_info = row.find_element(By.XPATH, './/td[2]').text
            if "重考" not in session_info:
                continue

            # 查找第三個欄位，查看是否顯示「額滿」
            status = row.find_element(By.XPATH, './/td[3]').text
            if "額滿" in status:
                    print(f"{date}, {convert_locate(args[3])}, 額滿")
            else:
                send_line_message(
                user_id='你的LINE ID', 
                message= target_date +" "+ args[3] + ' 還有名額!!!!!!!!!!!'
            )
                print(f"{target_date},{args[3]}還有名額!!!!!!!!!!!")
        except Exception as e:
            print(f"錯誤: {e}")
    driver.quit()    
    




# 網頁；日期、時間、地點
urls = [
     ["https://www.mvdis.gov.tw/m3-emv-trn/exm/locations#gsc.tab=0",
            '1131025',
            '新竹區監理所（桃竹苗）',
            '桃園監理站(桃園市介壽路416號)',
    ],
    ["https://www.mvdis.gov.tw/m3-emv-trn/exm/locations#gsc.tab=0",
            '1131025',
            '新竹區監理所（桃竹苗）',
            '中壢監理站(桃園縣中壢市延平路394號)',
    ],
    ["https://www.mvdis.gov.tw/m3-emv-trn/exm/locations#gsc.tab=0",
            '1131025',
            '臺北區監理所（北宜花）',
            '板橋監理站(新北市中和區中山路三段116號)'
    ],
    ["https://www.mvdis.gov.tw/m3-emv-trn/exm/locations#gsc.tab=0",
            '1131025',
            '臺北區監理所（北宜花）',
            '蘆洲監理站(新北市蘆洲區中山二路163號)'
    ],
    ["https://www.mvdis.gov.tw/m3-emv-trn/exm/locations#gsc.tab=0",
            '1131111',
            '新竹區監理所（桃竹苗）',
            '桃園監理站(桃園市介壽路416號)',
    ],
    ["https://www.mvdis.gov.tw/m3-emv-trn/exm/locations#gsc.tab=0",
            '1131111',
            '新竹區監理所（桃竹苗）',
            '中壢監理站(桃園縣中壢市延平路394號)',
    ],
    ["https://www.mvdis.gov.tw/m3-emv-trn/exm/locations#gsc.tab=0",
            '1131111',
            '臺北區監理所（北宜花）',
            '板橋監理站(新北市中和區中山路三段116號)'
    ],
    ["https://www.mvdis.gov.tw/m3-emv-trn/exm/locations#gsc.tab=0",
            '1131101',
            '新竹區監理所（桃竹苗）',
            '桃園監理站(桃園市介壽路416號)',
    ],
    ["https://www.mvdis.gov.tw/m3-emv-trn/exm/locations#gsc.tab=0",
            '1131101',
            '新竹區監理所（桃竹苗）',
            '中壢監理站(桃園縣中壢市延平路394號)',
    ],
    ["https://www.mvdis.gov.tw/m3-emv-trn/exm/locations#gsc.tab=0",
            '1131101',
            '臺北區監理所（北宜花）',
            '板橋監理站(新北市中和區中山路三段116號)'
    ],
    ["https://www.mvdis.gov.tw/m3-emv-trn/exm/locations#gsc.tab=0",
            '1131101',
            '臺北區監理所（北宜花）',
            '蘆洲監理站(新北市蘆洲區中山二路163號)'
    ]
]

threads = []


while(True):
    for url in urls:
        thread = threading.Thread(target=open_and_operate, args=(url,))
        threads.append(thread)
        thread.start()  

    for thread in threads:
        thread.join()
    time.sleep(3600)



