# from imdb import IMDb
# from pprint import pprint
# # create an instance of the IMDb class
# ia = IMDb()
# # get a movie
# #print((ia.get_movie('0133093')['directors']))
# #pprint(vars((ia.search_movie('the blacklist')[0])))
# movie = ia.get_movie('2741602')
# print(movie['kind'])
# ia.update(movie, 'main')
# pprint(vars(movie))

#https://medium.com/@annissouames99/how-to-upload-files-automatically-to-drive-with-python-ee19bb13dda
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()

# Try to load saved client credentials
gauth.LoadCredentialsFile("C:\\Users\\Dima\\PycharmProjects\\Moridim.tv-downloader\\mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("C:\\Users\\Dima\\PycharmProjects\\Moridim.tv-downloader\\mycreds.txt")


drive = GoogleDrive(gauth)

file_list = drive.ListFile({'q': "'1e4dwqUVtAroKJui9tR3DwO2QadV82Wrf' in parents and trashed=false"}).GetList()
for file1 in file_list:
  print('title: %s, id: %s' % (file1['title'], file1['id']))
  file1.Delete()


# file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": '1e4dwqUVtAroKJui9tR3DwO2QadV82Wrf'}], 'title': 'Deception.2018.S01E01.HDTV.x264-KILLERS[eztv].mkv'})
# file.SetContentFile('D:\\series\\Deception\\Deception.2018.S01E01.HDTV.x264-KILLERS[eztv].mkv')
# file.Upload()