import requests
import db_context
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def naver_site_list(name):
    hrd = {'User-Agent':'Mozilla/5.0', 'referer':'http://naver.com'}
    param = { 'where': 'post' }

    # 영화 제목 검색
    basic_url = "https://movie.naver.com/movie/search/result.nhn?section=movie&query="
    plus_url = str(name.encode('cp949'))[2:-1].replace("\\x", "%").replace(" ", "+").upper().strip()
    url = basic_url + plus_url
    # print(url)

    try:
        response = requests.get(url, params=param, headers=hrd)
        soup_temp = BeautifulSoup(response.text, 'html.parser')
        for link in soup_temp.find("p", class_="result_thumb").find_all('a'):
            area_temp = "https://movie.naver.com" + link.attrs['href'].strip()
        return area_temp.replace("basic", "point"), area_temp.replace("basic", "pointWriteFormList") + "&type=after&onlyActualPointYn=Y"
    except:
        return -1, -1

# 기본적인 평점 정보 가져오기
def naver_crawling_list1(url):
    hrd = {'User-Agent':'Mozilla/5.0', 'referer':'http://naver.com'}
    param = { 'where': 'post' }

    try:
        response = requests.get(url, params=param, headers=hrd)
        soup_temp = BeautifulSoup(response.text, 'html.parser')
        result1 = soup_temp.find('div', {'class':'main_score'}).findAll('em')[3].getText().strip() + soup_temp.find('div', {'class':'main_score'}).findAll('em')[4].getText().strip() + soup_temp.find('div', {'class':'main_score'}).findAll('em')[5].getText().strip() + soup_temp.find('div', {'class':'main_score'}).findAll('em')[6].getText().strip()
        result2 = soup_temp.find('div', {'class':'main_score'}).findAll('em')[8].getText().strip() + soup_temp.find('div', {'class':'main_score'}).findAll('em')[9].getText().strip() + soup_temp.find('div', {'class':'main_score'}).findAll('em')[10].getText().strip() + soup_temp.find('div', {'class':'main_score'}).findAll('em')[11].getText().strip()
        result3 = soup_temp.find('div', {'class':'main_score'}).findAll('em')[15].getText().strip() + soup_temp.find('div', {'class':'main_score'}).findAll('em')[16].getText().strip() + soup_temp.find('div', {'class':'main_score'}).findAll('em')[17].getText().strip() + soup_temp.find('div', {'class':'main_score'}).findAll('em')[18].getText().strip()
        print(result1)
        print(result2)
        print(result3)
        return result1, result2, result3
    except:
        return -1, -1, -1

# 스포일러 정보 가져오기
def naver_crawling_list2(url):
    hrd = {'User-Agent':'Mozilla/5.0', 'referer':'http://naver.com'}
    param = { 'where': 'post' }
    review_text_array = []

    try:
        response = requests.get(url+'&onlySpoilerPointYn=Y', params=param, headers=hrd)
        soup_temp = BeautifulSoup(response.text, 'html.parser')
        result = soup_temp.find('div', {'class':'score_total'}).find('strong').findChildren('em')[0].getText().strip()
        total_count = int(result.replace(',', ''))
        # print("result : " + result)

        if total_count > 100:
            total_count = 99

        # for i in range(1, 5):
        for i in range(1, int(total_count / 10) + 2):
            temp_url = url + '&onlySpoilerPointYn=Y&page=' + str(i)
            # print(i, 1, int(total_count / 10) + 1, temp_url)
            response = requests.get(temp_url, params=param, headers=hrd)
            soup_temp = BeautifulSoup(response.text, 'html.parser')

            score_result = soup_temp.find('div', {'class': 'score_result'})
            lis = score_result.findAll('li')

            count = 0
            for li in lis:
                count += 1
                review_text = li.find('p').find_all('span')[1].getText().strip()

                review_text_array.append(review_text)
                # print("=============================================================")
                # print("review_text : " + review_text)

        return review_text_array
    except:
        return -1

# 리뷰 정보 가져오기
def naver_crawling_list3(conn, url, review_text_array_temp):
    hrd = {'User-Agent':'Mozilla/5.0', 'referer':'http://naver.com'}
    param = { 'where': 'post' }
    count_array = []
    review_text_array = []
    score_array = []
    like_array = []
    dislike_array = []
    nicname_array = []
    created_at_array = []

    try:
        response = requests.get(url, params=param, headers=hrd)
        soup_temp = BeautifulSoup(response.text, 'html.parser')
        result = soup_temp.find('div', {'class':'score_total'}).find('strong').findChildren('em')[0].getText().strip()
        total_count = int(result.replace(',', ''))
        print("result : " + result)

        if total_count > 100:
            total_count = 99

        # for i in range(1, 5):
        for i in range(1, int(total_count / 10) + 2):
            temp_url = url + '&page=' + str(i)
            print(i, 1, int(total_count / 10) + 1, temp_url)
            response = requests.get(temp_url, params=param, headers=hrd)
            soup_temp = BeautifulSoup(response.text, 'html.parser')

            score_result = soup_temp.find('div', {'class': 'score_result'})
            lis = score_result.findAll('li')

            spolier_count = 0
            count = 0
            for li in lis:
                count += 1
                review_text = li.find('p').find_all('span')[1].getText().strip()
                if review_text == "스포일러가 포함된 감상평입니다. 감상평 보기":
                    review_text = review_text_array_temp[spolier_count]
                    spolier_count += 1

                score = li.find('em').getText().strip()
                like = li.find('div', {'class': 'btn_area'}).findAll('strong')[0].getText().strip()
                dislike = li.find('div', {'class': 'btn_area'}).findAll('strong')[1].getText().strip()
                nickname = li.find('div', {'class': 'score_reple'}).findAll('span')[-1].getText().strip()
                created_at = li.find('dt').findAll('em')[-1].getText().strip()

                count_array.append(str((i-1)*10 + count))
                review_text_array.append(review_text)
                score_array.append(score)
                like_array.append(like)
                dislike_array.append(dislike)
                nicname_array.append(nickname)
                created_at_array.append(created_at)
                
                print("=============================================================")
                print("번호 : " + str((i-1)*10 + count))
                print("리뷰 : " + review_text)
                print("점수 : " + score)
                print("좋아요 : " + like)
                print("싫어요 : " + dislike)
                print("닉네임 : " + nickname)
                print("날짜 : " + created_at)
                print("")

                # 번호 : ID / 점수 : TITLE / 좋아요 : LINK / 싫어요 : IMAGELINK / 리뷰 : CONTEXT1 / 날짜 : DATE / 닉네임 : NICNAME / 
                db_context.insert(conn, str((i-1)*10 + count), str(score), str(like), 
            str(dislike), str(review_text), str(created_at), str(nickname), "미판정", "미판정", "미판정")

        return review_text_array, score_array, like_array, dislike_array, nicname_array, created_at_array
    except:
        return -1, -1, -1, -1, -1, -1
