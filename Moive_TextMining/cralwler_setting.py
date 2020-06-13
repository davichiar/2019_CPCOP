import cralwler_naver
import Grade_review
import Visual_review
import db_context
import db_percentiy
import db_rating

def init(conn, text):
    # 네이버 URL 가져오기
    naver_url1, naver_url2 = cralwler_naver.naver_site_list(text)
    print(naver_url1, naver_url2)

    # 네이버 크롤링 리스트
    x, y, z = cralwler_naver.naver_crawling_list1(naver_url1)
    if x == -1 or y == -1 or z == -1:
        return
    else:
        db_rating.insert(conn, 1, x, y, z)
    review_text_array_temp = cralwler_naver.naver_crawling_list2(naver_url2)
    review_text_array, score_array, like_array, dislike_array, nicname_array, created_at_array = cralwler_naver.naver_crawling_list3(conn, naver_url2, review_text_array_temp)

    add_array = []
    check_array = []
    count_array = []

    file=open('context.txt','w')
    for x in range(len(review_text_array)):
        print("================================================================")
        print("번호 : " + str(x+1))
        print("리뷰 : " + review_text_array[x])
        print("점수 : " + score_array[x])
        print("좋아요 : " + like_array[x])
        print("싫어요 : " + dislike_array[x])
        print("닉네임 : " + nicname_array[x])
        print("날짜 : " + created_at_array[x])

        if len(review_text_array[x]) <= 1:
            add_array.append('글자수 광고')
        else:
            add_array.append('청정')
            print("광고 여부 : " + add_array[x])

        db_context.update_addtext(conn, str(x+1), add_array[x])
        if(add_array[x] == '청정'):
            try:
                file.write(review_text_array[x] + '\n')
                check = Grade_review.Grade(review_text_array[x])
                check_array.append(check)
            except:
                check_array.append('중립')
        else:
            check_array.append('중립')

        db_context.update_activetext(conn, str(x+1), check_array[x])
        print("긍/부정 : " + check_array[x])
        print("")

    try:
        print("광고 퍼센트 : " + str( ( 1 - float ( add_array.count('청정') / len(add_array) ) ) * 100 ) )
        print("긍/부정 퍼센트 : " + str( float ( check_array.count('긍정') / ( len(check_array) - check_array.count('중립') ) ) * 100 ) )
    except:
        pass
    print("")

    try:
        addper = ( ( 1 - float ( add_array.count('청정') / len(add_array) ) )  * 100 )
        actper = float ( check_array.count('긍정') / ( len(check_array) - check_array.count('중립') ) * 100 )

        print("광고 퍼센트 : " + str(addper))
        print("긍/부정 퍼센트 : " + str(actper))
        
        addnum = len(add_array) - add_array.count('청정')
        actnum = check_array.count('긍정')
        db_percentiy.insert(conn, str(1), str(x+1), str(addnum), str(actnum), str(round(addper, 1)), str(round(actper, 1)))
    except:
        pass
    print("")
    file.close()

    Visual_review.visual_main()
    file=open('count.txt','r')
    for x in range(20):
        count_array.append( file.readline().split('\n')[0] )
    file.close()
    temp_array = []
    for x in count_array:
        if text.count(x.split()[0]) == 0 and len(x.split()[0]) > 1:
            if x.split()[0] != "영화" and x.split()[0] != "스토리" and x.split()[0] != "시리즈":
                temp_array.append(x)

    print(temp_array)
    db_context.update_set(conn, str(temp_array))
    print("")
