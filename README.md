[![Python application test with Github Actions](https://github.com/maxpaschke/udacity-devops-second/actions/workflows/pythonapp.yml/badge.svg)](https://github.com/maxpaschke/udacity-devops-second/actions/workflows/pythonapp.yml)

# Overview
This projects hosts a small website with an integrated webservice on azure. The website allows the user to send requests and receive data from a pretrained model of housing price data in Boston. The main goal of the project is to demonstrate a fully workin CI / CD environment with GitHub and Azure pipelines.

## Architecture
![Architecture Diagramm](/project-management/architecture.svg?raw=true "Architecture diagramm")

## Project Plan
[Trello Board](https://trello.com/b/EwIOnB9G/udacity-devops)

A project plan can be found under [Spreadsheet](./project-management/project-management.xlsx).

# Hello.py
## How to run it locally
- Make sure you forfill the following requirements
    - Python Version `3.7.9`
    - `Make` is installed
- Run `make all` to run install, test and lint.

### Local results
* Passing tests that are displayed after running the `make all` command from the `Makefile`
  * The `make all` result for hello.py should look something like this:
``` cmd
>>make all
pip install --upgrade pip &&\
              pip install -r requirements.txt
Requirement already satisfied: pip in c:\python379\lib\site-packages (22.1.2)
[...]
Requirement already satisfied: pyparsing!=3.0.5,>=2.0.2 in c:\python379\lib\site-packages (from packaging->pytest->-r requirements.txt (line 2)) (3.0.9)
pylint --disable=R,C hello.py

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)

python -m pytest -vv test_hello.py
======================================= test session starts ========================================
platform win32 -- Python 3.7.9, pytest-7.1.2, pluggy-1.0.0 -- C:\Python379\python.exe
cachedir: .pytest_cache
rootdir: C:\Workspace\udacity\github\udacity-devops-second\Hello
collected 1 item                                                                                     

test_hello.py::test_hello_subtract PASSED                                                     [100%]

======================================== 1 passed in 0.02s =========================================
```
* Output of a test run
``` cmd
>>make test
python -m pytest -vv test_hello.py
======================================= test session starts ========================================
platform win32 -- Python 3.7.9, pytest-7.1.2, pluggy-1.0.0 -- C:\Python379\python.exe
cachedir: .pytest_cache
rootdir: C:\Workspace\udacity\github\udacity-devops-second\Hello
collected 1 item

test_hello.py::test_hello_subtract PASSED                                                     [100%]

======================================== 1 passed in 0.03s =========================================
  ```



# Prediction Service
## How to run it locally
- Make sure you forfill the following requirements
    - Python Version `3.7.9`
    - `Make` is installed
- Run `make install` to install the dependencies
- Run the flask webserver with `python app.py`
- Run example predictions by running `make_prediction.sh` in another shell


## Setup in Azure
* Setup the cloud shell
  - Open the cloud shell from Azure Portal
  - Select "Bash" as input
  - Configure advanced options
  - Use new fileshare and new storage accounts if you have not created them already.
  - Run the following commands:
    - `ssh-keygen -t rsa`
    - `cat /home/odl_user/.ssh/id_rsa.pub`
    - Copy the output of the `cat` command. It should start with "rsa"
  - Go to [github.com/settings/keys](github.com/settings/keys)
  - Add the new SSH Key

* Setup the Azure Devops organisation
  - Login to Azure on the Azure Portal
  - Go to https://aex.dev.azure.com/
  - Enter your details and continue
  - Create new organisation
  - Goto Organization Settings >> Policies 
    - Enable public projects
  - Create a new project
    - Name the project `udacity-azure-devops`
  - Setup the service connection in the Project settings >> Service connection
    - `Create service connection`
    - Select `Azure resource manager` and then `Service Principal (manual)`
    - Enter the details from the Udacity cloud lab
    - Set `Allow access to all pipelines to true`
    - Get the subscription name from the azure portal
    - Name the service connection `AzureUdacity`

* Setup the github repo according to [udacity](https://learn.udacity.com/nanodegrees/nd082/parts/cd1806/lessons/a415f839-37b3-4c7c-9bed-dc9764c4a08d/concepts/445e5041-41ce-4b31-b8f6-5c023e36425f)

* Authorize the App in github
  - Go to the [github marketplace](https://github.com/marketplace/azure-pipelines) and install Azure pipelines to your account 
  - Go to your [Github](https://github.com/settings/installations) account settings
  - Allow the pipelines application Access to the desired repositories in your account by clicking `Configure` and changing the `Repository access` settings accordingly

* Create the Azure Pipeline Agent
  - Create a Personal Access Token (PAT)
    - Goto [Dev.azure.com](https://dev.azure.com/)
    - Select `Personal Access Tokens` from the user settings menu
    - Click `Create new Token`
      - Name it `PAT_udacity`
      - Give it `Full access`
      - Create it
      - Save the Token
  - Create the agent pool
    - Goto [Dev.azure.com](https://dev.azure.com/)
    - Project Settings >> Agent pools
      - `Add pool`
      - Type: `self-hosted`
      - Name: `myAgentPool`
      - Enable `Grant access permission to all pipelines`
  - Create a pipeline runner (Linux VM)
    - Create VM in azure portal according to the following specs:
  
  | field                | value                                             |
  | -------------------- | ------------------------------------------------- |
  | Subscription         | Choose existing                                   |
  | Resource group       | Choose existing, say Azuredevops                  |
  | Virtual machine name | myLinuxVM                                         |
  | Availability options | No infrastructure redundency required             |
  | Region               | Select the region same that of the resource group |
  | Image                | Ubuntu Server 20.04 LTS - Gen1                    |
  | Size                 | Standard_D1s_v2                                   |
  | Authentication type  | Password                                          |
  | Username             | devopsagent                                       |
  | Password             | DevOpsAgent@123                                   |
  | Public inbound ports | Allow selected ports                              |
  | Select inbound ports | SSH (22)                                          |

    - Configure the VM
      - Copy the Ip address from the resource view of the vm
      - Connect to the VM via Azure cloud shell
      - `ssh devopsagent@$VMIP$`, use your specific IP for the VM here.
      - Enter the password
      - Run the following
        ```bash
        sudo snap install docker
        # Check Python version because this agent will build your code
        python3 --version
        # Configure the devopsagent user to run docker
        sudo groupadd docker
        sudo usermod -aG docker $USER
        exit
        ```
      - Restart the VM from the portal
      - Connect again via ssh: `ssh devopsagent@$VMIP$`, use your specific IP for the VM here.
      - Run the following to configure the runner
        ``` bash
        # Download the agent
        curl -O https://vstsagentpackage.azureedge.net/agent/2.202.1/vsts-agent-linux-x64-2.202.1.tar.gz
        # Create the agent
        mkdir myagent && cd myagent
        tar zxvf ../vsts-agent-linux-x64-2.202.1.tar.gz
        # Configure the agent
        ./config.sh
        # Finish the setup
        sudo ./svc.sh install
        sudo ./svc.sh start
        ```
      - For configuration refer to the following:

      | field                        | value                                                                                                                                   |
      | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
      | Server URL                   | Provide your Azure DevOps organization URL. For example, https://dev.azure.com/organization-name or https://dev.azure.com/odluser193422 |
      | Authentication type          | [Press enter]                                                                                                                           |
      | Personal access token        | [Provide the PAT saved above]                                                                                                           |
      | Agent pool (enter the value) | Choose the one created above,   say myAgentPool                                                                                         |
      | Agent name                   | [Press enter]                                                                                                                           |
      | Work folder                  | [Press enter]                                                                                                                           |

      - Configure the python environment on the vm
      ``` bash
      sudo apt-get update
      sudo apt update
      sudo apt install software-properties-common
      sudo add-apt-repository ppa:deadsnakes/ppa
      sudo apt-get install python3.7
      sudo apt-get install python3.7-venv
      sudo apt-get install python3-pip
      sudo apt install python3-pip
      python3 —version
      pip —version 
      sudo apt-get install python3.7-distutils
      sudo apt install python3.7-distutils
      sudo apt-get -y install zip
      # Fix for pylint
      # Shows no output because the Path is not set explicitly
      which pylint
      pip show --files pylint
      # Shows Files:
      #  ../../../bin/epylint
      # ../../../bin/pylint
      echo $PATH
      export PATH=$HOME/.local/bin:$PATH
      echo $PATH
      which pylint
      ```
    - The server should show as online now in the agent pool

* Create the webapp manually so it exists for further modification by the pipeline
    - Run the following in the cloud shell
    - ``` bash
      # adapt these links to suit your application
      git clone git@github.com:maxpaschke/udacity-devops-second.git
      cd udacity-devops-second/
      # Provide the web app name as a globally unique value. 
      az webapp up --name udacityWebApp123467 --resource-group Azuredevops --runtime "PYTHON:3.7"
      ```
    - Alternatively you can run the `commands.sh` file.
    - You can now view the page under [https://udacitywebapp123467.azurewebsites.net/](https://udacitywebapp123467.azurewebsites.net/)

* Create a new pipeline and connect it
  - Goto `Pipelines` in the Azure Devops project
  - Select `Create`
    - In the Connect Wizard Select `Github`
    - Choose your repository
    - Select existing yaml file
      - Select `/.azure/azure-pipeline-self-hosted-agent.yml`
      - Adjust the webapp name to your new name

* Run a prediction from the cloud shell
    - Allow the file to be executed via `chmod +x make_predict_azure_app.sh`
    - Run it with `make_predict_azure_app.sh`

* Run load testing 
    - Run `locust --host 127.0.0.1:5000` to test against the local server
    - Run `locust --host https://udacitywebapp123467.azurewebsites.net/` to test against the website
    - Select the amount of users you want to simulate

## Results
* Passing tests that are displayed after running the `make all` command from the `Makefile`
   ![Pred Result](/screenshots/2_Run_make_all_pass_tests.png?raw=true "Pass all tests after running make all")
* Project running on Azure App Service
  ![Pred Result](/screenshots/7_running_in_the_service.png?raw=true "Running in the cloud service")
* Project cloned into Azure Cloud Shell
  ![Pred Result](/screenshots/1_Clone_Into_Cloudshell.png?raw=true "Sucessfully deployed with the azure pipeline")
* Github actions running
![Pred Result](/screenshots/6_GH_Success.png?raw=true "Sucessfully run GH actions")

* Successful deploy of the project in Azure Pipelines & Running Azure App Service from Azure Pipelines automatic deployment  [Note the official documentation should be referred to and double checked as you setup CI/CD](https://docs.microsoft.com/en-us/azure/devops/pipelines/ecosystems/python-webapp?view=azure-devops).
  * See the result here: 
![Pred Result](/screenshots/4_sucessfull_CD.png?raw=true "Sucessfully deployed with the azure pipeline")
![Pred Result](/screenshots/9_pipeline_deploy.png?raw=true "Sucessfully deployed with the azure pipeline")

* Successful prediction from deployed flask app in Azure Cloud Shell.
  - Output of the make_predict_azure_app.sh from the cloud shell:
  ``` bash
  odl_user@Azure:~/udacity-devops-second$ ./make_predict_azure_app.sh
  Port: 443
  {"prediction":[20.35373177134412]}
  ```
  ![Pred Result](/screenshots/8_Run_prediction_in_the_shell.png?raw=true "Prediction Result")

* Output of streamed log files from deployed application
  - Logs can be viewed from the cloud shell with `az webapp log tail --name udacityWebApp123467 --resource-group Azuredevops`
  - For an example see [./example_tailed_logs.txt](./example_tailed_logs.txt)

* Load testing results
    - Results:
  ![Load testing](/screenshots/10_load_testing.png?raw=true "Sucessfully deployed with the azure pipeline")
  ![Load testing](/screenshots/11_load_testing_charts.png?raw=true "Sucessfully deployed with the azure pipeline")

## Enhancements
- Full integration of the CD part into the github side, using less of azure pipelines. It could be possible to reuse the artifacts that get build in github actions to save computing time.
- Improved testing: Increase the number of local tests but also do end to end (E2E) tests on the deployed webapp as a final testing step.
- Add further linting and compliance checking applications in github: Improve the compliance of the application to rules and regulations by checking them automatically.
- Move to a branching model for feature development

## Demo 
You can find the demo on [Youtube](https://youtu.be/MLaFUDRmrRQ). 
The demo shows the project running on Azure and one full run of the CI/CD pipeline as well as a prediction run and the active logs.


