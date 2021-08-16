from quotebot import daily_quote, handle_msg, quote_generator

def handler(event,context):
    if "detail-type" in event:
        print("daily_quote")
        daily_quote(event)
    elif "key1" in event:
        print("debugging quote_generator")
        quote_generator()
    else:
        print("handle_msg")
        handle_msg(event)