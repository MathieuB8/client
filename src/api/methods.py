def download_mod_list(api, page_size, page_number, on_finished, on_error):
#    req = api._get('/mods')
    req = api._get('/data/mod', {
        'include': 'latestVersion',
#XXX  {"errors":["InvalidValueException: Invalid value: Mod doesn't contain the field latestVersion.createTime"]}
#XXX Why this no work?
#        'sort': '-latestVersion.createTime',
        'page[size]': page_size,
        'page[number]': page_number,
        'page[totals]': 1
        })
    req.finished.connect(on_finished)
    req.error.connect(on_error)
    req.run()

    return req

def upload_mod(mod_dir, api, on_finished, on_error):
    temp = tempfile.NamedTemporaryFile(mode='w+b', suffix=".zip", delete=False)
    zipped = zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED)
    zipdir(mod_dir, zipped, os.path.basename(mod_dir))
    zipped.close()
    temp.flush()

    fname = os.path.basename(mod_dir) + '.zip'

    upload = api.create_upload(temp.name, fname)
    req = api._post('/mods/upload', upload)
    req.finished.connect(on_finished)
    req.error.connect(on_error)
    req.run()

    return req

def search_replays(minRating, playerName, mapName, featuredMod, api, page_size, page_number, on_finished, on_error):
    searchFilter = []
    if minRating:
        #XXX This simple filter means post-processing is needed to filter for proper rank (mean-3*deviation)
        searchFilter.append('playerStats.beforeMean=gt={}'.format(minRating))
    if playerName:
        searchFilter.append('playerStats.player.login==\'{}*\''.format(playerName.replace('\'','\\\'')))
    if mapName:
        searchFilter.append('mapVersion.map.displayName==\'{}*\''.format(mapName.replace('\'','\\\'')))
    if featuredMod:
        searchFilter.append('featuredMod.displayName==\'{}*\''.format(featuredMod.replace('\'','\\\'')))

    searchFilter = ';'.join(searchFilter)

    req = api._get('/data/game', {
        'include': 'mapVersion,mapVersion.map,playerStats,playerStats.player,featuredMod',
        'filter': searchFilter,
        'page[size]': page_size,
        'page[number]': page_number
        })
    req.finished.connect(on_finished)
    req.error.connect(on_error)
    req.run()

    return req

def recent_replays(api, page_size, page_number, on_finished, on_error):
    searchFilter = 'endTime=isnull=false'

    req = api._get('/data/game', {
        'include': 'mapVersion,mapVersion.map,playerStats,playerStats.player,featuredMod',
        'filter': searchFilter,
        'page[size]': page_size,
        'page[number]': page_number
        })
    req.finished.connect(on_finished)
    req.error.connect(on_error)
    req.run()

    return req

#request : https://api.faforever.com/data/player?include=names&fields[player]=login,names&fields[nameRecord]=name,changeTime&&filter[player]=login==player_nick
def namesPreviouslyKnown(api, page_size, page_number, player_nick, on_finished, on_error):
    req = api._get('/data/player', {
        'include': 'names',
        'fields[player]': 'login,names',
        'fields[nameRecord]': 'name,changeTime',
        'filter[player]': "login=='"+player_nick+"'",
        'page[size]': page_size,
        'page[number]': page_number
        })
    req.finished.connect(on_finished)
    req.error.connect(on_error)
    req.run()

    return req

#request : https://api.faforever.com/data/player?include=names&filter=(login=='+self.user.name+',names.name=='+self.user.name+')'
def nickUsedByOther(api, page_size, page_number, player_nick, on_finished, on_error):
    searchFilter="(login=='"+player_nick+"',names.name=='"+player_nick+"')"
    req = api._get('/data/player', {
        'include': 'names',
        'filter': searchFilter,
        'page[size]': page_size,
        'page[number]': page_number
        })
    req.finished.connect(on_finished)
    req.error.connect(on_error)
    req.run()

    return req

