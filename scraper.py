import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_citations_needed_count(url):
    """
    Takes in a url string and returns an integer.

    According to the chrome tools inspection, the tag for 'citation needed' links on this page is:

    `<a href="/wiki/Wikipedia:Citation needed" title="Wikipedia:Citation needed">`

    Dig down and find these in the page and populate a list with the parent <p> tag content.

    Return the length of the list.

    Notes:
    - It looks like the class for all the content we want to check in the body of this page is in the tag called:

    `<div class="mw-parser-output">`

    Start by digging for this "mw-parser-output" tag and then finding the links we're looking for...

    `<a href="/wiki/Wikipedia:Citation needed" title="Wikipedia:Citation needed">`

    ...by finding all the tags and checking if they match our target tag and counting the matches.

    *** DON'T FORGET `_` BETWEEN WORDS IN HREF TAG STRING

    """
    target_parent_class = "mw-parser-output"

    # don't forget '_' in spaces for tag
    target_href = '/wiki/Wikipedia:Citation_needed'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find the target parent class
    results = soup.find(class_=target_parent_class)

    # Find all the target tags within the parent class
    anchors = results("a")

    # Put target tags into a list
    links = [anchor["href"] for anchor in anchors]
    # print(links)

    # confirm whether or not target tag is in results
    # print(target_href in links)

    # Frequency Check (geeksforgeeks.org; see README.md)
    # df1 = pd.Series(links).value_counts().sort_index().reset_index().reset_index(drop=True)

    df1 = pd.Series(links).value_counts()

    # df1.columns = ['Link', 'Frequency']

    # Find Frequency of target href
    print(df1[target_href])

    # print(f"The list frequency of elements is :\n {df1.to_string(index=True)}" )

    # Find Index of target href
    # print(df1[df1['Link'] == target_href])

    # print(df1['Frequency']['Link'][target_href])

    # return 'frequency' value at discovered index
    num_citations_needed = df1[target_href]

    return f"The number of citations needed is {num_citations_needed}."


print(get_citations_needed_count(("https://en.wikipedia.org/wiki/Table_tennis")))

