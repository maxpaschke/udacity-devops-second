# Overview

<TODO: complete this with an overview of your project>

## Project Plan
[Trello Board](https://trello.com/b/EwIOnB9G/udacity-devops)

[Spreadsheet](./project-management/project-management.xlsx)

## Instructions

* Github Actions passing
  - Show Screenshot

<TODO:  
* Architectural Diagram (Shows how key parts of the system work)>

<TODO:  Instructions for running the Python project.  How could a user with no context run this project without asking you for any help.  Include screenshots with explicit steps to create that work. Be sure to at least include the following screenshots:

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
      sudo apt install python3.10.4
      sudo apt-get install python3.10.4-venv
      sudo apt-get install python3-pip
      sudo apt install python3-pip
      python3 —version
      pip —version 
      sudo apt-get install python3.10.4-distutils
      sudo apt-get -y install zip
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

* Create the webapp manually so it exists for further modification
    - Run the following in the cloud shell
    - ``` bash
      # adapt these links to suit your application
      git clone git@github.com:maxpaschke/udacity-devops-second.git
      cd udacity-devops-second/
      # Provide the web app name as a globally unique value. 
      az webapp up --name udacityWebApp123467 --resource-group Azuredevops --runtime "PYTHON:3.9"
      ```
    - You can now view the page under [https://udacitywebapp123467.azurewebsites.net/](https://udacitywebapp123467.azurewebsites.net/)


* Create a new pipeline and connect it
  - Goto `Pipelines` in the Azure Devops project
  - Select `Create`
    - In the Connect Wizard Select `Github`
    - Choose your repository
    - Select existing yaml file
      - Select `/.azure/azure-pipeline-self-hosted-agent.yml`
      - Adjust the webapp name to your new name


* Project running on Azure App Service

* Project cloned into Azure Cloud Shell

* Passing tests that are displayed after running the `make all` command from the `Makefile`

* Output of a test run

* Successful deploy of the project in Azure Pipelines.  [Note the official documentation should be referred to and double checked as you setup CI/CD](https://docs.microsoft.com/en-us/azure/devops/pipelines/ecosystems/python-webapp?view=azure-devops).

* Running Azure App Service from Azure Pipelines automatic deployment

* Successful prediction from deployed flask app in Azure Cloud Shell.  [Use this file as a template for the deployed prediction](https://github.com/udacity/nd082-Azure-Cloud-DevOps-Starter-Code/blob/master/C2-AgileDevelopmentwithAzure/project/starter_files/flask-sklearn/make_predict_azure_app.sh).
The output should look similar to this:

```bash
udacity@Azure:~$ ./make_predict_azure_app.sh
Port: 443
{"prediction":[20.35373177134412]}
```

* Output of streamed log files from deployed application

> 

## Enhancements

<TODO: A short description of how to improve the project in the future>

## Demo 

<TODO: Add link Screencast on YouTube>


