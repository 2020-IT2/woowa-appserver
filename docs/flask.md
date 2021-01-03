# flask webserver 실행 설명 문서

flask webserver는 flask-script 모듈을 활용했기 때문에 cmd에서 여러가지 옵션을 줄 수 있습니다. 모든 옵션은 다음과 같은 형태로 실행 됩니다.

```
python3 manage.py [arg] [option] [option] ...
```

## arg list

1. runserver  
서버를 실행 시키는 옵션입니다.

2. db
데이터 베이스를 업데이트할 때 실행하는 구문 입니다. 해당 구문을 실행하고 난 뒤에는 꼭 db 서버를 열어서 확인해 주시기 바랍니다.

```
python3 manage.py db migrate
python3 manage.py db upgrade
```

3. crawler
열심히 크롤링해서 .json 형식으로 저장한 값들을 db에 저장하는 기능 입니다. 총 3가지 기능이 있습니다. 학교 정보를 저장하는 기능, 급식표를 저장하는 기능, 공모전을 저장하는 기능 입니다. 각 기능은 수동으로 동작시켜 주어야 하며 해당 기능과 서버 동시에 사용 가능 한지 확인이 필요 합니다. (아마될 것으로 예상...)

`python3 manage.py crawler -T [option]`

option list
  - S : 학교 정보 저장 하는 기능
  - C : 급식 정보를 저장 하는 기능
  - D : 공모전 정보를 저장하는 기능

이 기능을 사용할때는 DB가 한번에 바뀌므로 에러가 자주 일어난다. 따라서 이때는 DB 서버 설정을 살짝 바꿔주어야 한다. `set @@global.sql_mode=""`커맨드를 통해서 `STRICT_TRANS_TABLES`옵션을 꺼주어야 한다. 꺼주고 나서는 꼭 select를 통해서 확인해주자.
기능을 쓰고 나서는 다시 옵션을 켜주어야 한다.
```
select @@global.sql_mode;
+-------------------------------------------------------------------------------------------------------------------------------------------+
| @@global.sql_mode                                                                                                                         |
+-------------------------------------------------------------------------------------------------------------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+-------------------------------------------------------------------------------------------------------------------------------------------+
```

```
set @@global.sql_mode =
"ONLY_FULL_GROUP_BY,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION";
```

```
set @@global.sql_mode = "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION";
```
