from currency import Currency
from flask import Flask, render_template, request

app = Flask(__name__)
currency = Currency()
currency.get_exchange_values()


@app.route('/')
def index():
    return render_template('index.html', content=currency.get_rates())


@app.route('/search')
def search():
    base_currency = request.args.get('base_currency').upper()
    quote_currency = request.args.get('quote_currency').upper()
    amount = request.args.get('amount')
    if base_currency == 'USD' and currency.currency_value(quote_currency):
        exchange_amount = currency.change_from_usd(quote_currency, amount)
    elif currency.currency_value(base_currency) and currency.currency_value(quote_currency):
        exchange_amount = currency.change_between_currencies(base_currency, quote_currency, amount)
    else:
        return render_template('search.html', content="")
    respond = [amount, base_currency, exchange_amount, quote_currency]
    return render_template('search.html', content=respond)


app.run(port=1123)