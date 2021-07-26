import os
import pexpect
from pexpect import pxssh
import sys
import time
import re
# pretty.install()
# sys.path.append('/home/sahib/idp_chatbot')
from server_credentials import IP, SUDOPASSWORD, USERNAME, PASSWORD

# print(IP, USERNAME, PASSWORD)
ip = IP
username = USERNAME
pw = PASSWORD
spw = SUDOPASSWORD

s = pxssh.pxssh()
if not s.login (ip, username, pw):
    print("SSH session failed on login.")
    print(str(s))
else:
    print("SSH session login successful")
    print('-------------------------CHECKING RUNNING CONTAINERS-------------------------------')
    s.sendline ('sudo docker ps')
    s.sendline (pw)
    s.prompt()         # match the prompt
    output_of_docker_ps = s.before.decode("utf8")
    print(output_of_docker_ps)

    print('-------------------------FETCHING CONTAINER ID-------------------------------')
    s.sendline ("sudo docker ps | grep sahib-bot-idp:latest | awk '{ print $1 }'")
    s.prompt()  
    output_of_docker_ps_grep = s.before.decode("utf8")
    splitted_output = output_of_docker_ps_grep.split(' ')
    id = splitted_output[-1:][0]
    # print(id)
    id = re.sub(r'[^ \w\.]', '', id).lower()
    print(id)

    print('-------------------------STOPING CONTAINER USING CONTAINER ID-------------------------------')
    print(f"sudo docker stop {id}")
    s.sendline (f"sudo docker stop {id}")
    s.prompt()  
    output_of_docker_stop = s.before.decode("utf8")
    print("stoped container id", output_of_docker_stop)

    print('-------------------------TO CHECK THE IMAGE ID\'S-------------------------------')
    s.sendline ("sudo docker image ls")
    s.prompt()  
    output_of_docker_image_ls = s.before.decode("utf8")
    print(output_of_docker_image_ls)

    print('-------------------------FETCHING IMAGE ID-------------------------------')
    s.sendline ("sudo docker image ls | grep sahib-bot-idp | awk '{ print $3 }'")
    s.prompt()  
    output_of_docker_image_ls_grep = s.before.decode("utf8")
    splitted_output = output_of_docker_image_ls_grep.split(' ')
    image_id = splitted_output[-1:][0]
    # print(image_id)
    image_id = re.sub(r'[^ \w\.]', '', image_id).lower()
    print(image_id)

    print('-------------------------REMOVING IMAGE USING IMAGE ID-------------------------------')
    s.sendline (f"sudo docker rmi -f {image_id}")
    s.prompt()  
    output_of_docker_remove_image_id = s.before.decode("utf8")
    print(output_of_docker_remove_image_id)

    ###PRUNING
    print('-------------------------ALL SYSTEM PRUNE-------------------------------')
    s.sendline ("sudo docker system prune --all")
    s.sendline ("y")
    s.prompt()  
    output_of_docker_all_system_prune = s.before.decode("utf8")
    print(output_of_docker_all_system_prune)

    print('-------------------------VOLUME SYSTEM PRUNE-------------------------------')
    s.sendline ("sudo docker system prune -a --volumes")
    s.sendline ("y")
    s.prompt()  
    output_of_docker_volume_system_prune = s.before.decode("utf8")
    print(output_of_docker_volume_system_prune)

    print('-------------------------VOLUME PRUNE-------------------------------')
    s.sendline ("sudo docker volume prune -f")
    s.sendline ("y")
    s.prompt()  
    output_of_docker_volume_prune = s.before.decode("utf8")
    print(output_of_docker_volume_prune)

    print('-------------------------IMAGE PRUNE-------------------------------')
    s.sendline ("sudo docker image prune -a")
    s.sendline ("y")
    s.prompt()  
    output_of_docker_image_prune = s.before.decode("utf8")
    print(output_of_docker_image_prune)

    print('-------------------------DOING ls-------------------------------')
    s.sendline ("ls")
    s.prompt()  
    output_of_ls = s.before.decode("utf8")
    print(output_of_ls)

    print('-------------------------GOING IN idp-chat-------------------------------')
    s.sendline ("cd idp-chat")
    s.prompt()  
    output_of_cd_idp_chat = s.before.decode("utf8")
    print(output_of_cd_idp_chat)


    print('-------------------------GOING IN idp_chatbot-------------------------------')
    s.sendline ("cd idp_chatbot")
    s.prompt()  
    output_of_cd = s.before.decode("utf8")
    print(output_of_cd)

    print('-------------------------REMOVING FOLDERS-------------------------------')
    list_of_folders_to_be_removed = ['actions/', 'domain-grp/', 'data/']
    for itr in list_of_folders_to_be_removed:
        s.sendline (f"rm -r {itr}")
        s.prompt()  
    
    print('-------------------------REMOVING FILES-------------------------------')
    list_of_files_to_be_removed = ['config.yml', 'domain.yml']
    for itr in list_of_files_to_be_removed:
        s.sendline (f"rm -r {itr}")
        s.prompt()  

    print('-------------------------GOING IN MODELS-------------------------------')
    s.sendline ("cd models")
    s.prompt()  
    output_of_cd_models = s.before.decode("utf8")
    print(output_of_cd_models)


    print('-------------------------DOING ls-------------------------------')
    s.sendline ("ls")
    s.prompt()  
    output_of_ls_in_models = s.before.decode("utf8")
    print(output_of_ls_in_models)
    splitted_output = output_of_ls_in_models.split(' ')
    print(splitted_output)
    model_name = splitted_output[-1:][0]
    print('before cleaning', model_name)
    model_name = re.sub('ls', '', model_name).lower()
    model_name = re.sub(r'[^ \w\.]', '', model_name).lower()
    model_name = re.sub('0m', '', model_name).lower()
    model_name = re.sub('0131m', '', model_name).lower()
    model_name_start = model_name[:8]
    model_name_end = model_name[8:]
    model_name = model_name_start+'-'+model_name_end
    print('after cleaning', model_name)

    print('-------------------------removing model-------------------------------')
    print(f"rm -r {model_name}")
    s.sendline (f" sudo rm -r {model_name}")
    s.sendline (spw)
    s.prompt()  
    output_of_cd = s.before.decode("utf8")
    print(output_of_cd)

    s.logout()
    # s.close()
    print('------------------------SCP FOLDERS AND FILES')
    
    #SCP FOLDERS AND FILES
    os.system('scp -r actions/ chatbotadmin@20.198.96.248:/home/chatbotadmin/idp-chat/idp_chatbot')
    os.system('scp -r data/ chatbotadmin@20.198.96.248:/home/chatbotadmin/idp-chat/idp_chatbot')
    os.system('scp -r domain-grp/ chatbotadmin@20.198.96.248:/home/chatbotadmin/idp-chat/idp_chatbot')
    os.system('scp -r actions/ chatbotadmin@20.198.96.248:/home/chatbotadmin/idp-chat/idp_chatbot')
    os.system('scp config.yml/ chatbotadmin@20.198.96.248:/home/chatbotadmin/idp-chat/idp_chatbot')
    os.system('scp domain.yml/ chatbotadmin@20.198.96.248:/home/chatbotadmin/idp-chat/idp_chatbot')
    # ####os.system('scp 20210706-151341.tar.gz chatbotadmin@20.198.96.248:/home/chatbotadmin/idp-chat/idp_chatbot/models/')


# s1 = pxssh.pxssh()
# if not s1.login (ip, username, pw):
#     print("SSH session failed on login.")
#     print(str(s1))
# else:
#     print("SSH session login successful")
#     print('-------------------BUILDING DOCKER IMAGE------------------')
#     s1.sendline('sudo docker ps')
#     # s1.sendline ('sudo docker build -t sahib-bot-idp')
#     # s1.sendline (pw)
#     output_of_docker_build = s.before.decode("utf8")
#     print(output_of_docker_build)
#     # print('-------------------RUNNING DOCKER IMAGE------------------')
#     # s1.sendline ('docker run -d -p 5005:5005 sahib-bot-idp:latest')
#     # s.sendline (pw)
#     s1.logout()



