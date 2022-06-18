import datetime
import time
from mercado_bitcoin.writers import DataWriter
from mercado_bitcoin.ingestors import DaySummaryIngestor
from schedule import repeat, every, run_pending


if __name__ == '__main__':
    day_summary_ingestor = DaySummaryIngestor(writer = DataWriter, coin = ['BTC','LTC','ETH'], default_start_date= datetime.date(2022,5,29))

    @repeat(every(1).seconds)
    def job():
        day_summary_ingestor.ingest()

    while True:
        run_pending()
        time.sleep(0.5)



