import os
import logging
from flask import Flask, request, render_template, redirect, url_for, flash
import backtrader as bt
from strategies.basic_strategy import BasicStrategy
from strategies.load_data_yf import fetch_data_from_yahoo
from strategies.load_data_a_stock import fetch_a_stock_data
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/backtest', methods=['POST'])
def backtest():
    logging.debug("Starting backtest function")
    try:
        data_source = request.form['data_source']
        symbol = request.form['symbol'] if data_source == 'online' else request.form.get('symbol_a', '')
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        initial_cash = float(request.form['initial_cash'])
        commission_rate = float(request.form['commission_rate']) / 100

        logging.info(f"Form data received: data_source={data_source}, symbol={symbol}, start_date={start_date}, end_date={end_date}, initial_cash={initial_cash}")

        cerebro = bt.Cerebro()
        cerebro.addstrategy(BasicStrategy)
        cerebro.broker.setcash(initial_cash)
        cerebro.broker.setcommission(commission=commission_rate)
        
        if data_source == 'online':
            df = fetch_data_from_yahoo(symbol, start_date, end_date)
        elif data_source == 'a_stock':
            days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days
            df = fetch_a_stock_data(symbol, start_date, days)

        if df is not None and not df.empty:
            if not isinstance(df.index, pd.DatetimeIndex):
                logging.error("Data index is not a DatetimeIndex.")
                flash("Data format error: Index is not a DatetimeIndex.")
                return redirect(url_for('index'))
            data = bt.feeds.PandasData(dataname=df)
            cerebro.adddata(data)
            cerebro.run()
            fig_path = 'backtest_result.png'
            fig = cerebro.plot()[0][0]
            fig.savefig(os.path.join(app.static_folder, fig_path))  
            plt.close(fig)

            logging.info("Backtest completed successfully")
            flash('Backtest completed successfully.')
            return render_template('index.html', fig_path=fig_path)

        else:
            logging.error("Data loading failed or data is empty.")
            flash('Failed to fetch or process data.')
            return redirect(url_for('index'))

    except Exception as e:
        logging.error(f"Error in backtest function: {e}", exc_info=True)
        flash(f'An error occurred during backtesting: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
