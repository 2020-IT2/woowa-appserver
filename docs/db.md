## DataBase Readme

1. current database is based on .sql files.

2. ORM vs SQL :

- sql방식 : 그냥 쿼리 쓰면 된다.
- [orm방식](https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#inserting-records)

If you want to create or drop table, you should use mysql workbench, not an orm. If you use orm, it is expandable. But more bigger, more complexer. I don't know

3. session db용 redis server 설정

- 서버 포트 : 127.0.0.1:6379
- 비밀번호 : 1234

현재 외부 접속을 막아놨다. 따라서 web server에서만 접속 가능하다.
또한 메모리는 20mb를 할당했고 메모리 초과시 가장 오래된 데이터 부터 지운다.

```
sudo vim /etc/redis/redis.conf
maxmemory 1g
maxmemory-policy allkeys-lru
```

서버가 열려있는지 확인 하는 명령어와 재시작하는 명령어는 다음과 같다.

```
netstat -nlpt | grep 6379
sudo systemctl restart redis-server.service
```

서버를 shell에서 접근하는 것은 다음 명령어를 사용하면 된다.

```
$ redis-cli
127.0.0.1:6379> auth ngleredis1234
OK
```

4. 기존 SQL 문드로 작성된 코드 ORM 방식으로 변경하는 방법

`flask-sqlacodegen` 라이브러리를 사용하면 된다. 자세한 것은 이 [블로그](https://beomi.github.io/2017/10/20/DB-To-SQLAlchemy-Model/)를 참고하자. 그리고 만약 에러가 난다면 이 [블로글](https://yenoss.github.io/2017/09/11/pythonMysql_conf.html)를 참고하면 된다.

5. ORM 방식으로 DB 사용할 경우 Model.py 수정할 때마다 Upgrade하는 방법

flask-migration의 [공식홈페이지](https://flask-migrate.readthedocs.io/en/latest/)를 참고하는 것이 가장 빠르다. 해당 문서에서 보면 migration을 버전별로 만들 수 있다고 나와 있다. migration을 통해서 현재 dataBase와 model.py의 차이점을 가지고 upgade method를 만들어내는 방식이다. 즉, flask-migration을 통해서 db가 바뀔 때마다 손 쉽게 변경 사항을 적용할 수 있다.

flask-migration 공식 홈페이지에 보면 flask-script를 통해서 manage.py로 한번에 관리하는 방법이 있다. 이 방법을 통해서 flask-migration command를 manage.py 로 한번에 관리 할 수 있다. 이 방식은 나중에 test까지 한번에 cmd로 관리한다면 편하게 사용할 수 있다.

현재 내가 사용하는 커맨드는 model.py가 바뀔 때마다 사용하는 커맨드 하나 밖에 없다.

```
$ python manage.py db init (처음 한법만)
$ python manage.py db migrate -m "Initial migration." (업데이트 될 때마다)
$ python manage.py db upgrade (업데이트 될 때 마다)
$ python manage.py db --help (history를 볼 수 있는 방법같을 것을 알려주는 command line helper이다.)
```

6. ORM 방식으로 DB 접근하는 방법

flask-sqlalchemy의 [공식문서](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)를 보는 것이 도움이 된다.

7. server_defalut = FetchedValue() 에러 해결방법

migration에 `from sqlalchemy.schema import FetchedValue`를 추가해준다. 이걸 왜 import안해주는지는 잘 모르겠지만...
