## 야놀자펜션
 전국 펜션 실시간 빈방 조회 및 최저가 예약, 대실시간 연장혜택! 지금 야놀자 펜션 혜택을 이용하세요.

## 프로젝트 소개
Fastcapmpus 웹 프로그래밍스쿨 과정에서 배운 기술과 Front-end, IOS협업을 통해 야놀자펜션 COPY

## 프로젝트 URL

<a href="www.pmb.kr">https://pmb.kr (Front-end)</a>

<a href="www.pmb.kr">https://api.pmb.kr (Back-end)</a>


## 프로젝트 구성

* 프로젝트 팀: 백엔드3명, 프론트엔드3명, IOS 앱개발 2명
* 기간 : 2018.7.30 ~ 2018.8.24
* 역할 : 서버세팅 및 배포, API 작성
* 사용 언어 및 프로그램
	* 공통: Git, Postman, Slack
	* 백엔드: python, django, PostgreSQL, Django-Rest-Framework, AWS EC2, S3, RDS, Elastic Beanstalk, Docker
* 주요 내용
	* 백엔드 개발 환경분리(local / production)
	* 지역별 펜션 리스트 보여주기
	* 회원가입시 e-mail인증
	* Keyword-search, Button-search
	* `.secrets` 폴더내의 파일로 비밀 키를 관리합니다.
	* DB로 PostgreSQL을 사용하며, `local`환경에서는 `localhost`의 DB, production환경에서는 `AWS RDS`의 DB를 사용합니다.
	
## 프로젝트 API
<a href="https://wps-yapen.gitbook.io/project/"> Yapen API Gitbook</a>
	
## Requirements

- Python (3.6)
- Django (2.x)

## AWS 환경

* S3 Bucket, 해당 Bucket을 사용할 수 있는 IAM User의 AWS  AccessKey, SecretAccessKey
* RDS Database(보안그룹 허용 필요), 해당 DB를 사용할 수 있는 RDS의 User, Password

### Secrets

#### `.sercets/base.json`

```json
{
  "SECRET_KEY": "<Django secret key>"
}
```

## Installation
```
pipenv install
```

## Running

```
# Move project`s directory
- pipenv install
- pipenv shell
- cd app
- export DjANGO_SETTINGS_MODULE=config.settings.local
- `./manage.py runserver`
```

## DockerHub

```
docker build -t yapen-docker:base -f Dockerfile.base
docker tag yapen-docker:base <자신의 사용자명>/<저장소명>:base
docker push <자신의 사용자명>/<저장소명>:base
```

