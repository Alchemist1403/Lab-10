import random
import webbrowser
import requests
import pyttsx3
import speech_recognition as sr


class VoiceAssistant:
    ''' Голосовой ассистент с функцией поиска информации о каком-либо слове'''
    def __init__(self,api_key):
        self.tts_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.api_key = api_key
        self.in_dialog = False

    def say(self,text):
        '''Голосовой ассистент воспроизводит текст (говорит)'''
        print(f'Assistant: {text}')
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        '''Голосовой ассистент слушает пользователя и преобразует звук в текст'''
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio, language='en-GB')
            print(f'You`ve just said: {command}')
            return command.lower()

        except sr.UnknownValueError:
            self.say('Incorrect command')
            return ''

        except sr.RequestError:
            self.say('Recognizer error')
            return ''

    def get_word(self,word):
        '''Голосовой ассистент ищет информацию о слове из словаря'''
        self.word = word
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}'
        response = requests.get(url).json()
        return response

    def run(self):
        '''Голосовой ассистент работает в реальном времени'''
        self.say('Your voice assistant is activated and ready to work!')

        while True:
            command = self.listen().lower()
            if self.in_dialog:
                if "find" in command:
                    self.say('Tell me what word do you want to find. Say only one word')
                    word = self.listen().lower()
                    self.say(f'You said: {word}')
                    res = self.get_word(word)
                    print(res)
                    self.say('What do you want to do with this information?')

                    while True:
                        command = self.listen().lower()
                        if 'meaning' in command:
                            meaning =  res[0]['meanings'][random.randint(0,len(res[0]['meanings'])-1)]['definitions'][0]['definition']
                            self.say(meaning)

                        elif 'example' in command:
                            example = res[0]['meanings'][random.randint(0,len(res[0]['meanings'])-1)]['definitions'][0]['example']
                            if not 'example' in res[0]['meanings'][random.randint(0,len(res[0]['meanings'])-1)]['definitions'][0]:
                                self.say('There`s no example')
                            else:
                                self.say(example)

                        elif 'link' in command:
                            link = res[0]['sourceUrls'][0]
                            webbrowser.open(link)

                        elif 'save' in command:
                            file = open('last_word.txt','w')
                            file.write(f'{word}\nDefinition:{res[0]['meanings'][random.randint(0,len(res[0]['meanings'])-1)]['definitions'][0]['definition']}\nLink:{res[0]['sourceUrls'][0]}')
                            file.close()

                        elif 'stop' in command:
                            self.say('Thank you for using my new feature!')
                            break

                        else:
                            self.say('Give me a correct command please')
                        self.say('Something else?')

                elif "goodbye" in command:
                    self.say('Goodbye!')
                    break
                else:
                    self.say('Give me a correct command please')

            if 'hello assistant' in command:
                self.say('Hello! Give me a task.')
                self.in_dialog = True


if __name__ == '__main__':
    api_key = '090447fad4cab7e8c96be5871abc7332'
    assistant = VoiceAssistant(api_key)
    assistant.run()
