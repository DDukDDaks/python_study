import requests
import json
import pandas as pd
import time
# import csv
# f=open('매물정보_추출_테스트_ver1.csv','a',newline='')
# wr = csv.writer(f)
apt_data_df = pd.DataFrame(columns=['시','군구','동','아파트이름','층수',
    '몇동','몇호','방향','거래타입','가격','면적','평수','평단가','매전갭',
    '최근실거래가','최근거래날짜','실거래가 대비 호가 퍼센트','특징',
    '설명','연식','세대수','공시가격','평균관리비','중개수수료',
    '취득세','보유세','공인중개사','중개사이름','중개사번호','링크'])
headers = {
    'Accept': '*/*',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Referer': 'https://new.land.naver.com/complexes/4401?ms=35.1599,126.8018956,16&a=APT:ABYG:JGC&e=RETAIL',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.57 Whale/3.14.133.23 Safari/537.36',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE2NTA2NTQzNDYsImV4cCI6MTY1MDY2NTE0Nn0.CPWwXaq7urgnW1tUyyEqOj5m-Kg75zQFosok1Q4iJ4E',
    
}

def apt_detail_object(json_data,complexNo):
    # 매물리스트에 있는 매물 정보 긁어오는 함수 /
    for item in json_data['articleList']:
        try :
            code = item['articleNo'] #매물코드
        except:
            code = ''
        #매물링크    
        apt_link = 'https://m.land.naver.com/article/info/'+code   

        try :
            apt_name = item['articleName'] #아파트이름
        except:
            apt_name = ''
        
        try :
            trade_type = item['tradeTypeName'] #매매,전세,월세
        except:
            trade_type = ''
        
        try :
            floor = item['floorInfo'] #층수
        except:
            floor = ''
        print(floor)

        try :
            feature = item['articleFeatureDesc'] #매물 설명
        except:
            feature = ''
        try :
            tagList = item['tagList'] #매물 태그
        except:
            tagList = ''
        
        try :
            price = item['dealOrWarrantPrc'] #가격
            if trade_type =='월세':
                price = f"{item['dealOrWarrantPrc']}/{item['rentPrc']}"
        except:
            price = ''
            # 공시가격
        
        try :
            realtor = item['realtorName'] #공인중개사
        except:
            realtor = ''
        
        try :
            public_area = item['area1'] #공급평수
        except:
            public_area = ''
        
        try :
            private_area = item['area2'] #전용평수
        except:
            private_area = ''


    # 매물 개별로 하나하나 들어와서 다양한 상세정보 긁음.
        res = requests.get(f'https://new.land.naver.com/api/articles/{code}', headers=headers)
        # response = requests.get('https://new.land.naver.com/api/articles/2212513920', headers=headers, params=params, cookies=cookies)
        try :
            temp = json.loads(res.text)
        except:
            continue
        try : #A1,B1,B2 거래타입 파라미터로 사용
            type_code = temp['articleAddition']['tradeTypeCode'] 
        except :
            type_code = ''

        if trade_type == '매매':
            try : #물건 호가 ex)15000
                deal_price = temp['articlePrice']['dealPrice'] 
            except :
                deal_price = ''
        else : #전세, 월세
            try : #보증금 ex)15000
                deal_price = temp['articlePrice']['warrantPrice'] 
            except :
                deal_price = ''   

        try: #중개사 이름 #중개사 번호
            realtor_name = temp['articleRealtor']['representativeName'] 
            realtor_phone = temp['articleRealtor']['cellPhoneNo'] 
        except :    
            realtor_name=''
            realtor_phone=''
            
        try : #평수 순번, 실거래가, 매전갭 추출 시 필요
            pyeong_no=temp['landPrice']['ptpNo'] 
        except :
            pyeong_no = ''
        try : #방향 / 남동
            direction = temp['articleFacility']['directionTypeName'] 
        except:
            direction = ''    
        
        try : #평단가 1200
            pyeong_price = f"{int(temp['articlePrice']['priceBySpace'])}만원"
        except :
            pyeong_price = ''        
    
        
        try :# 몇동
            apt_dong_number = temp['landPrice']['dongNm'] 
        except :
            apt_dong_number = ''        
            
        try :  # 몇호
            apt_home_number = temp['landPrice']['hoNm']
        except :
            apt_home_number = ''    
            
        try : #1억으로 나누기 # 호실공시가격
            posted_price = f"{round(int(temp['landPrice']['price'])/100000000,1)}억원" 
        except :  
            posted_price = '안나옴'     
            
        try : # 평균관리비 만원단위 나누기
            management_cost = f"{int(temp['articleDetail']['monthlyManagementCost']/10000)}만원"
        except :
            management_cost = ''       

        # 중개수수료 취득세 보유세
        try :  # 중개수수료 만원으로 나누기
            broker_fee = f"{int(temp['articleTax']['brokerFee']/10000)}만원"
        except :
            broker_fee = '' 

        try :  # 취득세 1억넘을 때는 억으로 나누기 / 나머진 만원으로 나누기
            if len(str(temp['articleTax']['totalPrice']))>=9 :
                get_tax = f"{round(temp['articleTax']['totalPrice']/ 100000000,2)}억원"
            else : 
                get_tax = f"{int(temp['articleTax']['totalPrice']/ 10000)}만원"
        except :
            get_tax = ''


        try : # 보유세 만원단위 나누기
            have_tax = f"{int((int(temp['landPrice']['landPriceTax']['propertyTotalTax'])+int(temp['landPrice']['landPriceTax']['realEstateTotalTax']))/10000)}만원" 
        except :
            have_tax = ''  
            
        
        try :   #연식
            building_year = f"{temp['articleDetail']['aptUseApproveYmd'][:4]}년"
        except :
            building_year = ''

        try : #세대수
            household_Count = f"{temp['articleDetail']['aptHouseholdCount']}세대"
        except :
            household_Count = ''

        try : #주소
            city = temp['articleDetail']['exposureAddress'].split()[0]
            gungu = temp['articleDetail']['exposureAddress'].split()[1]
            dong = temp['articleDetail']['exposureAddress'].split()[2]
        except : 
            city = ''
            gungu = ''
            dong = ''

        # 매전 갭 구하기
        res = requests.get(f'https://new.land.naver.com/api/complexes/{complexNo}/prices?complexNo={complexNo}&tradeType={type_code}&areaNo={pyeong_no}&type=table', headers=headers)
        try :
            temp = json.loads(res.text)
        except:
            continue
        try: 
            gap_rate = temp['marketPrices'][0]['leasePerDealRate'] #매전갭 퍼센트
#             print(gap_rate, type(gap_rate))
#             if type(gap_rate)==list:
#                 gap_rate=gap_rate[0]
        except :
            gap_rate = ''
        # 가장 최근 실거래가 구하기 및 현재 호가와 비교
        
        res = requests.get(f'https://new.land.naver.com/api/complexes/{complexNo}/prices/real?complexNo={complexNo}&tradeType={type_code}&areaNo={pyeong_no}&type=table', headers=headers)
        try :
            temp = json.loads(res.text)
        except:
            continue
        # print(temp)
        if trade_type == '매매':
            try : #매매
                recent_deal_Price = temp['realPriceOnMonthList'][0]['realPriceList'][0]['dealPrice'] #최근실거래가
                recent_Trade_date = temp['realPriceOnMonthList'][0]['realPriceList'][0]['formattedTradeYearMonth'] #최근실거래 날짜
            except :    
                recent_deal_Price= 0
                recent_Trade_date= 0
        else : 
            try : #전세월세
                recent_deal_Price = temp['realPriceOnMonthList'][0]['realPriceList'][0]['leasePrice'] #최근실거래가
                recent_Trade_date = temp['realPriceOnMonthList'][0]['realPriceList'][0]['formattedTradeYearMonth'] #최근실거래 날짜
            except :    
                recent_deal_Price= 0
                recent_Trade_date= 0
        # #현재호가와 비교
        try :
            compare_price = f'{int(deal_price/recent_deal_Price*100)}%'
        except :
            compare_price = 0

        # 계산을 위한 dealprice에서 formatted로 변경
        recent_deal_Price = temp['realPriceOnMonthList'][0]['realPriceList'][0]['formattedPrice']



#         # 매물코드, 아파트이름, 매매,전세,월세, 층수, 매물 설명, 매물 태그, 가격, 공급평수, 전용평수, 
#         # 공인중개사, 중개사 이름, 중개사 번호, 매전갭, 최근실거래가, 최근거래날짜, 실거래가 대비 호가 퍼센트
#         len(df)
        i = len(apt_data_df)
        print(i)
        # apt_data_df.loc[i,"매물코드"]=code
        apt_data_df.loc[i,"시"]=city
        apt_data_df.loc[i,"군구"]=gungu
        apt_data_df.loc[i,"동"]=dong
        apt_data_df.loc[i,"아파트이름"]=apt_name
        apt_data_df.loc[i,"층수"]=f"{item['floorInfo']}층"
        apt_data_df.loc[i,"몇동"]=apt_dong_number+'동'
        apt_data_df.loc[i,"몇호"]=apt_home_number+'호'
        apt_data_df.loc[i,"방향"]=direction
        apt_data_df.loc[i,"거래타입"]=trade_type
        apt_data_df.loc[i,"가격"]=price
        apt_data_df.loc[i,"면적"]=f'{public_area}/{private_area}m²'
        apt_data_df.loc[i,"평수"]=f'{round(public_area*0.3025,1)}/{round(private_area*0.3025,1)}평'
        apt_data_df.loc[i,"평단가"]=pyeong_price
        apt_data_df.loc[i,"매전갭"]=gap_rate
        apt_data_df.loc[i,"최근실거래가"]=recent_deal_Price
        apt_data_df.loc[i,"최근거래날짜"]=recent_Trade_date
        apt_data_df.loc[i,"실거래가 대비 호가 퍼센트"]=compare_price
        apt_data_df.loc[i,"특징"]=feature
        apt_data_df.loc[i,"설명"]=tagList
        apt_data_df.loc[i,"연식"]=building_year
        apt_data_df.loc[i,"세대수"]=household_Count
        apt_data_df.loc[i,"평균관리비"]=management_cost
        apt_data_df.loc[i,"공시가격"]=posted_price 
        apt_data_df.loc[i,"중개수수료"]=broker_fee
        apt_data_df.loc[i,"취득세"]=get_tax
        apt_data_df.loc[i,"보유세"]=have_tax
        apt_data_df.loc[i,"공인중개사"]=realtor
        apt_data_df.loc[i,"중개사이름"]=realtor_name
        apt_data_df.loc[i,"중개사번호"]=realtor_phone
        apt_data_df.loc[i,"링크"]=apt_link
#         print(temp_data)
    if json_data['isMoreData']==False:
        return apt_data_df
    
def apt_detail_list(complexNo):
    # PC 네이버부동산 매물검색
    page = 1
    # 매물 페이지 로딩을 불러올 때 사용
    while True:
        data = f'?tradeType=&sameAddressGroup=true&page={page}&complexNo={complexNo}'
        response = requests.get(f'https://new.land.naver.com/api/articles/complex/{complexNo}'+data,headers=headers)
        # print(response.text)
        try :
            json_data = json.loads(response.text)
        except:
            continue   
        if json_data['isMoreData']==True:
            apt_detail_object(json_data,complexNo)
            print(1)
            page+=1
        else:
            apt_detail_df = apt_detail_object(json_data,complexNo)
            print(2)
            break
#     print(apt_detail_df)
    apt_detail_df.to_csv("test_ver.csv",encoding="utf-8-sig",index=False)
    
#     hurry_df = apt_detail_df[apt_detail_df['특징'].str.contains('급매')] ## df[조건식]
#     hurry_df.to_csv("apt_detail_df_text_Gwangju_hurry.csv",encoding="utf-8-sig",index=False)
    

# apt_detail_list(114522)    
# ab = ['8928','103385']
ab = ['8928']
for x,y in enumerate(ab) :
    apt_detail_list(y)
    if x % 300 == 0:
        time.sleep(3) #1000번 조회마다 3초 쉼
