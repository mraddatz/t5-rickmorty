from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

API_URL = 'https://integracion-rick-morty-api.herokuapp.com/graphql'

def url_id(url, id_num=""):
  if url[-1] == "/":
    return id_num
  else:
    return url_id(url[0:-1], url[-1]+id_num)




def index(request):
    page = 1
    query = """query {{episodes (page: {page}) {{info {{count next}} results {{id name air_date episode}} }} }}"""
    episodes = []

    while True:
        response = requests.post(API_URL, json={'query': query.format(page=str(page))})
        response_dic = json.loads(response.text)
        print("Responde DIC")
        print(response_dic)
        next_page = response_dic['data']['episodes']['info']['next']
        page_results = response_dic['data']['episodes']['results']
        print(next_page)
        for episode in page_results:
            episode_dic = {}
            episode_dic['id'] = episode['id']
            episode_dic['name'] = episode['name']
            episode_dic['air_date'] = episode['air_date']
            episode_dic['episode'] = episode['episode']
            episodes.append(episode_dic)

        if next_page:
            page += 1
        else:
            break

    
    data = {
        'episodes': episodes,
    }

    return render(request, 'rickmortyapp/home.html', data)
    #return HttpResponse("Http response")

def episode(request, episode_id):
    print("Entre a episode")
    query = "query {{ episode (id: {id}) {{ name air_date episode characters {{ id name }} }} }}".format(id=str(episode_id))


    response = requests.post(API_URL, json={'query': query})
    response = json.loads(response.text)
    episode = response['data']['episode']
    data = {
        'episode': episode,
    }
    return render(request, 'rickmortyapp/episode.html', data)

def character(request, character_id):
    query = "query {{character (id: {id}) {{name status species type gender origin {{id name}}location {{id name}} image episode {{id name}}}}}}".format(id = str(character_id))
    response = requests.post(API_URL, json={'query': query})
    response = json.loads(response.text)
    character = response['data']['character']

    print("Characters")
    print(character)
    data = {
        'character': character,
    }
    return render(request, 'rickmortyapp/character.html', data)

def location(request, location_id):
    query = "query {{ location (id: {id}) {{ name type dimension residents {{ id name }} }} }}".format(id = location_id)
    response = requests.post(API_URL, json={'query': query})
    response = json.loads(response.text)
    location = response['data']['location']
    data = {
        'location': location,
    }


    return render(request, 'rickmortyapp/location.html', data)

def search(request):

    search = request.POST.get('search', '')

    characters_search_query = """ query {{ characters (filter: {{name: "{search_query}" }}) {{ results {{ id name }} }} }}""".format(search_query=search)
    
    response_characters = requests.post(API_URL, json={'query': characters_search_query})
    response_characters = json.loads(response_characters.text)
    print("Response episodes")
    print(characters_search_query)
    try:
        response_characters = response_characters['data']['characters']['results']
    except: 
        response_characters = []

        
    episodes_search_query = """ query {{ episodes ( filter: {{name: "{search_query}" }}) {{ results {{ id name }} }} }}""".format(search_query=search)
    response_episodes = requests.post(API_URL, json={'query': episodes_search_query})
    response_episodes = json.loads(response_episodes.text)
    print("Response episodes")
    print(response_episodes)
    try:
        response_episodes = response_episodes['data']['episodes']['results']
    except: 
        response_episodes = []
    
    
    location_search_query = """ query {{ locations (filter: {{name: "{search_query}" }}) {{ results {{ id name }} }} }}""".format(search_query=search)
    response_locations = requests.post(API_URL, json={'query': location_search_query})
    response_locations = json.loads(response_locations.text)
    print("Response location")
    print(response_locations)
    try:
        response_locations = response_locations['data']['locations']['results']
    except: 
        response_locations = []
    # characters = name_search('character', search_term)
    # locations = name_search('location', search_term)
    # episodes = name_search('episode', search_term)

    data = {
        'search_query': search,
        'characters': response_characters,
        'locations': response_locations,
        'episodes': response_episodes,

    }


    return render(request, 'rickmortyapp/search.html', data)


def character_search(search_string):
    request_link = API_URL + search_type + '/?name=' + search_string
    response_dic = requests.get(request_link).json()
    if 'error' in response_dic.keys():
        return []
    pages = response_dic['info']['pages']
    output = []
    for _ in range(1, pages+1):
        output += response_dic['results']
        next_url = response_dic['info']['next']
        if next_url:
            response_dic = requests.get(next_url).json()
    
        # characters
    query = """query {{characters(filter: {{name: "{search_term}" }}) {{results {{id name}}}}}}"""
    try:
        r = requests.post(_URL_API, json={'query': query_characters.format(search_term=search_term)})
        json_data = json.loads(r.text)
        characters = json_data['data']['characters']['results']
    except: 
        characters = [{'id': "",
                       'name': ""}]
    
    return output