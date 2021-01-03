# login

1. db table 수정 :

user_credential 테이블 없애기
userName 없애기

2. 배포 판에서는 모든 유저의 정보 초기화 후에 내보내기

3. 학교 및 지역 정보 업데이트

4. 자동 로그인

sharedPreferences 라는 것을 이용해서 기능을 만들었다. 어짜피 버튼을 누르냐 마냐 이기때문에 아이디, 비밀번호를 저장하기 보다는 로그아웃 했을 때 자동 로그인이 되지 않도록 하기 위해서 만든 기능이다. 예제 코드는 이 [블로그](https://m.blog.naver.com/PostView.nhn?blogId=rain483&logNo=220812563378&proxyReferer=https:%2F%2Fwww.google.com%2F)에서 참고하였다.

아래 코드는 로그아웃시 작동해야 하는 코드이다. 현재는 로그아웃 기능을 만들지 않았기 때문에 별로 쓸모가 없다.
```
SharedPreferences auto = getSharedPreferences("auto", Activity.MODE_PRIVATE);
                SharedPreferences.Editor editor = auto.edit();
                //editor.clear()는 auto에 들어있는 모든 정보를 기기에서 지웁니다.
                editor.clear();
                editor.commit();
```

5. 회원가입 진행 후 너무 오래 시간이 지난 경우

카카오 엑세스 토큰 만료 시간이 지난 후에는 처음 부터 다시 시작하도록 함.
