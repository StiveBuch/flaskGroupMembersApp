import vk
from flask import Flask
from flask import render_template_string
import os
from envparse import env
env.read_envfile()
app = Flask(__name__)
token = env('API_TOKEN')

@app.route("/")
def getGroups():
    api = vk.API(access_token=token)
    # получить от вк группы одного пользователя по user_id https://dev.vk.com/ru/method/groups.get
    allGroups = api.groups.get(user_id=241222399,extended=1,fields='description',count=1000,v=5.199)
    
    groups=allGroups['items']
    print(groups)
    res_string='<H2>сайт</H2>'
    for group in groups:
        print('https://vk.com/club', group['id'],'  ',group['name'], sep='')
        res_string+='<img src=\"'
        res_string+=group['photo_50']
        res_string+='\'>'
        res_string+='<br>'
        res_string+='<p>'
        res_string+=group['name']
        res_string+='</p>'
        # res_string+='<br>'
        res_string+='<a href=\">'
        res_string+='https://vk.com/club'
        res_string+= str(group['id'])
        res_string+='\'>https://vk.com/club'
        res_string+=str(group['id'])
        res_string+='</a>'
        res_string+='<br>'
        res_string+='  <p>'
        res_string+=str(group.get('description'))
        res_string+='</p>'
        res_string+='<br>'
    return render_template_string(res_string)

@app.route("/mem")
def getGroupMembers():
    api = vk.API(access_token=token)
    # получить от вк пользователей по group_id https://dev.vk.com/ru/method/users.get
    allGroups = api.groups.getMembers(group_id=211211142,offset=0,count=100,fields='bdate,city,sex,country,photo_400_orig',v=5.199)
    
    groups=allGroups['items']
    girls=list(filter(lambda item: item['sex'] == 1, groups)) # 
    print('len girls=',len(girls),'len all = ', len(groups))
    res_string='<H2>сайт</H2>'
    for man in girls:
        # печать отладочной информации в консоль - чисто для себя
        print('https://vk.com/id', man['id'],'  ',str(man.get('first_name')) + ' '+  str(man.get('last_name')), sep='')
        # картинка
        res_string+='<img src=\"'
        res_string+=str(man.get('photo_400_orig'))
        res_string+='\'>'
        # перенос
        res_string+='<br>'
        # название (параграф)
        res_string+='<p>'
        res_string+=str(man.get('first_name')) + ' '+  str(man.get('last_name'))
        res_string+='</p>'
        # ссылка
        res_string+='<a href=\">'
        res_string+='https://vk.com/id'
        res_string+= str(man['id'])
        res_string+='\'>https://vk.com/id'
        res_string+=str(man['id'])
        res_string+='</a>'
        # перенос
        res_string+='<br>'
        # имя (параграф)
        res_string+='  <p>'
        res_string+=str(man.get('first_name'))
        res_string+=str(man.get('last_name'))
        res_string+='</p>'
        res_string+='<br>'
    return render_template_string(res_string)

if __name__ == '__main__':
    app.run(debug=True)