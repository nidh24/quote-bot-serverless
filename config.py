from datetime import time


class Config:

    morningQuoteTime = time(9, 0)
    # eveningQuoteTime = time(22, 0)

    EVENT_PAYLOAD_MORNING = {
          "version": "0",
          "id": "cdc73f9d-aea9-11e3-9d5a-835b769c0d9c",
          "detail-type": "Scheduled Event",
          "source": "aws.events",
          "account": "<account-id>",
          "time": "2021-07-29T04:30:00Z",
          "region": "us-east-1",
          "resources": [
            "arn:aws:events:us-east-1:<account-id>:rule/lambdaTriggerer"
          ],
          "detail": {}
        }

    quotesLocation = "quotebot/quotes/quotes_"
    CSV_EXT = ".csv"
    bucket_name = "telegrambots"
    table_name =  "quotebotUsers" # "test"
    commands = {
      "/help":"/help for command guide\n/start to start application\n/hello for formality \n/send for a quote",
      "/hello": "Hey there!",
      "default":"Hey! Didn't get that",
      "Exception":"Hey! Some error occured",
      "welcome":"Hey, {}! Welcome to the QuoteBot\nSend /help command for commands guide",
      "welcome_back": "Hi again, {} !\nSend /help command for commands guide"

    }