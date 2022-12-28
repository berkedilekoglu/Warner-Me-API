# Warner-Me API

> Warner-Me is a Rest API that sends a notification via Telegram to programmers who are waiting for the code they ran to finish. Therefore, you can learn your code status and your results.

## Requirements

> requirements.txt file contains all the necessary packages for the development of Warner-Me API.

> You just need to requests package for usage.

## Usage

> Firstly you need to register in Warner-Me database by using Telegram Bot.

> You can find our bot by searching it 'WARNMEE_BOT' or by QR Code

<img src="https://github.com/berkedilekoglu/berkedilekoglu.github.io/blob/master/imgs/qr_code.png" width="250" height="350">

> Then you can type /help to get detailed information

> /register you can register in Warner-Me database. Your code status is inactive and your results are empty by default.

> /id you can learn your id

> Once you learnt the id, you can use Warner-Me Api

```python
from warnerme_client.main import WarnerMe

warner = WarnerMe(user_id) # user_id is the id that was taken by Warner-Me Telegram Bot.
print(warner.status()) # You can get current information
warner.activate(status=False) # Activate the warner before your code. It also prints the status by default (status=True). Set status=False if no need to print the status.

"""
YOUR CODE HERE:

For instance model.fit() or any other script.
"""

warner.deactivate(status=False, result_str = "acc:0.9, f1:0.6") # Deactivate and update the status. If you don't want to be reported automatically on Telegram, set post_telegram = False, it's True by default.
```

> Warner-Me provides 2 information areas for you: CodeStatus and results. These can be used in any way you like. Both fields should be strings, and they should be used inside a dictionary as shown in the example.

```python
requests.post(BASE + "warnMe/your_id", {'codeStatus':'SOME STRING HERE', 'results':'SOME STRING HERE'}) #You can write what ever you want for your codeStatus and results.
```

> You can use other languages than Python by using same pattern.
