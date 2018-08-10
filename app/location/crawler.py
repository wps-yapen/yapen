import re
import requests
from bs4 import BeautifulSoup
import time
from urllib import parse
from selenium import webdriver

from location.models import Pension, RoomImage, PensionImage, Room, Location, SubLocation


# 가격에 string, 100,00 표현 맞지 않는 경우 0넣고 아니면 int로 바꿔서 출력
def get_int_only(string):
    a= re.findall( '(\d*,\d*)원.*',string)
    if len(a)==0:
        result= 0
    else:
        result = int(re.sub(',','',a[0]))
    return result

def room_crawler(soup,room_num,url,pension,count_sec_after_popup,count_sec_after_click,room_picture_url_num):

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

    chromedriver_dir = '/Users/jeonsangmin/project/chromedriver'

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

        # 빈값들을 일단 넣어줘서 아래서 Room 모델 생성시 애러뜨지 않게하려함.
        structure = ""
        size = ""
        normal_num_poeple = 0
        max_num_people = 0
        equipments = ""
        info = ""
        price = 0
        extra_charge_head = 0
        extra_charge_adult = 0
        extra_charge_child = 0
        # room 의 속성들 뽑는중.
        layer_table_trs = soup.select('div.layerBox > table > tbody > tr')

        # 종종 여기서 애러떠서 아예 빈값이면 안들어가게했음.
        if layer_table_trs:
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

    driver.close()




def pension_detail_crawler(sub_location,lowest_price,pension_image_thumbnail,ypidx,discount_rate):
    max_room_num = 1
    pension_picture_url_num = 2  # 저장할 pension 이미지 url 1이상으로 설정해야함.
    room_picture_url_num = 2  # 저장할 room 이미지 url 1이상으로 설정해야함.
    count_sec_after_popup = 3  # seleinuim으로 창 연후에 후 몇초 sleep할지
    count_sec_after_click = 2  # seleinuim으로 각 방버튼 클릭 후 몇초 sleep할지

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
    result = re.findall('지번 : (.*) ',address)
    lat=0
    lng=0
    while(lat==0):     # 한번 요청 보내도 값 안줄때가 있어서 적절한 값 들어갈때까지 요청 보낸다.
        URL = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=ko&address={}' \
            .format(result)
        response = requests.get(URL)
        data = response.json()
        if data.get('results'):  # 만약 reaults에 뭔가 있다면 if문들어가서 lat, lng에 값 할당
            lat = data['results'][0]['geometry']['location']['lat']                                 # 위도 lat
            lng = data['results'][0]['geometry']['location']['lng']                                 # 경도 lng

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

    # room_num 최대 max_room_num으로 제한걸어줌.
    if room_num > max_room_num:
        room_num = max_room_num

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
        # '테마1,테마2,테마3' 이런 형태로 저장하고 싶다.
    theme = (',').join(theme_list)  # theme

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
    # location_total_crawler안에서 pension_detail_crawler사용시 전달받아야되는 인자들.-->location_crawler() 로 얻어짐.
            pension_image_thumbnail=pension_image_thumbnail,
            lowest_price=lowest_price,
            ypidx=ypidx,
            sub_location=sub_location,
            discount_rate=discount_rate,

    #pension_detail_crawler 안에서 크롤링한 속성들.
            name=name,
            address=address,
            check_in=check_in,
            check_out=check_out,
            pickup=pickup,
            room_num=room_num,
            info=info,
            theme=theme,
            lat=lat,
            lng=lng,
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

    # 각 팬션에 속한 room정보 크롤링하며 Room객체 생성하는 크롤러
    room_crawler(soup=soup,
                 room_num=room_num,
                 url=url,
                 pension=pension,
                 count_sec_after_click=count_sec_after_click,
                 count_sec_after_popup=count_sec_after_popup,
                 room_picture_url_num=room_picture_url_num)






#  세부지역 페이지에서 각 팬션에 대한 기본정보 5개만 여러개 팬션에게서 가져왔던것.
def sub_location_crawler(location_no, sub_location_no):
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



# location_name_list 뽑는 과정
def location_crawler():
    request = requests.get("http://www.yapen.co.kr")
    response = request.text
    soup = BeautifulSoup(response, 'lxml')

    left_menu = soup.select('div.locLayer')
    # 풀빌라, MD추천 제외 14지역중 7지역 만남김.
    selected_left_menu = left_menu[2:3]

    for selected_location in selected_left_menu:
        # 지역 이름 먼저 뽑음
        location_name = selected_location.select('div.titleStyle')[0].get_text(strip=True)

        # Location 객체 생성
        location,__=Location.objects.get_or_create(name=location_name)                                  # Location(지역)객체 생성

        li = selected_location.select('li')
        for location_detail in li:
            onclick_value = location_detail['onclick']  # regionMove('1.003021','금산/논산');
            split_right = onclick_value.split(',')[0]
            split_left = onclick_value.split(',')[1]
            sub_location_no = re.findall("'(.+)'", split_right)[0]
            sub_location_name = re.findall("'(.+)'", split_left)[0]
            if len(re.findall('.*(전체).*', sub_location_name))==1: # sub_location_name 에 전체가 들어있으면 for문 이하 건너뜀
                continue

            # SubLocation 객체 생성
            sub_location,__= SubLocation.objects.get_or_create(location=location,                       # SubLocation(세부지역) 객체 생성
                                                               name=sub_location_name,
                                                               sub_location_no=sub_location_no)

            # 지역 고유번호부터 정규표현식으로 뽑아내서 담음.(세부지역 고유번호의 소숫점 뒤 3자리) # '1.003021'
            location_no = re.findall(".(\d\d\d)", sub_location_no)[0] # 지역번호

            # sub_location(세부지역) 페이지로부터 기본정보 5개 크롤링먼저 해옴.(팬션 디테일 페이지 접속위한 ypidx얻기위해 필요한 과정)
            sub_locations_info_list = sub_location_crawler(location_no, sub_location_no)
            for i in range(len(sub_locations_info_list[0])):

                # 각각의 팬션을 크롤링 하며 Pension객체 생성, 방들 크롤링한후 Room 객체 생성하는 크롤러 호출
                pension_detail_crawler(
                   sub_location=sub_location,
                   lowest_price=sub_locations_info_list[1][i],  # lowest_price,
                   pension_image_thumbnail=sub_locations_info_list[2][i],  # pension_image_thumbnail
                   ypidx=sub_locations_info_list[3][i],  # ypidx,
                   discount_rate=sub_locations_info_list[4][i]   # discount_rate,
               )
        for location in Location.objects.all():
            location.pensions_length = len(Pension.objects.filter(location=location))

    for location in Location.objects.all():
        sub_location = SubLocation.objects.filter(location=location)
        location.pensions_length = len(Pension.objects.filter(sub_location__in=sub_location))
        location.save()

    for sublocation in SubLocation.objects.all():
        sublocation.pensions_length = len(Pension.objects.filter(sub_location=sublocation))
        sublocation.save()

