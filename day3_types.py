notification_response = {
    "code":200,
    "user_id":1647459472,
    "unread_count":3,
    "notification_data":{
        "total":4,
        "items":[
            {"type":"video","content":"哈哈哈","timestamp":"2024-06-01T12:00:00Z","is_read":False},
            {"type":"image","content":"啊啊啊啊","timestamp":"2024-06-02T12:00:00Z","is_read":True},
            {"type":"text","content":"你好世界","timestamp":"2024-06-03T12:00:00Z","is_read":False},
            {"type":"link","content":"链接内容","timestamp":"2024-06-04T12:00:00Z","is_read":False}
        ]
    }
}
print(notification_response["notification_data"]["items"][1]["content"])#取第二条通知的内容
#取所有未读通知type列表
unread_types = [] #准备一个空列表来存储所有未读通知的类型
for a in notification_response["notification_data"]["items"]:
    if a["is_read"]==False:
        unread_types.append(a["type"])
print(unread_types) #直接打印的是列表的的内容读通知的类型
for t in unread_types: #用for 语句从列表里把每个内容取出来并打印
    print(t)