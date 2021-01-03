[Send Request]
url :  https://fcm.googleapis.com/fcm/send
method : post
header : {
	Content-Type : application/json
	Authorization : key=server_token

}
body : {
  "to":"디바이스 토큰 값",
  "priority" : "high",
  "data" : {
    "title" : "Postman",
    "message" : "Hello, World!"
  },
   "notification":{
      "title":"Portugal vs. Denmark",
      "body":"great match!"
    }
}

[Return Result]
{
"multicast_id":6959721758744553407,
"success":1,
"failure":0,
"canonical_ids":0,
"results":
[{"message_id":"0:1603951573798332%1c24d486f9fd7ecd"}]
}

server token : AAAAfktu114:APA91bFKJ0O4YF28d_IgbGJRmf6iyjSMdYEheVu_zLfvlNKi-vHBSeKuSlqEP-8JnWGG1e0s17-Ask5wKoFMOZLA11jXaS8hJLuGPA-pSQt5d_ylmHJfv8YlKzQ8dsjq7kOAIpv2bpCz

device token : cbjVdBd6QUiAB-8abvn7jH:APA91bGLzbrwmIiIVTBsxQmzsruQ-WLvOVgCH-XrUM2n9hME6p0xe92XVqlia0EzEnTWPCzncLZZ0J7UfCGvXtd-rWEYovJiGPK6MQxtYMuLqQjlx5itgzdzn07jhB0K2KUl6wDFC8mb
