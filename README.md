# Telegram Bot

This is a versatile teleautobot that brings a range of powerful functionalities  
## What Can It Actually Do?

- **Scrape Group Member Data:** Obtain valuable insights by scraping data about members in telegram groups.

- **Effortless Invitations:** Invite new members to your chats and channels seamlessly.

- **Smart Message Reactions:** Set up the bot to react to specific messages in your chat.

## Getting Started

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Download necessary libraries
4. Run setup.py via 'python setup.py'
5. Enter your phone number, api id, api hash (get this info on my.telegram.org)

```bash
pip install cprint telethon
git clone https://github.com/befragment/teleautobot.git
cd teleautobot
python setup.py
```

## Utils 

### Chat parser

- Scrapes information about users in telegram chat and arranges them into a csv file, containing following information:
username, user id, access hash, name, group, phone number

```bash
cd src
python setup.py
```

### Inviter
- Invites people to a certain channel/group/chat (all members are taken from members.csv)

```bash
cd src
python invite.py
```

### SmsBot

- SmsBot reacts on a certain user's keywords in the chat and sends him a message in private chat

```bash
cd src
python invite.py
```

#### How to use it?

- Open textfiles/messagebot directory, 2 files will appear there
- In chat_target.txt write ids of chats that bot should work on 
- In pre_restricted.txt write ids of users that should not receive messages from bot (e.g. admins of chats)
- Open textfiles/responses directory
- Add as many messages as you wish that bot should react on (e.g. response1.txt, response2.txt etc.)
- Run SmsBot

```bash
cd src
python smsbot.py
```

#### _How to handle response text files?_

- In the first line of text file write a keyword that bot should react on (keyword case is ignored)
- Split a keyword via ///
- Write a response to a keyword

#### _Example of response1.txt:_

hi <br>
/// <br>
Hi, there! Do you want to join our discord channel? Here's a link: <br>

- If any user send a message containing _hi_ keyword bot will automatically send him a message:<br>
_Hi, there! Do you want to join our discord channel? Here's a link:_

### For any issues contact me via discord: be.fragment