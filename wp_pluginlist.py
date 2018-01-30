from bs4 import BeautifulSoup
import requests


def main():
    WORDPRESS_PLUGIN_SEARCH="https://nl-be.wordpress.org/plugins/?s="
    OUTPUT_FILE="wp-pluginlist.txt"

    req = requests.get(WORDPRESS_PLUGIN_SEARCH)
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, "lxml")
        try:
            maxpage = int(str(soup.findAll("a", {"class": "page-numbers"})[1].string).replace(".", ""))
        except Exception as e:
            print("Something went wrong!")
            exit(1)
        page = 1
        plugins = []
        open(OUTPUT_FILE, 'w+').close()

        while page <= maxpage:
            file = open(OUTPUT_FILE, 'a+')
            print("Fetching page " + str(page))
            pageurl = "https://nl-be.wordpress.org/plugins/page/" + str(page) + "/?s"
            req = requests.get(pageurl)
            if req.status_code == 200:
                print("Got the page. Enumerating plugins... Found " + str(len(plugins)) + " plugins so far...")
                soup = BeautifulSoup(req.text, "lxml")
                bookmarks = soup.findAll("a", {"rel": "bookmark"})
                for bookmark in bookmarks:
                    if bookmark.nextSibling == None:
                        pluginurl = bookmark.attrs['href']
                        plugins.append(str(pluginurl).split('/')[4])
                        file.write(str(pluginurl).split('/')[4] + "\n")
                        pass
            page = page + 1
            file.close()

        print("Found " + str(maxpage) + " plugins! Output stored in " + str(OUTPUT_FILE))
        print("************************************************************************")


if __name__ == "__main__":
    main()