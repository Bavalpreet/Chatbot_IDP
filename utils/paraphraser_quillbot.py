
import requests
import itertools
import time
import pandas as pd
from tqdm import tqdm


# preparing string in specific format
def text_formatter(text):
  text_ = text.split(' ')
  modified_text = '%20'.join(text_)
  return modified_text


# hitting api for paraphraased questions
def paraphrase(text):
  parameters = {'text':text,
                'strength':'2',
                'autoflip':'false',
                'wikify':'false',
                'fthresh':'-1',
                'inputLang':'en',
                'quoteIndex':'-1'
                }
  url = "https://rest.quillbot.com/api/paraphraser/single-paraphrase/2?text="+parameters['text']+"&strength="+parameters['strength']+\
        "&autoflip="+parameters['autoflip']+"&wikify="+parameters['wikify']+"&fthresh="+parameters['fthresh']+\
        "&inputLang="+parameters['inputLang']+"&quoteIndex="+parameters['quoteIndex']

  payload={}
  headers = {
    'Cookie': '_gcl_au=1.1.576355756.1624427747; user_status=not registered; _gid=GA1.2.1251542784.1625914978; connect.sid=s%3ACQ3o7CIGKgWgBhfJS1QZesjN6FRw_TY0.kfq5dTmQDwN0UvFfMw%2BWbuR89uhourvCYVLn5F48XbI; qdid=7baf7512-3748-4bca-9de5-146acdd2b035; _ga_KQNKKHJ2B0=GS1.1.1625991937.22.1.1625994261.0; _ga=GA1.2.1972348962.1624427747; _gat=1; _uetsid=62f59600e16e11eba371c309b0324956; _uetvid=a7c362f0d3e711ebb514a7188af80e73; amp_6e403e=5M-q57lIAhODCdcd1rMKXT...1faaai0sr.1faacv274.4b6.1.4b7'
  }
  try:
      
    response = requests.request("GET", url, headers=headers, data=payload)
  except Exception as e:
    print(e)
  time.sleep(2.5)
  return response.json()


# getting sentences from api json response
def get_sent_from_json(response):
  list_of_data = response['data']
  # print(list_of_data[0].keys())
  list_of_alternatives = [ele['alt'] for ele in list_of_data[0]['paras_3']]
  return list_of_alternatives


if __name__ == "__main__":
  file_and_batch = 'viz_b3'
  data = pd.read_csv('/home/bavalpreet/Documents/new-question-viz-b3.csv')
  sentences = list(data['questions'].values)
  question = []
  paraphrased_values = []
  
  for sent in tqdm(sentences):
    text = text_formatter(sent)
    response = paraphrase(text)
    result = get_sent_from_json(response)
    text_itr2 = [text_formatter(ele) for ele in result]
    response_itr2 = [paraphrase(ele) for ele in text_itr2]
    result_itr2 = [get_sent_from_json(itr) for itr in response_itr2]
    flatten_result_itr2 = list(itertools.chain(*result_itr2))
    text_itr3 = [text_formatter(ele) for ele in flatten_result_itr2]
    response_itr3 = [paraphrase(ele) for ele in text_itr3]
    result_itr3 = [get_sent_from_json(itr) for itr in response_itr3]
    flatten_result_itr3 = list(itertools.chain(*result_itr3))
    list_of_flatten_all_iters = list(set(result+flatten_result_itr2+flatten_result_itr3))
    # flatten_all_iters = list(itertools.chain(*list_of_flatten_all_iters))
    for ele in list_of_flatten_all_iters:
      paraphrased_values.append(ele)
    for itr in range(0,len(list(set(result+flatten_result_itr2+flatten_result_itr3)))):
      question.append(sent)
    print(len(question), len(list(set(result+flatten_result_itr2+flatten_result_itr3))))
  print(len(question), len(paraphrased_values))
  dic = {}
  dic['sentence'] = question
  dic['variation'] = paraphrased_values
  df = pd.DataFrame(dic)
  df.to_csv('/home/bavalpreet/IDP/generated_data/paraphrased_data/'+file_and_batch+'_paraphrased_file.csv')
  df.to_excel('/home/bavalpreet/IDP/generated_data/paraphrased_data/'+file_and_batch+'_paraphrased_file.xlsx')
  print('hi')
