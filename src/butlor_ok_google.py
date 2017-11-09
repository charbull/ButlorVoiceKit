#!/usr/bin/env python3
# Charbel Kaed

""" Schizophrenic Bot: Google Assistant and Butlor """

import logging
import subprocess
import re
import aiy.assistant.grpc
import aiy.audio
import aiy.voicehat
from mschatbot import ask_butlor


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


def main():
    """ Main Butlor """
    status_ui = aiy.voicehat.get_status_ui()
    led = aiy.voicehat.get_led()

    status_ui.status('starting')
    assistant = aiy.assistant.grpc.get_assistant()
    button = aiy.voicehat.get_button()
    ok_google_hotword = "OK Google "
    #Open the recorder
    with aiy.audio.get_recorder():
        print('Butlor is ready')
        led.set_state(aiy.voicehat.LED.ON)
        aiy.audio.say('Hello! this is Butlor ! How can I help you? ')
        while True:
            status_ui.status('ready')

            button.wait_for_press()

            status_ui.status('listening')
            print('Listening...')
            led.set_state(aiy.voicehat.LED.BLINK)
            text, audio = assistant.recognize()

            if text:
                print('You said "', text, '"')
                ok_google_cmd = re.match(ok_google_hotword, text)
                if ok_google_cmd:
                    print('Handled by Google Assitant "', text, '"')
                    aiy.audio.play_audio(audio)
                
                elif text == 'goodbye':
                    status_ui.status('stopping')
                    print('Bye!')
                    led.set_state(aiy.voicehat.LED.OFF)
                    aiy.audio.say(text)
                    break
                elif 'what is your IP' in text:
                    status_ui.status('stopping')
                    say_ip()
                elif 'shut down' in text:
                    status_ui.status('stopping')
                    power_off_pi()
                elif 'reboot' in text:
                    status_ui.status('stopping')
                    reboot_pi()

                #Butlor is invoked
                else:
                    #Stop VoiceHat from listening
                    status_ui.status('stopping')

                    #Handle the Command with Butlor
                    print(text)
                    #interact_butlor()
                    var_result = ask_butlor(text)
                    aiy.audio.say(var_result)
                    #Put the Google Assistant Back
                    print('Listening...')
                    status_ui.status('listening')
   


def power_off_pi():
    aiy.audio.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    aiy.audio.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('My IP address is %s' % ip_address.decode('utf-8'))





if __name__ == '__main__':
    main()
