from selenium import webdriver
from json import load

def get_driver(config):
    BROWSER_PATH = config["BROWSER_PATH"] 
    OPTIONS = webdriver.ChromeOptions()
    OPTIONS.binary_location = BROWSER_PATH
    return webdriver.Chrome(options=OPTIONS)

def main():
    with open("config.json", 'r') as file:
        config = load(file)
    
    # Get driver
    driver = get_driver(config)

    # Open episode directory
    driver.get("https://theengineeringcommons.com/episodes-2/")
    

    # Open each episode link
    # Save each download link to a text file
    # Open each associated download link

    driver.quit()

if __name__ == "__main__":
    main()