#!/usr/bin/env python3

""" Butlor Based on Cloud Speech Demo:
Intention is to use the google cloud speech API to better recognize the commands for the Butlor bot.
It summurized the steps here:
1- record user voice
2- send to google cloud and get a text back
3- if the text can be handled by Butlor then use butlor
4- if not insert the text for the google assistant.
However, it seems that the google assistant cannot take a text as input
"""
import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import aiy.assistant.grpc
from mschatbot import ask_butlor


def main():
    cloud_recognizer = aiy.cloudspeech.get_recognizer()
    cloud_recognizer.expect_hotword(['butler'])
    google_assistant = aiy.assistant.grpc.get_assistant()
    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    status_ui = aiy.voicehat.get_status_ui()

    var_bool_to_butler = False
    aiy.audio.get_recorder().start()

    while True:
        print('Press the button and speak')
        led.set_state(aiy.voicehat.LED.ON)
        status_ui.status('ready')

        button.wait_for_press()
        print('Listening...')
        status_ui.status('listening')
        var_bool_to_butler = False


        led.set_state(aiy.voicehat.LED.DECAY)

        text_recognized_by_cloud = cloud_recognizer.recognize()
        audio_from_assistant, text_from_assistant = google_assistant.recognize()

        status_ui.status('thinking')
        if not text_recognized_by_cloud:
            status_ui.status('stopping')
            print('Handled by Google Assistant "', text_from_assistant, '"')
            aiy.audio.say(audio_from_assistant)
        else:
            status_ui.status('stopping')
            #already in Butler due to the hotword detection
            print("Butler handling:  "+text_recognized_by_cloud)
            if 'goodbye' in text_recognized_by_cloud:
                break
            else:
                var_bool_to_butler = True
                led.set_state(aiy.voicehat.LED.BLINK_3)
                var_result = ask_butlor(text_recognized_by_cloud)
                aiy.audio.say(var_result)

        #if not var_bool_to_butler:
        #    print('Handled by Google Assistant "', text_from_assistant, '"')
        #    aiy.audio.say(audio_from_assistant)


if __name__ == '__main__':
    main()
