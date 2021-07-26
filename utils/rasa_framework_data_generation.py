'''
this script will generate retrieval intents and then make nlu and domain files
'''
import sys
sys.path.append('/home/bavalpreet/IDP/')
from utils.semi_automation_insertion import *
from utils.paraphraser_quillbot import *

#paraphraser driver funtion
def get_paraphrased_sentence(path_to_input_file, path_to_output_csv, path_to_output_xlsx):
    data = pd.read_csv(path_to_input_file)
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
    dic['question'] = question
    dic['variations'] = paraphrased_values
    df = pd.DataFrame(dic)
    df.to_csv(path_to_output_csv)
    df.to_excel(path_to_output_xlsx)

#Retrieval driver function
def get_retrieval_intents(path_to_output_csv):
    df = pd.read_csv(path_to_output_csv)
    list_of_ques = df['question']
    filter_sent = filter_stopword(list_of_ques)
    punc_removal = remove_punct(filter_sent)
    steming_sent = steming(punc_removal, 'faq-fel-b0/')

    dictionary = {}
    dictionary['intent'] = steming_sent
    dictionary['question'] = list(df['question'])
    dictionary['variation'] = list(df['variations'])
    dataframe = pd.DataFrame(dictionary)
    return dataframe

if __name__ == "__main__":
    #paraphrasing
    filebatch = 'fel-b0'
    path_to_input_file = '/home/bavalpreet/Documents/new-question-fel-b0.csv'
    path_to_output_csv = '/home/bavalpreet/IDP/generated_data/paraphrased_data/'+filebatch+'_paraphrased_file.csv'
    path_to_output_xlsx = '/home/bavalpreet/IDP/generated_data/paraphrased_data/'+filebatch+'_paraphrased_file.xlsx'
    get_paraphrased_sentence(path_to_input_file, path_to_output_csv, path_to_output_xlsx)

    #retrievals preparation
    dataframe = get_retrieval_intents(path_to_output_csv)
    
    #intermediate data format 
    path_to_csv = '/home/bavalpreet/IDP/generated_data/intermediate_data/'+filebatch+'_intermediate.csv'
    df = dataframe
    preparing_intermediate_output_for_nlu_and_domain_filegeneration(path_to_csv, df)
    
    #generating files
    path = path_to_csv
    create_files_path = '/home/bavalpreet/IDP/generated_data/semiautomation/'
    domain_file_name = '\domain'
    nlu_file_name = '\nlu'
    create_rasa_files(path, create_files_path, nlu_file_name, domain_file_name)
    # gsheetid = '1luFRpbX9a0DIwJ0vNIyVglcKb8TcyNaBHXFj-4TLYAc'
    # sheet_name = 'sheet1'
    # gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, sheet_name)
    # df = pd.read_csv(gsheet_url)
    # list_of_ques = list(df['question']) 