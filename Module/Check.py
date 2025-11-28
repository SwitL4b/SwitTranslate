from Module.Translate.Utils import Config
def check():
    if Config.Discord.Token() == '':
        return False
    if Config.Gemini.ApiKey() == '':
        return False
    return True