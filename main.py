from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
from json import load

def get_driver(config):
    BROWSER_PATH = config["BROWSER_PATH"] 
    OPTIONS = webdriver.ChromeOptions()
    OPTIONS.binary_location = BROWSER_PATH
    return webdriver.Chrome(options=OPTIONS)

def main():
    with open("config.json", 'r') as file:
        config = load(file)

    driver = get_driver(config)

    driver.get("https://theengineeringcommons.com/episodes-2/")

    ul_element = driver.find_element(By.CSS_SELECTOR, "ul.tocc_expandable") 
    li_elements = ul_element.find_elements(By.CSS_SELECTOR, "li.tocc_blog_post")

    with open(config["EPISODE_LINK_PATH"], "r+") as episode_link_file:
        content = episode_link_file.read()
        if not content: # if it's an empty file
            for li_element in li_elements:
                name = li_element.find_element(By.CSS_SELECTOR, "a.tocc_blog_post_title").text
                link = li_element.find_element(By.CSS_SELECTOR, "a.tocc_blog_post_title").get_attribute("href")
                episode_link_file.write(link + '\n')
                print(f"[+] Saved {name} to {config['EPISODE_LINK_PATH']}")
        else:
            print("[-] Skipped getting episode links")    
        
        episode_link_file.seek(0) # Move cursor to the top 

        with open(config["EPISODE_DOWNLOAD_LINK_PATH"], "r+") as download_links_file:
            content = download_links_file.read()
            if not content:
                for episode_link in episode_link_file:
                    episode_link = episode_link.strip()
                    driver.execute_script(f'window.open("{episode_link}","_blank");')
                    driver.switch_to.window(driver.window_handles[-1])

                    try:
                        download_link = driver.find_element(By.CSS_SELECTOR, "a.powerpress_link_d").get_attribute("href")
                        download_links_file.write(download_link + '\n')
                        print(f"[+] Saved {download_link} to {config['EPISODE_DOWNLOAD_LINK_PATH']}")
                    except:
                        print("[-] Dowload link not found on this page")             

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
            else:
                print("[-] Skipped getting download links")
            
            download_links_file.seek(0)

            for download_link in download_links_file:
                download_link = download_link.strip()
                urllib.request.urlretrieve(download_link, f"{config['MP3_OUTPUT_PATH']}\\{download_link.split('/')[-1]}")
                print(f"[+] Downloaded {download_link} to {config['MP3_OUTPUT_PATH']}\\{download_link.split('/')[-1]}")

    driver.quit()

if __name__ == "__main__":
    main()