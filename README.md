# auth-with-flask-and-jwt

---
# What is auth-with-flask-and-jwt?
* auth project with jwt
* domain driven design : 도메인 간 침범이 있음, TODO : 도메인 간 메시지 전달
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
| requirement                                                                                | design                                                                                                                                                                                                                                                                         | API                                  |
|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|
| 사용자는 회원가입을 한다                                                                   | 사용자가 입력한 password, nickname을 가지고 회원가입한다                                                                                                                                                                                                                       | `POST`   `api/user/v1/signup`            |
| 회원은 로그인을 한다                                                                       | users 테이블에서 nickname, password가 일치하는 row가 존재하는지 확인한다 1. 다르면 unauthorized error 2. 같으면 성공 응답에 user_id를 담은 JWT를 반환한다                                                                                                                       | `POST`   `api/user/v1/signin`            |
| 이메일 인증 시 이메일을 직접 보낼 필요는 없으며, log 상에서 인증키를 확인할 수 있어야 한다 | 사용자가 입력한 email을 auths 테이블에 저장한다 생성된 인증 코드를 email로 보낸다 → log로 찍고 생략.                                                                                                                                                                                                     | `POST`   `api/auth/v1`    |
| 회원인 인증코드로 인증한다                                                     | 사용자의 이메일로 전송된 인증 코드를 auths 테이블의 verify_code와 비교한다. 1. 값이 같으면 is_verified true, 인증 성공 응답 2. 값이 다르면 is_verified false, 인증 실패 응답                                                                                                                          |`PUT` `api/auth/v1`
| 개인정보 수정 시 로그인한 유저 본인만 수정할 수 있어야 한다                                | JWT 토큰에 있는 user_id를 가지고 users 테이블에 유저가 있는지 확인한다. 인증 데코레이터 사용. 1. 있으면 로직 진행. 2. 없으면 실패 응답. request body에 있는 값들을 users table에 반영한다.                                                                                       | `PUT`  `api/user/v1/user/ <int:user_id>` |
| 유저는 email, password, nickname 이 반드시 있어야 한다                                     | 회원가입 시 request body에 email, password, nickname 속성이 없으면 에러 응답                                                                                                                                                                                                   |                                      |
| 유저 비밀번호는 암호화해서 저장한다                                                        | 회원가입 시 password는 복호화 불가능한 방식으로 암호화해서 저장한다                                                                                                                                                                                                            |                                      |
| 유저 관리 라이브러리를 사용할 수 없다                                                      |                                                                                                                                                                                                                                                                                |                                      |