import pandas as pd
import matplotlib.pyplot as mpl
import datetime as dt
import requests

def getData(dataUrl):
    response = requests.request('GET', dataUrl, headers={'Accept': 'application/json'})
    data = response.json()
    return pd.DataFrame(data.get("data"))

def main():
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    airData = getData("http://atis.koca.go.kr/ATIS/aircraft/statList01.do?AIR_GUBUN=all")
    wantedOwner = ["대한항공","아시아나항공","진에어","제주항공","티웨이","에어부산","에어서울","에어프레미아","에어로케이항공","산림청","에어인천","이스타","중앙119구조본부" ]
    mpl.rcParams["font.family"] = 'NanumGothicOTF'
    mpl.rcParams["figure.figsize"] = (11,12)
    # airData 데이터프레임에서 각 회사의 항공기 수와 20년 이상 된 항공기 수를 계산합니다.
    airData = airData[airData['REG_CUSER'].isin(wantedOwner)]
    companies = airData['REG_CUSER'].unique()

    company_aircraft_count = airData.groupby('REG_CUSER')['REG_CUSER'].count()
    company_old_aircraft_count = airData[airData['AIR_AGE'].astype(int) >= 20].groupby('REG_CUSER')['REG_CUSER'].count()

    # 그래프를 그리기 위한 데이터를 준비합니다.
    data = {
        'Total': company_aircraft_count,
        '20+ years old': company_old_aircraft_count
    }

    # Stacked Bar 그래프를 그립니다.
    ax = pd.DataFrame(data).plot.bar(stacked=False)
    ax.set_xticklabels(companies)

    mpl.text(4,100,now,ha="center",va="center",fontsize=10)
    #각 막대에 갯수를 표시합니다.
    for p in ax.patches:
            ax.annotate(p.get_height(), (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    mpl.savefig('foo.png')

main()