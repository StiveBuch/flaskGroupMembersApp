import vk
from flask import Flask
from flask import render_template_string, render_template, request
import os
from envparse import env
env.read_envfile()
app = Flask(__name__)
token = env('API_TOKEN')

@app.route("/")
def getGroups():
    api = vk.API(access_token=token)
    # получить от вк группы одного пользователя по user_id https://dev.vk.com/ru/method/groups.get
    manId=12
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
    allGroups = api.groups.getMembers(group_id=21121142,offset=0,count=100,fields='bdate,city,sex,country,photo_400_orig',v=5.199)
    
    groups=allGroups['items']
    girls=list(filter(lambda item: item['sex'] == 1, groups)) # 
    print('len girls=',len(girls),'len all = ', len(groups))
    context=girls 
    return render_template('getMembers.html', context=context)

@app.route("/search")
def getSearchUsers():
    api = vk.API(access_token=token)
    # получить от вк пользователей по group_id https://dev.vk.com/ru/method/users.get
    allUsers = api.users.search(q="Кристина",city=1,offset=0,count=1000,age_to=27,fields='bdate,relatives,name,games,books,career,screen_name,sex,about,city,photo_max_orig,sex,country',v=5.199)
    # getCities()
    print(allUsers)
    users=allUsers['items']
    girls=list(filter(lambda item: item['sex'] == 1, users)) # 
    print('len girls=',len(girls),'len all = ', len(users))
    context=girls 
    return render_template('search.html', context=context)

@app.route('/search_form', methods=['POST', 'GET'])
def my_form():
    name = request.form['text']
    
    api = vk.API(access_token=token)
    # получить от вк пользователей по group_id https://dev.vk.com/ru/method/users.get
    allCities = api.database.getCities(q=name,need_all=1,count=100,v=5.199)
    print('===города===',allCities)
    cityId=allCities['items'][0]['id']
    print('===город===',allCities['items'][1]['id'])
    allUsers = api.users.search(q="Рита",city=cityId,offset=0,count=1000,fields='bdate,relatives,name,games,books,career,screen_name,sex,about,city,photo_max_orig,sex,country',v=5.199)
    # getCities()
    print('===пользователи===',allUsers)
    users=allUsers['items']
    girls=list(filter(lambda item: item['sex'] == 1, users)) # 
    print('len girls=',len(girls),'len all = ', len(users))
    context=girls 
    return render_template('search_form.html', context=context)

@app.route('/search_gr', methods=['POST', 'GET'])
def getSearchByGroup():
    abd = request.form['text']
    api = vk.API(access_token=token)
    allUsers = api.users.search(q="Кристина",group_id=abd,offset=0,count=1000,fields='bdate,relatives,name,games,books,career,screen_name,sex,about,city,photo_max_orig,sex,country',v=5.199)
    # getCities()
    print('===пользователи===',allUsers)
    users=allUsers['items']
    girls=list(filter(lambda item: item['sex'] == 1, users)) # 
    print('len girls=',len(girls),'len all = ', len(users))
    context=girls 
    return render_template('search_form.html', context=context)
@app.route('/search2', methods=['POST'])
def my_form_post():
    name = request.form['text']
    
    api = vk.API(access_token=token)
    # получить от вк пользователей по group_id https://dev.vk.com/ru/method/users.get
    allCities = api.database.getCities(q=name,need_all=1,count=100,v=5.199)
    cityId=allCities['items'][1]['id']
    allUsers = api.users.search(q="",city=cityId,offset=0,count=1000,age_to=27,fields='bdate,relatives,name,games,books,career,screen_name,sex,about,city,photo_max_orig,sex,country',v=5.199)
    # getCities()
    print(allUsers)
    users=allUsers['items']
    girls=list(filter(lambda item: item['sex'] == 1, users)) # 
    print('len girls=',len(girls),'len all = ', len(users))
    context=girls 
    return render_template('search.html', context=context)


@app.route("/cities")
def getAllCities():
    api = vk.API(access_token=token)
    # получить от вк пользователей по group_id https://dev.vk.com/ru/method/users.get
    allCities = api.database.getCities(need_all=1,count=100,v=5.199)
    print(allCities)
    cities=allCities['items']
    print(cities)
    context=cities 
    return render_template('cities.html', context=context)

@app.route("/spec")
def getCitiesByName():
    context = {}
    context.pop(getCities("Москва"))


    return render_template('cities.html', context=context)

def getCities(name):
    api = vk.API(access_token=token)
    # получить от вк пользователей по group_id https://dev.vk.com/ru/method/users.get
    allCities = api.database.getCities(q=name,need_all=1,count=100,v=5.199)
    print(allCities)
    cities=allCities['items']
    print(cities)
    return cities

if __name__ == '__main__':
    app.run(debug=True)
