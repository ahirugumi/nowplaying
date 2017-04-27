# coding: utf-8

from mastodon import Mastodon
import appscript
import time, os
import json

def getAlbumNameAndAlbumDirectory(album):
    # iTurnesは、アルバム名の最後に.があると_のパスになる
    albumDirectory=album
    if (albumDirectory.endswith('.')):
        albumDirectory = album.rstrip('.') + '_'
    # iTurnesは、アルバム名に/があると_のパスになる
    albumDirectory = albumDirectory.replace('/', '_')
    albumName = album.replace('/', '_')
    print(albumName, albumDirectory)
    return (albumName, albumDirectory)

def getArtworkFile(current, album, artist):
    # アートワークの場所を特定し、メディア情報を取得
    # 音楽ファイルがあるベースディレクトリ
    basePath = '/Volumes/MyHDD2/iTunes/Music/'
    # アートワークのファイル名を形成
    albumName, albumDirectory = getAlbumNameAndAlbumDirectory(album)
    imagePath = basePath + artist + '/' + albumDirectory + '/' + artist + '-' + albumName
    return imagePath

def getMediaType(artworkFile):
    # ファイル形式がPNGかJPEGのどちらかなので、トライをしてから決定する
    mediaPng = {'png':'.png'}
    mediaJpeg = {'jpeg':'.jpg'}
    tryImagePath = artworkFile + mediaPng['png']
    mediaType = mediaPng
    ret=os.path.exists(tryImagePath)
    if (ret==False): mediaType = mediaJpeg
    return mediaType

def getArtWorkFullPath(artworkFile, mediaType):
    for ext in mediaType.values():
        artworkFullPath = artworkFile + ext
        return artworkFullPath

def getMusicData(now):
    # 曲名
    current = now.name.get()
    # アルバム名
    album = now.album.get()
    # アーティスト名
    artist = now.artist.get()
    return (current, album, artist)

# Mastodonにログイン
client = Mastodon(client_id="credential.txt", access_token="login.txt", api_base_url = "https://mstdn.jp")

# iTunesから今再生中の音楽ファイルの情報を取得する
itunes = appscript.app('iTunes')
# 次の曲は、初回は初期化しておく
prev = ''
current, album, artist = getMusicData(itunes.current_track)

# 無限ループし、次の曲に移ったかどうかを判定し、Mastodonへトゥートする
while(True):
    if (current != prev):
        current, album, artist = getMusicData(itunes.current_track)

        # アートワークの場所を特定し、メディア情報を取得
        # アートワークファイルの場所を特定
        artworkFile = getArtworkFile(current, album, artist)

        # アートワークファイルを決定するため、メディアタイプとファイルの拡張子を決定
        mediaType = getMediaType(artworkFile)
        print('mediaType: ' + str(mediaType))

        # アートワークのフルパスを取得
        artworkFullPath = getArtWorkFullPath(artworkFile, mediaType)
        print('Artwork file full path: ' + artworkFullPath)

        # Mastodonにトゥートする
        text = u"\n\n{} - {} - {}\n\n#nowplaying #metal #songinfo #なうぷれ".format(artist, album, current)
        for mediaName in mediaType.keys():
            media_files = [client.media_post(media, "image/" + mediaName) for media in [artworkFullPath]]
        client.status_post(status=text, media_ids=media_files)

    # 現在の曲を次の曲にセット
    prev = current
    current, album, artist = getMusicData(itunes.current_track)
    time.sleep(10)

