# auth-with-flask-and-jwt

---
# What is auth-with-flask-and-jwt?
* auth project with jwt
* domain driven design : 도메인 간 메시지 전달을 구현하지 않아 침범이 있음
* version 
    * python : 3.7.8
    * flask : 1.1.2
# Usage
## [poetry](https://python-poetry.org/)
* install pipenv : `pip install poetry`
* create python virtual environment : `poetry init`
* install packages in pyproject.toml : `poetry install`
* install package : `poetry add {package name}`
* install packages with dev in pipfile : `poetry add --dev`
* uninstall package : `pipenv remove {package name}`
## [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/)
* create empty migration file : `flask db revision -m "create {name} table"`
* create auto-generate migrate file : `flask db migrate -m "create {name} table"`
    * `model에 설정된대로 revision 파일을 만들어주기 때문에 편리하다.`
    * `migrations/env.py의 target_metadata에 db.Model.metadata를 넣어줘야 한다.`
* db upgrade : `flask db upgrade`
* db downgrade : `flask db downgrade`
* target current db : `flask db stamp {revision}`
    * 사용해야할 상황
        1. `진행된 마이그레이션과 현재 alembic이 가리키고 있는 마이그레이션이 다른 경우 동기화`
        2. `아직 진행되지 않은, 혹은 downgrade로 db 롤백 후 마이그레이션 파일 삭제하기 전에 가리키려는 revision을 지정하고 파일 삭제`
    * `revision에는 head나 revision이 들어가면 된다.`
## [pydantic](https://pydantic-docs.helpmanual.io/)
* python schema validator
* validate request parameter, dto, response schema
# Requirements
1. 사용자는 회원가입을 한다
2. 회원은 로그인을 한다
3. 이메일 인증 시 이메일을 직접 보낼 필요는 없으며, log 상에서 인증키를 확인할 수 있어야 한다
4. 개인정보 수정 시 로그인한 유저 본인만 수정할 수 있어야 한다
5. 유저는 email, password, nickname 이 반드시 있어야 한다
6. 유저 비밀번호는 암호화해서 저장한다
7. 유저 관리 라이브러리를 사용할 수 없다
# Design
| requirement                                                                                | design                                                                                                                                                                                                                                                                         | API                                  | request              | response                         |
|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------| ----------------------- | ------------------------------------------- | 
| 사용자는 회원가입을 한다                                                                   | 사용자가 입력한 password, nickname을 가지고 회원가입한다                                                                                                                                                                                                                       | `POST`   `api/user/v1/signup`            | `{ "nickname" : str, "password" :str }` | `{ "data" : bool, "meta" : null }` |
| 회원은 로그인을 한다                                                                       | users 테이블에서 nickname, password가 일치하는 row가 존재하는지 확인한다 1. 다르면 unauthorized error 2. 같으면 성공 응답에 user_id를 담은 JWT를 반환한다                                                                                                                       | `POST`   `api/user/v1/signin`            | `{ "nickname" : str, "password" : str }` | `{ "data": str, "meta": null }`
| 이메일 인증 시 이메일을 직접 보낼 필요는 없으며, log 상에서 인증키를 확인할 수 있어야 한다 | 사용자가 입력한 email을 auths 테이블에 저장한다 생성된 인증 코드를 email로 보낸다 → log로 찍고 생략.                                                                                                                                                                                                     | `POST`   `api/auth/v1`    | `{"user_id" : int, "identification" : "test@test.com", "type_" : "email"}` | `{ "data" : bool, "meta" : null }` |
| 회원인 인증코드로 인증한다                                                     | 사용자의 이메일로 전송된 인증 코드를 auths 테이블의 verify_code와 비교한다. 1. 값이 같으면 is_verified true, 인증 성공 응답 2. 값이 다르면 is_verified false, 인증 실패 응답                                                                                                                          |`PUT` `api/auth/v1` | `{"user_id" : int, "identification": "test@test.com", "verify_code": int}` | `{ "data" : bool, "meta" : null }` |
| 개인정보 수정 시 로그인한 유저 본인만 수정할 수 있어야 한다                                | JWT 토큰에 있는 user_id를 가지고 users 테이블에 유저가 있는지 확인한다. 인증 데코레이터 사용. 1. 있으면 로직 진행. 2. 없으면 실패 응답. request body에 있는 값들을 users table에 반영한다.                                                                                       | `PUT`  `api/user/v1/user/ <int:user_id>` | `{"new_nickname" : str, "current_password" : str, "new_password" : str, "new_password_check" : str}` | `{ "data" : bool, "meta" : null }` |
| 유저는 email, password, nickname 이 반드시 있어야 한다                                     | 회원가입 시 request body에 email, password, nickname 속성이 없으면 에러 응답                                                                                                                                                                                                   |                                      |
| 유저 비밀번호는 암호화해서 저장한다                                                        | 회원가입 시 password는 복호화 불가능한 방식으로 암호화해서 저장한다                                                                                                                                                                                                            |                                      |
| 유저 관리 라이브러리를 사용할 수 없다                                                      |                                                                                                                                                                                                                                                                                |                                      |
# 사용자 관점 email 인증 흐름
1. 사용자는 회원 가입을 한다.
2. 사용자는 이메일을 입력한다.
3. 사용자는 `2.`에서 입력한 이메일에서 인증 코드를 확인하고 인증 코드를 전송한다.
# 서버 관점 email 인증 흐름
1. nickname, password를 users 테이블에 저장한다.
2. email을 auths 테이블에 저장하고 인증 코드를 이메일로 전송한다.
3. 입력된 인증 코드를 확인하고 인증 여부를 auths 테이블에 기록한다.
# table
### users
|column|type|constraint|default|description|
|----|---|---|---|---|
| id | bigint | PK | NOT NULL |
| password | bytea |  | NOT NULL | binary 값 저장
| nickname | string(50) |  | NOT NULL |
| created_at | datetime | | NOT NULL |
| updated_at | datetime | | NOT NULL |
### auths
|column|type|constraint|default|description|
|----|---|---|---|---|
| id | bigint | PK | NOT NULL |
| user_id | bigint | FK | NOT NULL |
| identification | string(50) |  | NOT NULL | 인증 식별자
| type | string(20) |  | NOT NULL | 인증 타입
| verify_code | string(50) |  | NOT NULL | 인증 코드 
| is_verified | bool | false | | 인증 여부 
| created_at | datetime | | NOT NULL | 인증 타입 `ex) email`
| updated_at | datetime | | NOT NULL |
| expired_at | datetime | | NOT NULL | 인증 만료 기한
# 코드 실행 방법 - pycharm 기준
## package 설치
1. pycharm `Preferences` -> `Project` -> `Python Interpreter` -> `python 3.7 가상 환경 생성`
2. terminal에서 `auth-with-flask-and-jwt` 프로젝트 접근 (터미널 왼쪽에 가상환경 표시 안되면 터미널 종료 후 재실행)
3. terminal에서 `pip install poetry` 입력
4. `poetry install` 입력
## test code 실행
0. 테스트 코드는 sqlite3 메모리 기반이므로 바로 실행 가능
1. terminal에서 `pytest` 입력
2. 병렬 실행 `pytest -n5`
## table migration
1. DB는 `postgresql`을 사용.
2. `postgresql`, `pgadmin4` 설치
3. `pgadmin4` 접속 후 계정 : `postgres`, pw : `password` 생성, DB `elysia` 생성
    1. 만약 `postgres` 계정이 있다면 그 계정으로 `elysia` DB 생성 후 프로젝트 `config` 파일에서 DB 연결 값 수정 `"postgresql+psycopg2://postgres:password@localhost:5432/elysia"` -> `"postgresql+psycopg2://postgres:{비밀번호}@localhost:5432/elysia"`
4. terminal에서 `flask db upgrade` 입력
5. `users`, `auths` 테이블 생성 확인
## pycharm DB connection
![img.png](img.png)
## pycharm server connection
![img_1.png](img_1.png)
## 서버 실행
1. terminal에서 `flask run` 입력 또는 `pycharm server connection` 참고해서 실행