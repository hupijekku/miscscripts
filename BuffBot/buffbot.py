from bs4 import BeautifulSoup
import requests
def find_riven_buffs():
    file = None
    try:
        file = open("latest_patch.txt", "r")
    except IOError:
        print("No latest_patch.txt found")
        return
    patch_url = file.read()
    file.close()
    sp = patch_url.split("/")
    vsp = sp[len(sp)-2].split("-")
    vsp[2] = str(int(vsp[2])+1)
    temp = "-".join(vsp)
    sp[len(sp)-2] = temp
    minor_url = "/".join(sp)
    sauce = requests.get(minor_url)
    soup = BeautifulSoup(sauce.content, 'html.parser')
    if "Error" in str(soup.find_all('h1')[0]):
        print("No new patch to check for")
    else:
        file = open("latest_patch.txt", "w")
        file.write(minor_url)
        links = soup.find_all('a')
        for link in links:
            if "Riven" in str(link):
                parent = link.parent
                print("SUMMARY : {}".format(parent.p.text.strip()))
                changes = parent.findChildren('div', {'class': 'attribute-change'})
                attrib = ""
                before = ""
                after = ""
                for change in changes:
                    spans = change.findChildren('span', recursive=False)
                    for span in spans:
                        if "\"attribute\"" in str(span):
                            attrib = span.text.strip()
                        elif "before" in str(span):
                            before = span.text.strip()
                        elif "after" in str(span):
                            after = span.text.strip()   
                    print("{} : {} -> {}".format(attrib, before, after))
                break
if __name__ == '__main__':
    find_riven_buffs()