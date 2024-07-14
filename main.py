import vk
from flask import Flask
from flask import render_template_string, render_template
import os
from envparse import env
env.read_envfile()
app = Flask(__name__)
token = env('API_TOKEN')

@app.route("/")
def getGroups():
    api = vk.API(access_token=token)
    # получить от вк группы одного пользователя по user_id https://dev.vk.com/ru/method/groups.get
    manId=241222399
    allGroups = api.groups.get(user_id=manId,extended=1,fields='description',count=1000,v=5.199)

    groups=allGroups['items']
    context={}
    context['1']= groups # list(filter(lambda item: item.get('country') == 1, groups))
    context['title']=manId
    # print(groups)
    
    return render_template('getGroups.html', context=context)

@app.route("/mem")
def getGroupMembers():
    api = vk.API(access_token=token)
    # получить от вк пользователей по group_id https://dev.vk.com/ru/method/users.get
    allGroups = api.groups.getMembers(group_id=211211142,offset=0,count=100,fields='bdate,city,sex,country,photo_400_orig',v=5.199)
    
    groups=allGroups['items']
    girls=list(filter(lambda item: item['sex'] == 1, groups)) # 
    print('len girls=',len(girls),'len all = ', len(groups))
    context=girls 
    return render_template('getMembers.html', context=context)

if __name__ == '__main__':
    app.run(debug=True)