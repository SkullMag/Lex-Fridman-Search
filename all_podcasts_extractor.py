from selenium import webdriver


if __name__ == "__main__":
    driver = webdriver.Safari() 
    driver.get("https://lexfridman.com/podcast/")
    driver.find_element_by_css_selector("button[data-sort-value='all']").click()
    with open("podcasts.html", "w") as f:
        f.write(driver.page_source)
    driver.close()

