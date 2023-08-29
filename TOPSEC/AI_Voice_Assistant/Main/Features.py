import wikipedia
def Wiki(Audio):
    Audio = Audio.lower()
    Audio = Audio.replace("wikipedia","")
    Audio = Audio.replace("search","")
    Search =  "According to Wikipedia...\n"
    try :
        Search += wikipedia.summary(Audio,sentences = 2)
    except :
        Search = "No Information Found"
    return Search