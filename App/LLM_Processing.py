# Import libraries

import os
from openai import OpenAI

from dotenv import load_dotenv


def llm_processing(abstracts):
    print("Started LLM:")
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv('OPEN_AI_KEY')
    )
    
    # Aggregate abstracts
    aggregated_input = " ".join(abstracts)
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Present the information of Abstracts as if you were a science news reporter. Make it as brief as possible, focusing on what researchers might find interesting to research next based on this. Present all in markdown format."},
            {"role": "user", "content": aggregated_input}
        ]
    )

    aggregated_summary = completion.choices[0].message
    return aggregated_summary
    # else:
    # print("Failed to retrieve content:", response.status_code)

