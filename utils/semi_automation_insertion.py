import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import nltk
nltk.download('punkt')
porter=PorterStemmer()
nltk.download('stopwords')

#FROM CLIENT INPUT TO PARTICULAR FORMAT

#filtering stopwords
def filter_stopword(list_of_ques):
  stop_words = set(stopwords.words('english'))
  filtered_sentence = []
  for sent in list_of_ques:
    word_tokens = word_tokenize(sent)
    # print('word_tokens',word_tokens)
    filtered_sent = [w for w in word_tokens if not w.lower() in stop_words]
    # print('filtered_sent',filtered_sent)
    filtered_sentence.append(" ".join(filtered_sent))
  return filtered_sentence

#removing punctuation
def remove_punct(filtered_sentence):
  punc_sentence = []
  for f_text in filtered_sentence:
    tokens = word_tokenize(f_text)
    # remove all tokens that are not alphabetic
    words = [word for word in tokens if word.isalpha()]
    # print(words)
    punc_sentence.append(" ".join(words))
  return punc_sentence

#stemming
def steming(punc_sentence, retrieval_name):
  stemmed_list = []
  #making retrievalintents
  name_of_retrieval = str(retrieval_name)
  # name_of_retrieval = 'faq-visualisation-b1/'
  def stemSentence(sentence):
      token_words=word_tokenize(sentence)
      token_words
      stem_sentence=[]
      for word in token_words:
          stem_sentence.append(porter.stem(word))
          # stem_sentence.append("")
      return "-".join(stem_sentence)

  for sent in punc_sentence:
    x = stemSentence(sent)
    y = name_of_retrieval+x
    stemmed_list.append(y)
  return stemmed_list

# after having retrievals we will prepare intermediate outputs
def pad_dict_list(dict_list, padel):
    lmax = 0
    for lname in dict_list.keys():
        lmax = max(lmax, len(dict_list[lname]))
    for lname in dict_list.keys():
        ll = len(dict_list[lname])
        if  ll < lmax:
            dict_list[lname] += [padel] * (lmax - ll)
    return dict_list

def preparing_intermediate_output_for_nlu_and_domain_filegeneration(path_to_csv, df):
  intent_list = list(df['intent'].unique())
  dic = {}
  for intent in intent_list:
    variation_list = list(df[df['intent'] == intent]['variation'])
    question_list = list(set(list(df[df['intent'] == intent]['question'])))
    print(question_list)
    dic[intent] = variation_list+question_list
  padel = 'xyz'
  pad_dict_list(dic, padel)
  data = pd.DataFrame(dic)
  df = data.replace(['xyz'],'')
  df.to_csv(path_to_csv)

'''
param: create_files_path - where we want to create the nlu and domain files
param: nlu_file_name
param: domain_file_name
'''
#GENERATING FILES
def create_rasa_files(path, create_files_path, nlu_file_name, domain_file_name, Nlu_file_flag = True, Domain_file_flag = True):
    
    #NLU FILE
    NLU_FILE_CREATION = Nlu_file_flag
    if(NLU_FILE_CREATION):
        df = pd.read_csv(r"{}".format(path))
        df = df.replace(np.nan, '', regex=True)
        file = open(create_files_path+'nlu'+nlu_file_name+'.yml',"w")
        df=df.drop('Unnamed: 0',axis=1)
        intents = list(df.columns)
        for item in intents:
            file.write("- intent: {intent_name}\n".format(intent_name=item))
            file.write("  examples: |"+'\n')
            for sent in df[item]:
                if sent != '':
                  file.write("    - {}\n".format(sent))
        file.close()


    #DOMAIN FILE
    DOMAIN_FILE_CREATION = Domain_file_flag
    if(DOMAIN_FILE_CREATION):
        file = open(create_files_path+domain_file_name+'.yml',"w")
        file.write("intents:\n")
        file.write("responses:\n")
        for intent_name in intents:
            file.write("    utter_{}:\n".format(intent_name))
            file.write('    - text:\n')
        file.write("actions: []\n")
        # for intent_name in intents:
        #     file.write("  - utter_{}\n".format(intent_name))
        file.write('forms: {}\n')
        file.write('e2e_actions: []\n')
        file.close()
    return None

if __name__ == '__main__':
    #retrievals preparation
    df = pd.read_csv('')
    list_of_ques = df['question']
    filter_sent = filter_stopword(list_of_ques)
    punc_removal = remove_punct(filter_sent)
    steming_sent = steming(punc_removal, 'faq-fel-b0/')

    dictionary = {}
    dictionary['intent'] = steming_sent
    dictionary['question'] = list(df['question'])
    dictionary['variation'] = list(df['variations'])
    dataframe = pd.DataFrame(dictionary)
    
    #intermediate data format
    # 
    path_to_csv = '/home/bavalpreet/IDP/generated_data/intermediate_data/intermediate.csv'
    df = dataframe
    preparing_intermediate_output_for_nlu_and_domain_filegeneration(path_to_csv, df)
    
    #generating files
    path = path_to_csv
    create_files_path = '/home/bavalpreet/IDP/generated_data/semiautomation/'
    domain_file_name = '\domain'
    nlu_file_name = '\nlu'
    create_rasa_files(path, create_files_path, nlu_file_name, domain_file_name)