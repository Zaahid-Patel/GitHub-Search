import urllib.parse
import requests
from bs4 import BeautifulSoup
from github import Github
import re


def scrape_github(search_term, num_pages=1):
    param = urllib.parse.quote(search_term)
    URL = 'https://github.com/search?q=%s&type=' % param
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    name_of_keys = ["repo_name", "description", "tags", "num_stars",
                    "language", "license", "last_updated", "num_issues"]
    if str(soup.findAll('a', class_='v-align-middle')).count('href') == 0:
        num_of_repos = 0
    else:
        num_of_repos = str(soup.findAll(
            'a', class_='v-align-middle')).count('href')

    list_of_dict = [{key: None for key in name_of_keys}
                    for x in range(num_of_repos)]

    x = 0
    for name in soup.findAll('a', class_='v-align-middle'):
        list_of_dict[x].update({"repo_name": name.get('href').strip()})
        x = x+1

    x = 0
    for description in soup.findAll('div', class_='mt-n1'):
        if str(description).count('mb-1') == 0:
            list_of_dict[x].update({"description": None})
        else:
            for temp1 in description.findAll('p', class_='mb-1'):
                list_of_dict[x].update({"description": temp1.text.strip()})
        x = x+1

    x = 0
    tag_list_temp = []
    for tags in soup.findAll('div', class_='mt-n1'):
        if str(tags).count('mb-1') == 0:
            list_of_dict[x].update({"tags": None})
        else:
            for temp1 in tags.findAll('a', class_='topic-tag'):
                tag_list_temp.append(temp1.text.strip())
            list_of_dict[x].update({"tags": tag_list_temp})
            tag_list_temp = []
        x = x+1

    x = 0
    for num_stars in soup.findAll('div', class_='d-flex flex-wrap text-small color-text-secondary'):
        if str(num_stars).count('mr-3') == 1:
            list_of_dict[x].update({"num_stars": None})
        else:
            for temp1 in num_stars.findAll('a', class_='Link--muted'):
                temp2 = str(num_stars.find('a', class_='Link--muted f6'))
                if str(temp1).strip() == temp2.strip():
                    list_of_dict[x].update(
                        {"num_issues": int(re.search(r'\d+', temp1.text.strip()).group())})
                else:
                    list_of_dict[x].update({"num_stars": temp1.text.strip()})
        x = x+1

    x = 0
    for language in soup.findAll('div', class_='mt-n1'):
        if str(language).count('programmingLanguage') == 0:
            list_of_dict[x].update({"language": None})
        else:
            for temp1 in language.findAll('span', itemprop='programmingLanguage'):
                list_of_dict[x].update({"language": temp1.text.strip()})
        x = x+1

    x = 0
    for licence in soup.findAll('div', class_='mt-n1'):
        if str(licence).count('license') == 0:
            list_of_dict[x].update({"license": None})
        else:
            for temp1 in licence.findAll('div', class_='mr-3'):
                if str(temp1).count('license') == 1:
                    list_of_dict[x].update({"license": temp1.text.strip()})
        x = x+1

    x = 0
    for last_updated in soup.findAll('relative-time'):
        if last_updated.has_attr('datetime'):
            list_of_dict[x].update({"last_updated": last_updated['datetime']})
        x = x+1

    return list_of_dict



def github_api(search_term, num_pages=1):
    search = Github().search_repositories("%s in:name,description" %search_term)
    name_of_keys = ["repo_name", "description", "num_stars",
                    "language", "license", "last_updated", "has_issues"]
    
    num_of_repos = 0
    for i, repo in enumerate(search):
        num_of_repos = num_of_repos + 1
        if i == 9:
            break

    list_of_dict = [{key: None for key in name_of_keys}
                    for x in range(num_of_repos)]

    for i, repo in enumerate(search):
        list_of_dict[i].update({"repo_name": repo.full_name})
        list_of_dict[i].update({"description": repo.description})
        list_of_dict[i].update({"num_stars": int(repo.stargazers_count)})
        list_of_dict[i].update({"language": repo.language})
        try:
            if repo.get_license().license.name == "Other":
                list_of_dict[i].update({"license": None})
            else:
                list_of_dict[i].update({"license": repo.get_license().license.name})
        except:
            pass
        list_of_dict[i].update({"last_updated": repo.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ")})
        list_of_dict[i].update({"has_issues": repo.has_issues})
        if i == 9:
            break

    return list_of_dict