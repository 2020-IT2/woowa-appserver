# Woowa - Appserver Read Me

<p align="center">
    <img src="pic/main.png" height="500"/>
</p>
<h4 align="center">사용자 기반 음식 추천 & 요식업계 시장 분석 어플리케이션</h4>

<p align="center">
    이 어플리케이션은 2020년 아주대학교 집중 교육의 일환으로 제작되었습니다. 이 어플리케이션은 실제 상업적 목적이 포함되어 있지 않습니다. 전체적인 디자인 모티브로 배달의 민족 어플리케이션을 참고하였습니다. 이 프로젝트는 <a href="https://github.com/hankyul-needs-girfriends/woowa-appserver">서버</a>, <a href="https://github.com/hankyul-needs-girfriends/woowa-crawler">크롤링</a>, <a href="https://github.com/hankyul-needs-girfriends/woowa-ML">머신러닝</a> 레포와 같이 운영되어 왔습니다. 하지만 프로젝트의 주요 레포지토리는 <a href="https://github.com/hankyul-needs-girfriends/woowa-android-main-">안드로이드 레포지토리</a> 입니다. 이 프로젝트는 강*결, 윤*은, 허*철의 도움으로 만들어졌습니다. 같이 고생한 팀원분들께 감사의 말을 전합니다.
</p>


대부분의 코드는 기존의 다른 [레포지토리](https://github.com/Algostu/dodam-appserver)를 참고하여 구현하였습니다. 



## Tutorial

```
git clone https://github.com/hankyul-needs-girfriends/woowa-appserver.git
pip install -r "requirements.txt"
```

You can start server by simple command

```
python manage.py runserver 
```