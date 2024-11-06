label start:

## Setup/Reset the scores and players

    default persistent.username = False
    $ score = 0
    $ player = 0

## Setup the username

    if not persistent.username:
        $ persistent.username = renpy.input("What's your username ?", length=12).strip()
        if not persistent.username:
            $ persistent.username = None

    if persistent.username == None:
        $ persistent.username = False
        jump start

    menu:
        "Your name is [persistent.username], right ?"
        "Yes":
            pass
        "No":
            $ persistent.username = False
            jump start


    menu:
        "Chose your number !"
        "Player 1":
            $ player = 1
            "You play now as the player 1"

        "Player 2":
            $ player = 2
            "You play now as the player 2"

        "Player 3":
            $ player = 3
            "You play now as the player 3"

label game:

    if player == 1:
        $ url = "https://discord.com/api/webhooks/(WebhookID1)"
    elif player == 2:
        $ url = "https://discord.com/api/webhooks/(WebhookID2)"
    elif player == 3:
        $ url = "https://discord.com/api/webhooks/(WebhookID3)"

## Add as much webhooks as you want ^ 


## Message sending the username and the score of the player
    $ message = persistent.username + " : " + str(score)

## The channel where the webhooks will send their messages
    $ channel_id = '[channel_id]'

## The authentification token needed to receive the messages
    $ auth_token = '[authentification token]'


## Sending, receiving and clearing old messages
    python:
        import requests

        def send_message(url, message):
            requests.post(url, data={"content": message})

        def retrieve_messages(channel_id, auth_token):
            headers = {
                'authorization': auth_token
            }
            r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers)
            return r.json()

        def delete_message(channel_id, message_id, auth_token):
            headers = {
                'authorization': auth_token
            }
            requests.delete(f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}', headers=headers)

        send_message(url, message)
        messages = retrieve_messages(channel_id, auth_token)

## Showing messages on screen

    screen discord_messages(messages):
        vbox:
            for message in messages:
                frame:
                    text message['content']

    show screen discord_messages(messages)

## Refreshing the messages

    python:
        for message in messages:
            delete_message(channel_id, message['id'], auth_token)

        messages = retrieve_messages(channel_id, auth_token)

## Random text to prevent infinite loop

    "Random text"

    jump game