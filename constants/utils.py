
import os
import configparser

def get_latest_file_name(directory):
    try:
        files = [f for f in os.listdir(directory)]
        if not files:
            return None
        files.sort()
        return files[-1]

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def get_username():
    config = configparser.ConfigParser()
    config.read('config.ini')

    return config.get('credentials', 'username')

if __name__ == "__main__":
    HEARTHSTONE_POWER_LOG_HOME_PATH = r"C:\Program Files (x86)\Hearthstone\Logs"
    a = HEARTHSTONE_POWER_LOG_HOME_PATH + "\\" + \
        get_latest_file_name(HEARTHSTONE_POWER_LOG_HOME_PATH) + "\Power.log"
    print(a)
    print(get_username())
