# INDIAN DATA PORTAL Chatbot

#### To train model locally
```
rasa train --domain domain-grp/

```
#### To talk to bot in shell
```
rasa shell

```

#### To see bot working locally with UI


``` 
rasa run -m models --enable-api --cors "*" 
```

If it gives error port 5005 already in use 
check with
1. ``` docker ps ```
    > if your conatiner is running if yes stop it 
    > and if no container is running and it is still saying the same.
 
2. ``` rasa run -m models --enable-api --cors "*" -p [ port-number ] ```
    > and also make sure that this port number is also present in IDP.html in **socketUrl** : [ ip-address ]: [ port-number ]


## To run Docker image of chatbot

> **you can replace sahib-bot-idp with your bot name**
```
docker build -t sahib-bot-idp . 

docker run -it  -p 5005:5005 sahib-bot-idp:latest
```

If it gives an error port 5005 already in use

1. ``` docker run -it  -p [ port-number]:5005 sahib-bot-idp:latest ```

This will map your localhost [ port-number ] to 5005 and that 5005 port is used by docker container
But make sure  that this port number is also present in IDP.html in **socketUrl** : [ localhost ]: [ port-number ]
#### To run chatbot in shell using docker container
```
docker run  -it --workdir /app sahib-bot-idp bash ./scripts/start_shell.sh

```
#### To stop Docker container
```
docker stop <container-id>
```

#### To remove docker image

```
docker image rm -f sahib-bot-idp:latest
```


## Problem we faced while connecting RASA X with Github

To connect rasa x to Github via UI RASA X expects files to be of same structure as we get after
```
rasa init
```

Prerequisites for making **build-domain.py** file 
```
pip3 install HiYaPyCo

```
Means it does not support multiple domain files 
But What we have done is we have written a script **build-domain.py** and gave it path of all domain files so what it does is it takes all domain files combines them to make **domain.yml** 
so that we can connect RASA X to github via UI.

Now whenever we make multiple domain files before every re training
run

```
python3 build-domain.py

rasa train

```

### No need of below command now

```
rasa train --domain domain-grp/

```

# To setup Rasa x on server


Use step 1,2,3,4 from below link

https://rasa.com/docs/rasa-x/installation-and-setup/install/docker-compose/


# Server

1. After connecting rasa x to github ( considering we have made file structure same as **rasa init**) because then only rasa x connects to github.

2. cd /etc/rasa/

3. ``` sudo docker-compose down ```

4. Make changes to **credentials.yml**

5. ``` sudo docker-compose up -d ```


6. Open the [ Ip-address ] your RASA x is working

# To connect Personal Website to Server using socket io

1. Made an Folder in server

2. Installed rasa (rasa 2.6.0)
    ```
    pip3 install -U pip
    pip3 install rasa
    ```

3. git pull from repo to get the latest code

4. ``` rasa train ```

5. Open html file where you embedded the script from [here](https://github.com/botfront/rasa-webchat)
    ( any html file that can be present locally can be used just make sure
        1. In socketUrl : [ ip-address]:5005 of server )

6. Make sure the port you are mentioning is open  ( from Server UI you can do this )
    ( In our case we had to manually to open port **5005 from Azure server** because rasa by default runs on port 5005 )
7. ``` rasa run -m models --enable-api --cors "*"  ```
    **or**
8. ``` docker build -t sahib-bot-idp . ```

8.a ``` docker run -it  -p 5005:5005 sahib-bot-idp:latest ``` 

# To stop the Rasa Server connected via socket io

1. ``` lsof -i:5005 ``` ( to see which service is running on port 5005 and what is the PID)

2. ``` 
    kill $(lsof -t -i:5005)

    or

    kill -9 $(lsof -t -i:5005)
    ```
# To stop Rasa X server

1. ``` cd /etc/rasa/  ```

2. ``` sudo docker-compose down ```



# SSL certificates

#### Install certbot
```
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install certbot
```
1. sudo certbot certonly -d  [ domain name ].

    1.a Example ---> 
    
    ``` sudo certbot certonly -d chatbot.idp.tatrasdata.com ```
2. ``` cd /etc/letsencrypt/archive/<domain name>/ ```

Copy the certificates files :- 
Example ( copying certificates from /etc to inside our chatbot)

3. ``` cp /etc/letsencrypt/archive/chatbot.idp.tatrasdata.com/ /home/idp-chat/idp_chatbot/certs ```

4. Give Permissions to files ( Go to path where they are copied in chatbot)

    ``` chmod +rwx cert1.pem fullchain1.pem privkey1.pem chain1.pem ```

5. Give access of running command to User

Example ---> 

``` sudo chown -R chatbotadmin . ``` 
( It means give running access to username =chatbotadmin)

Make changes to **HTML** we will run in Browser
set it's socketurl with DOMAIN NAME you BOUGHT

```  socketUrl: "https://chatbot.idp.tatrasdata.com:5005",```


6. Command to Run Chatbot having SSL 

``` rasa run --ssl-certificate ./certs/chatbot.idp.tatrasdata.com/cert1.pem --ssl-keyfile ./certs/chatbot.idp.tatrasdata.com/privkey1.pem -m models --enable-api --cors "*" ```


#  whenever any difficulty with No spca required

1. ``` sudo docker system prune --volumes -a ```

or 

2. ``` sudo docker system prune ```
## To do
1. Have to solve the issue of chatbot giving False Positives ( Menas correct answer for wrong answer)

2. Permission error ( How to save model after training from docker image itself --if possible )


# When RASA x doesn't gives response

1. ``` cd /etc/rasa ```
2. ``` sudo docker-compose down ```
3. ``` sudo docker-compose up ```

If you see this https://forum.rasa.com/t/the-answers-of-bot-dont-appear-on-rasa-x/41000/8


## First Option

1. ``` sudo docker system prune --all ```
2. ```  sudo docker system prune -a --volumes ```
3.  ``` sudo docker volume prune -f ```
4. ``` sudo docker image prune -a ```


fo any help related to above commands 
1. https://docs.docker.com/engine/reference/commandline/system_prune/
2. https://docs.docker.com/config/pruning/



### If Rasa X **fails to train** or **can't upload model**
CLear RAM

    1. ``` sync; echo 3 | sudo tee /proc/sys/vm/drop_caches ```

    2. sync; echo 2 | sudo tee /proc/sys/vm/drop_caches 

Now ``` sudo docker-compose down ```

and  then again   ``` sudo docker-compose up -d ```

# Whenver doing rasa training make sure  

1. You have added all **response selectors**
2. Made changes for those repsonse selectors in rules and config file
3. WHen we press **rasa train** make sure all **retrieval intents** are present 
#### Additional 
    TO check which files are consuming how much space 
    https://www.hostinger.in/tutorials/vps/how-to-check-and-manage-disk-space-via-terminal

Then you will have to give **More space to you VM**

