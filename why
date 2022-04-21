import requests
import json


headers = {
    'Accept': '*/*',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Referer': 'https://new.land.naver.com/complexes/4401?ms=35.1599,126.8018956,16&a=APT:ABYG:JGC&e=RETAIL',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.57 Whale/3.14.133.23 Safari/537.36',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE2NTA1MzQ4NTIsImV4cCI6MTY1MDU0NTY1Mn0.SS2d_1aZa0MIZUgtyKO2kR0GiYb5L1Y7TsgeiErAVXo',
}
def recent_deal_price(complexNo1,type_code,pyeong_no):
    # 해당 평수 가장 최근 실거래가 deal_price와 비교
    res = requests.get(f'https://new.land.naver.com/api/complexes/{complexNo1}/prices/real?complexNo={complexNo1}&tradeType={type_code}&areaNo={pyeong_no}&type=table', headers=headers)
    temp = json.loads(res.text)
    # print(temp)
    print(temp['realPriceOnMonthList'][0]['realPriceList'][0]['dealPrice'])
    # m = temp['marketPrices'][0]['leasePerDealRate']
    # print(temp_data['dealPrice'])
    # print(temp_data['formattedTradeYearMonth'])

# recent_deal_price('4401','A1','1')

def apt_detail_object(json_data,complexNo):
    # 매물 내에서 자세한 정보를 긁어오는 함수
    for i, item in enumerate(json_data['articleList']):
        code = item['articleNo'] #매물코드
        apt_name = item['articleName'] #아파트이름
        trade_type = item['tradeTypeName'] #매매,전세,월세
        floor = item['floorInfo'] #층수
        try :
            feature = item['articleFeatureDesc'] #매물 설명
        except KeyError:
            feature = ''
        tagList = item['tagList'] #매물 태그
        price = item['dealOrWarrantPrc'] #가격
        realtor = item['realtorName'] #공인중개사
        public_area = item['area1'] #공급평수
        private_area = item['area2'] #전용평수
        
        # 중개사 전화번호얻기  a는 매물코드
        res = requests.get(f'https://new.land.naver.com/api/articles/{code}', headers=headers)
        # response = requests.get('https://new.land.naver.com/api/articles/2212513920', headers=headers, params=params, cookies=cookies)
        temp = json.loads(res.text)

        type_code = temp['articleAddition']['tradeTypeCode'] #A1,B1,B2 거래타입 파라미터로 사용
        deal_price = temp['articlePrice']['dealPrice'] #물건 호가 ex)15000

        try: 
            realtor_name = temp['articleRealtor']['representativeName'] #중개사 이름
            realtor_phone = temp['articleRealtor']['cellPhoneNo'] #중개사 번호
        except KeyError :    
            k=''
            l=''
        pyeong_no=temp['landPrice']['ptpNo'] #평수 순번, 실거래가, 매전갭 추출 시 필요

        # 매전 갭 구하기
        res = requests.get(f'https://new.land.naver.com/api/complexes/{complexNo}/prices?complexNo={complexNo}&tradeType={type_code}&areaNo={pyeong_no}&type=table', headers=headers)
        temp = json.loads(res.text)
        gap_rate = temp['marketPrices'][0]['leasePerDealRate'] #매전갭 퍼센트
        
        # 가장 최근 실거래가 구하기 및 현재 호가와 비교
        res = requests.get(f'https://new.land.naver.com/api/complexes/{complexNo}/prices/real?complexNo={complexNo}&tradeType={type_code}&areaNo={pyeong_no}&type=table', headers=headers)
        temp = json.loads(res.text)
        # print(temp)
        try :
            recent_deal_Price = temp['realPriceOnMonthList'][0]['realPriceList'][0]['dealPrice'] #최근실거래가
            recent_Trade_date = temp['realPriceOnMonthList'][0]['realPriceList'][0]['formattedTradeYearMonth'] #최근실거래 날짜
        except KeyError :    
            recent_deal_Price=1
            recent_Trade_date=1    
        # #현재호가와 비교
        compare_price = f'{int(deal_price/recent_deal_Price*100)}%'
#         A1 = 0 #매매 전세 월세 순
#         B1 = 0
#         B2 = 0 
#         if trade_type =='매매':
#             A1+=1
#         elif trade_type =='전세':
#             B1+=1
#         elif trade_type =='월세':
#             B2+=1
    # print(A1,B1,B2)    
#         print(code,apt_name,trade_type,floor,feature,tagList,price,realtor,public_area,private_area,realtor_name,realtor_phone, gap_rate, recent_deal_Price,recent_Trade_date,compare_price)

#         # 매물코드, 아파트이름, 매매,전세,월세, 층수, 매물 설명, 매물 태그, 가격, 공급평수, 전용평수, 
#         # 공인중개사, 중개사 이름, 중개사 번호, 매전갭, 최근실거래가, 최근거래날짜, 실거래가 대비 호가 퍼센트
        temp_data.loc[i,"매물코드"]=code
        temp_data.loc[i,"아파트이름"]=apt_name
        temp_data.loc[i,"거래타입"]=trade_type
        temp_data.loc[i,"층수"]=floor.replace('-','/')
        temp_data.loc[i,"특징"]=feature
        temp_data.loc[i,"설명"]=tagList
        temp_data.loc[i,"가격"]=price
        temp_data.loc[i,"평수"]=f'{public_area}/{private_area}'
        temp_data.loc[i,"공인중개사"]=realtor
        temp_data.loc[i,"중개사이름"]=realtor_name
        temp_data.loc[i,"중개사번호"]=realtor_phone
        temp_data.loc[i,"매전갭"]=gap_rate
        temp_data.loc[i,"최근실거래가"]=recent_deal_Price
        temp_data.loc[i,"최근거래날짜"]=recent_Trade_date
        temp_data.loc[i,"실거래가 대비 호가 퍼센트"]=compare_price
#     print(temp_data)
#     return temp_data
#     wr.writerow(f'매매 : {A1} , 전세 : {B1}, 월세 : {B2}')
    



def apt_detail_list(complexNo):
    # PC 네이버부동산 매물검색
    page = 1
    # 매물 페이지 로딩을 불러올 때 사용
    apt_detail_df = [0]
    while True:
        data = f'?tradeType=&sameAddressGroup=false&page={page}&complexNo={complexNo}'
        response = requests.get(f'https://new.land.naver.com/api/articles/complex/{complexNo}'+data,headers=headers)
        # print(response.text)
        json_data = json.loads(response.text)
        # 페이지가 더 남아있으면 page+1하여 돌리고, isMoreData가 False면 마지막페이지 출력 후 종료
#         page=1 #페이지 수 먼저 체크 후 돌릴꺼다.
#         if json_data['isMoreData']==True:
#             page+=1
#             apt_detail_df.append(0)
#         else :
#             page+=1
#             apt_detail_df.append(0)
# dong_apt_list[k]=pd.concat(apt_list_data)
           
        if json_data['isMoreData']==True:
            apt_detail_df.append(0)
            apt_detail_df[page-1] = apt_detail_object(json_data,complexNo)
            print(1)
            page+=1
        else:
#             apt_detail_df.append(0)
            apt_detail_df[page-1] = apt_detail_object(json_data,complexNo)
#             print(apt_detail_object(json_data,complexNo))
            print(2)
            break
    apt_detail_df
#     temp_data=pd.concat(apt_detail_df)
#     temp_data.to_csv("매물정보_추출_테스트_ver2.csv",encoding="CP949",index=False)


apt_detail_list(4401)
