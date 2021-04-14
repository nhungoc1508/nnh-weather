client_id = 'cCDZL9dbBhk86Gr0z1x2BJWfN8Fo04oS0X3rZSW3Nk0'
url = 'https://api.unsplash.com/photos/random'

def get_creds():
    return(url, client_id)
# unsplash_image = requests.get(url, params={'client_id' = client_id}.json()['urls']['small'])