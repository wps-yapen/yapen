import re
import requests
from bs4 import BeautifulSoup
import time
from urllib import parse
import json
from selenium import webdriver

from location.models import Pension, RoomImage, PensionImage, Room

# 가격에 string, 100,00 표현 맞지 않는 경우 0넣고 아니면 int로 바꿔서 출력
def get_int_only(string):
    a= re.findall( '(\d*,\d*)원.*',string)
    if len(a)==0:
        result= 0
    else:
        result = int(re.sub(',','',a[0]))
    return result

# location_name_list 뽑는 과정
def location_name_list_crawler():
    request = requests.get("http://www.yapen.co.kr")
    response = request.text
    soup = BeautifulSoup(response, 'lxml')

    left_menu = soup.select('div.locLayer')
    # 풀빌라, MD추천 제외 14지역중 7지역 만남김.
    selected_left_menu = left_menu[2:3]

    # 여기에 list 형태로 지역,지역고유번호/(세부지역,고유번호) 넣고싶다.
    # location_name_list =[ [지역1 ,지역1고유번호 , [ (고유번호,세부지역),(고유번호2,세부지역2)...] ],
    #                       [지역2 ,지역2고유번호 , [ (고유번호,세부지역),(고유번호2,세부지역2)...] ],..
    location_name_list = list()

    for location in selected_left_menu:
        # 지역 이름 먼저 뽑음
        location_name = location.select('div.titleStyle')[0].get_text(strip=True)
        location_name_sub_list = list()
        location_name_sub_list.append(location_name)

        li = location.select('li')

        # for문 돌면서 (고유번호 세부지역) 리스트에 담은뒤 location_list에 넣겠다.
        location_detail_list = []
        for location_detail in li:
            onclick_value = location_detail['onclick']  # regionMove('1.003021','금산/논산');

            split_right = onclick_value.split(',')[0]
            split_left = onclick_value.split(',')[1]

            sub_location_no = re.findall("'(.+)'", split_right)[0]
            sub_location_name = re.findall("'(.+)'", split_left)[0]

            flag_for_stop_upper_for = False
            if len(re.findall('.*(전체).*', sub_location_name))==1: # sub_location_name 에 전체가 들어있으면 for문 이하 건너뜀
                continue

            location_detail_tuple = (sub_location_no, sub_location_name)

            # (고유번호/세부지역) 리스트에 담음
            location_detail_list.append(location_detail_tuple)


        # 지역 고유번호부터 정규표현식으로 뽑아내서 담음.(세부지역 고유번호의 소숫점 뒤 3자리)

        location_detail_no_for_search = location_detail_list[0][0]  # '1.003021'
        location_detaol_no = re.findall(".(\d\d\d)", location_detail_no_for_search)[0]
        location_name_sub_list.append(location_detaol_no)

        # location_name_sub_list (고유번호 세부지역) 리스트를 넣음.
        location_name_sub_list.append(location_detail_list)

        # 상위 리스트에 넣음
        location_name_list.append(location_name_sub_list)

    return location_name_list


# 이제 각 페이지 location 가서 해커톤때 쓴 pension crawler 돌리고 싶다.
# 메인페이지에서 기본정보 3개만 여러개 팬션에게서 가져왔던것.
def pension_crawler(location_no, sub_location_no):
    params = {
        'location': location_no,
        'subLocation': sub_location_no,
    }

    url = "http://www.yapen.co.kr/region?" + parse.urlencode(params)

    request = requests.get(url)
    response = request.text
    soup = BeautifulSoup(response, 'lxml')

    title_list = list()
    img_file_list = list()
    price_list = list()
    ypidx_list = list()
    discount_rate_list = list()

    title_uls = soup.select('ul.dest-place-opt-fea')
    for ul in title_uls:
        li = ul.select('li')
        title_list.append(li[1].get_text())

    price_uls = soup.select('ul.dest-place-opt-cast')
    for ul in price_uls:
        li = ul.select('li')
        price_list.append(get_int_only(li[1].get_text())) # '370,000원~' 에서 숫자만 남기는 함수 호출함.

    img_file_divs = soup.select('div.imgBox')
    for div in img_file_divs:
        img_file_list.append(div.select('img')[0]['src'])

        list1 = re.split('/', div.select('img')[0]['src'])
        ypidx_list.append(int(list1[5]))

    dest_place_pics = soup.select('div.dest-place-pic')
    for dest_place_pic in dest_place_pics:
        # dest_place_pic에는 dic가 2개 or 1게 있는데  discount_rate가 있는 경우는 div가 2개이며
        # 길이가 5여서 이것으로 discount_rate있고 없고 를 비교한다.
        if (len(dest_place_pic) == 5):
            discount_rate_string = dest_place_pic.select('div')[0].get_text(strip=True)
            # %문자 정규표현식으로 빼줌.
            discount_rate_int = int(re.search('(\d*)', discount_rate_string).group())
            discount_rate_list.append(discount_rate_int)
        else:
            discount_rate_list.append(0)

    sub_locations_info_list = [title_list, price_list, img_file_list, ypidx_list, discount_rate_list]

    return sub_locations_info_list







def pension_detail_crawler(ypidx):
    pension_picture_url_num = 1  # 저장할 pension 이미지 url 1이상으로 설정해야함.
    room_picture_url_num = 1  # 저장할 room 이미지 url 1이상으로 설정해야함.
    count_sec_after_popup = 5  # seleinuim으로 창 연후에 후 몇초 sleep할지
    count_sec_after_click = 5  # seleinuim으로 각 방버튼 클릭 후 몇초 sleep할지
    count_sec_before_end_room_for_loop = 1  # Room 모델 object에 정보 저장되는 동안 sleep---->필요한지 모르겠다. 추후 테스트후 빼자.

    params = {
        'ypIdx': ypidx
    }

    url = "http://www.yapen.co.kr/details?" + parse.urlencode(params)

    request = requests.get(url)
    response = request.text
    soup = BeautifulSoup(response, 'lxml')

    ##############pension_detail 페이지 상단 기본정보들 .
    # name
    name_root = soup.select('div.wrap_1000')
    name = name_root[0].select('h3')[0].get_text()  # name

    # address
    table = soup.select('table.pensionTbl')
    trs = table[0].select('tr')
    tds = trs[0].select('td')
    address = tds[0].get_text()  # address

    # check_in, check_out
    tds2 = trs[1].select('td')
    check_in_out = tds2[0].select('span')
    check_in = check_in_out[0].get_text()  # check_in
    check_out = check_in_out[1].get_text()  # check_out

    # pickup
    tds3 = trs[2].select('td')
    pickup = tds3[0].get_text(strip=True)  # pickup

    # room_num
    td4 = trs[3].select('td')
    number_tags = td4[0].select('span')
    room_string = number_tags[0].get_text()
    room_num = int(re.search('(\d*)', room_string).group())  # room_num

    # info
    td5 = trs[4].select('td')
    infos = td5[0].select('p')
    info = ''
    for one_info in infos:
        info = info + '\n' + one_info.get_text() + '\n'  # info

    # theme
    td6 = trs[5].select('td')
    lis = td6[0].select('li')
    theme_list = []
    for li in lis:
        theme_list.append(li.get_text())
    theme = json.dumps(theme_list)  # theme

    ###############pension_detail 페이지 하단 추가정보들 .
    detailDiv = soup.select('div.detailDiv')[0]
    detailsPensionInfoTitle = detailDiv.select('div.detailsPensionInfoTitle')

    pension_detail_bellow_dict = dict()
    for one_title in detailsPensionInfoTitle:
        next_detail_div = one_title.findNext('div')
        next_detail = ''
        for p in next_detail_div.select('p'):
            next_detail = next_detail + p.get_text() + '\n'
        # p 테그없고 바로 text쓴경우에는 검출안된다.....
        pension_detail_bellow_dict[one_title.get_text(strip=True)] = next_detail

    check_in_out_detail = ""
    pickup_detail = ""
    gretting = ""
    precautions = ""

    for key, value in pension_detail_bellow_dict.items():
        if key == '입실 / 퇴실시간':
            check_in_out_detail = value  # check_in_out_detail
        elif key == '픽업가능':
            pickup_detail = value  # pickup_detail
        elif key == '펜션소개 및 인사말':
            gretting = value  # gretting
        elif key == '이용 주의사항':
            precautions = value  # precautions

    # print("@@@@PensionObject 속성들")
    # print(name)
    # print(address)
    # print(check_in)
    # print(check_out)
    # print(room_num)
    # print(info)
    # print(theme)
    #
    # print(check_in_out_detail)
    # print(pickup_detail)
    # print(gretting)
    # print(precautions)

    pension,pension_created_bool = Pension.objects.get_or_create(
            name=name,
            address=address,
            check_in=check_in,
            check_out=check_out,
            room_num=room_num,
            info=info,
            theme=theme,
            check_in_out_detail=check_in_out_detail,
            pickup_detail=pickup_detail,
            gretting=gretting,
            precautions=precautions,
        )


    ##############PensionImage 에 넣을 Pension 사진들 3장뽑겠슴.
    pensionImagesLists = soup.find(id="pensionMainImageSlider")
    image_tags = pensionImagesLists.select(" > div img")

    for index, image_tag in enumerate(image_tags):
        # html보면 2개씩 같은 이미지라서 홀수번째 만 받기로함.
        if index % 2 == 0:
            image_src = image_tag.get("src")  # image_src---------------->PensionImage객체만들때써라
            # print('@@@@팬션 이미지')
            # print(image_src)
            PensionImage.objects.get_or_create(
                pension=pension,
                pension_image=image_src,
            )
            if index == (pension_picture_url_num-1)*2:  # pension_picture_url_num 장 뽑는 시점에서 break
                break

    ############################################################
    # Room 모델 정보, RoomImage 모델 체우기 위한 이미지 셀레늄으로 뽑아보겠슴.

    # 버튼 이름 으로쓸 방 이름부터 뽑아내겠슴.
    room_name_list = []
    image_table = soup.select('div.roomImageLists')
    image_table_lis = image_table[0].select('li')
    for index, image_table_li in enumerate(image_table_lis):
        if 0 < index < room_num + 1:
            room_name_list.append(image_table_li.get_text())

    # 접속.
    chromedriver_dir = '/home/nasanmaro/Desktop/projects/yapen/test/selenium_crawling_test/chromedriver'
    driver = webdriver.Chrome(chromedriver_dir)
    driver.get(url)
    time.sleep(count_sec_after_popup)

    # 방갯수만큼의 버튼을 클릭!
    image_table = driver.find_element_by_class_name('roomImageLists')
    for room_name_text in room_name_list:
        name = room_name_text  # 객실 이름.
        room_name_button = image_table.find_elements_by_xpath('//li[contains(text(), "{0}") and @class="roomLists"]'.format(room_name_text))
        room_name_button[0].click()
        time.sleep(count_sec_after_click)  # 버튼 클릭후 충분히 멈춰줘야 사진이 로딩된다.

        # 드라이버 인스턴스로부터 현제 메뉴 연상태의 페이지 소스 받아서 source에 넣는다.
        source = driver.page_source
        # soup 객체로 만듬.
        soup = BeautifulSoup(source, 'lxml')

        pensionImagesLists = soup.find(id="pensionImagesLists")
        jssorts = pensionImagesLists.select_one('div.jssort07')
        jssort = jssorts.select('div')[0]
        image_tags = jssort.select('div.p > img')



        # room 의 속성들 뽑는중.
        layer_table_trs = soup.select('div.layerBox > table > tbody > tr')

        td_list1 = layer_table_trs[0].select('td')  # 1행
        structure = td_list1[1].get_text()  # '객실구조'
        size = td_list1[3].get_text(strip=True)  # '크기'
        num_result = re.findall('(\d*)명 / (\d*)명', td_list1[5].get_text())
        normal_num_poeple = int(num_result[0][0])  # '기준인원'
        max_num_people = int(num_result[0][1])  # '최대인원'

        td_list2 = layer_table_trs[1].select('td')  # 2행
        equipments = td_list2[1].get_text()  # 구비시설

        td_list3 = layer_table_trs[2].select('td')  # 3행
        info = td_list3[1].get_text()  # 객실 설명

        td_list4 = layer_table_trs[3].select(' > td')  # 4행

        ######기본금액뽑기.
        # price table 의 content중 좌상단 한개만 선택해서 기본금액으로 이것만 저장하려함.
        price_table_td = td_list4[1].select('table.datePriceTbl > tbody > tr > td')

        # 추가할인으로 밑줄 그어진 부분 같은 경우는 이것이 p테그안에 들어가서 따로 구분해줌.
        price_p_tag = price_table_td[1].select_one('p')
        if price_p_tag == None:
            price_p_tag = price_table_td[1]
        # 100,000원 에서 숫자들만뽑아냄.
        price = get_int_only(price_p_tag.get_text(strip=True))  # 가격

        ###### 추가금액 뽑기
        extra_charge_table_trs = td_list4[3].select('table.datePriceTbl > thead > tr')
        extra_charge_head = extra_charge_table_trs[0].get_text(strip=True)  # 추가금액 헤드
        extra_charge_adult_str = extra_charge_table_trs[1].select('td')[1].get_text(strip=True)
        extra_charge_child_str = extra_charge_table_trs[2].select('td')[1].get_text(strip=True)
        extra_charge_baby_str = extra_charge_table_trs[3].select('td')[1].get_text(strip=True)
        # 100,000원 에서 숫자들만뽑아냄.
        extra_charge_adult = get_int_only(extra_charge_adult_str)  # 어른
        extra_charge_child = get_int_only(extra_charge_child_str)  # 아동
        extra_charge_baby = get_int_only(extra_charge_baby_str)  # 유아

        room,room_created_bool = Room.objects.get_or_create(
            pension=pension,
            name=name,
            structure=structure,
            size=size,
            normal_num_poeple=normal_num_poeple,
            max_num_people=max_num_people,
            equipments=equipments,
            info=info,
            price=price,
            extra_charge_head=extra_charge_head,
            extra_charge_adult=extra_charge_adult,
            extra_charge_child=extra_charge_child,
            extra_charge_baby=extra_charge_baby,
        )

        for index, image_tag in enumerate(image_tags):
            image_src = image_tag.get("src")  # image_src--------------------->RoomImage객체만들때써라
            # print('@@룸 이미지')
            # print(image_src)
            RoomImage.objects.get_or_create(
                room=room,
                room_image=image_src,
            )

            if index == (room_picture_url_num-1):  #  room_picture_url_num 장 뽑는 시점에서 break
                break
                # 이 for 문안에서 RoomImage객체 room마다 총세번 만들면될듯

        # print("@@RoomObject 속성들")
        # print(name)
        # print(structure)
        # print(size)
        # print(normal_num_poeple)
        # print(max_num_people)
        # print(equipments)
        # print(info)
        # print(price)
        #
        # print(extra_charge_head)
        # print(extra_charge_adult)
        # print(extra_charge_child)
        # print(extra_charge_baby)

        time.sleep(count_sec_before_end_room_for_loop)

    driver.close()



###########################################################################################
##location_name_list 로부터 지역명,고유번호 받아서 각 세부지역별로 pension_crawler
## 해서 기본정보 5개씩 모으는 크롤러##

def location_crawler():
    location_info_list = list()

    location_name_list = location_name_list_crawler()
    # location_name_list =[ [지역1 ,지역1고유번호 , [ (고유번호,세부지역),(고유번호2,세부지역2)...] ],
    #                       [지역2 ,지역2고유번호 , [ (고유번호,세부지역),(고유번호2,세부지역2)...] ],..

    for location in location_name_list:
        location_name = location[0]
        location_no = location[1]
        sub_location_list = location[2]
        for sub_location in sub_location_list:
            print(sub_location)
            sub_location_no = sub_location[0]
            sub_location_name = sub_location[1]
            sub_locations_info_list = pension_crawler(location_no, sub_location_no)

            # 기존에 pension모델 1차적으로 이름,가격,이미지로  만들던것에
            # location, sub_location 속성 추가해서 이곳에서 만들면 될듯하다.
            # 일단은 리스트 형태로 정보 6개 묶어서 저장해보겠음.
            # [[location,sub_location,title,pricem,img_file,ypidx]....팬션 999까지 한 리스트에

            for i in range(len(sub_locations_info_list[0])):
                location_info_list.append([location_name,
                                           sub_location_name,
                                           sub_locations_info_list[0][i],  # name
                                           sub_locations_info_list[1][i],  # lowest_price
                                           sub_locations_info_list[2][i],  # pension_image_thumbnail
                                           sub_locations_info_list[3][i],  # ypidx
                                           sub_locations_info_list[4][i]   # discount_rate
                                           ])

    return location_info_list



# 전지역 크롤링하고 지역 > 세부지역 안의 팬션 > 방 정보 모두 크롤링후 오브젝트에 넣는 통합적인 크롤러.
def location_crawler_total():

    # 지역/세부지역/팬션이름/최저가/팬션이미지썸네일/ypidx/할인율  크롤러로 크롤링 후 결과 list로 받음.
    location_info_list = location_crawler()

    for pension_info in location_info_list:
        location = pension_info[0]
        sub_location = pension_info[1]
        name = pension_info[2]
        lowest_price = pension_info[3]
        pension_image_thumbnail = pension_info[4]
        ypidx = pension_info[5]
        discount_rate = pension_info[6]

    # PensionObjects위 속성 의 값들 5개씩만 가지고 1차적으로 만듬 ----------------->추후에 먼저 세부 메인페이지띄우고 클릭하면서 pension_detail크롤링하고 싶을경우 대비해서 나눠놈.
        pension,pension_created_bool = Pension.objects.get_or_create(
            name=name,
            pension_image_thumbnail=pension_image_thumbnail,
            lowest_price=lowest_price,
            ypidx=ypidx,
            location=location,
            sub_location=sub_location,
            discount_rate=discount_rate,
        )
        # location_info_list 에있던 ypidx값 가지고 pension_detail_crawler돌려서 나머지 속성들 체움,
        pension_detail_crawler(ypidx)
