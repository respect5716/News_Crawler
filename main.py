import os
import ray
import time
import dropbox
import schedule
from utils import *
from pdf import PDF

ray.init()
CONFIG = read_config()

def main():
    date = get_date()
    dbx = dropbox.Dropbox(CONFIG['DROPBOX_TOKEN'])
    
    for key, value in CONFIG['QUERY'].items():
        data = collect_news(value, date)
        pdf = PDF(f'{date}_{key}')
        pdf.write(data)
        
        with open(f'{date}_{key}.pdf', 'rb') as f:
            dbx.files_upload(f.read(), f'/news/{date}/{key}.pdf', mode=dropbox.files.WriteMode.overwrite)
        os.remove(f'{date}_{key}.pdf')

if __name__ == '__main__':
    if CONFIG['TIME'] == 'now':
        main()
    else:
        schedule.every().day.at(CONFIG['TIME']).do(main)
        while True:
            schedule.run_pending()
            time.sleep(10)