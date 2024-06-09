import urllib.parse
import requests
from bs4 import BeautifulSoup
from LLM_Processing import llm_processing
from markdown import markdown


def fetch_arxiv_results(subject, query):
    
    query_str = " ".join(query)
    print("subject, query: ", subject, query)

    params = {
        "advanced": "",
        "terms-0-operator": "AND",
        "terms-0-term": query_str,
        "terms-0-field": "title",
        "date-filter_by": "all_dates",
        "date-year": "",
        "date-from_date": "",
        "date-to_date": "",
        "date-date_type": "submitted_date",
        "abstracts": "show",
        "size": "50",  # Limit results to 10
        "classification-include_cross_list": "include",
        "order": "-announced_date_first",
    }


    # Add the subject to params
    params.update(subject)

    url = f"https://arxiv.org/search/advanced?"
    url += urllib.parse.urlencode(params)

    response = requests.get(url)
    #print("url: ", url)
    #print("response: ", dir(response), response.reason)

    if response.status_code == 200:
        response_content = response.content
        soup = BeautifulSoup(response_content, 'html.parser')

        results = []
        abstracts = []
        # Extract titles and abstracts
        for result in soup.find_all('li', class_='arxiv-result'):
            title = result.find('p', class_='title').get_text(strip=True)
            abstract = result.find('span', class_='abstract-short').get_text(strip=True)
            results.append({'title': title, 'abstract': abstract})
            abstracts.append(abstract)

        aggregated_summary = llm_processing(abstracts).content
        #print("aggregated_summary: ", dir(aggregated_summary))
        # Convert Markdown to HTML
        html_summary = markdown(aggregated_summary)
        #print("html_summary: ", html_summary)

        return html_summary
    else:
        return f"Failed to retrieve content: {response.status_code}"
