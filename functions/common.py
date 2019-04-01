#!/usr/bin/python3

import gitlab,click,os,ast

def defineGitlabHost(url): # Simple checker for host
    if url:
        return url
    else:
        return os.environ.get('PGCLI_URL')


def defineGitlabToken(token): # Simple checker for private token
    if token:
        return token
    else:
        return os.environ.get('PGCLI_TOKEN')


def performConnection(url, token): # Gitlab connection function (url + private token)
    connection_host = defineGitlabHost(url)
    connection_token = defineGitlabToken(token)
    return gitlab.Gitlab(connection_host, private_token=connection_token)


def transformToDict(dict_string): # Transform python-gitlab's result to Python Dictionary
    return ast.literal_eval(str(dict_string).split(' => ')[1])


def validateProjectName(project_name):
    if(len(project_name.split('/')) != 2):
        clickOutputMessage('ERROR', 'red', 'The project name should be defined as <group>/<project_name>.')
        return False
    else:
        return True

def askForConfirmation(auto_confirm, confirmation_string, cancel_string, status='TERMINATING...'):
    if not auto_confirm:
        confirmation = input(confirmation_string)
        if confirmation != 'yes':
            print('--------------------------------------------------------------------------------------')
            clickOutputMessage(status, 'red', cancel_string)
            return False
        else:
            return True
    else:
        return True

def clickOutputMessage(status, color, string):
    click.echo('[' + click.style(status, fg=color) + '] ' + string)

def clickOutputHeader(action, object_kind, gl_object_name, gl_from = ''):
    if action == 'Creating':
        color = 'green'
    elif action == 'Updating':
        color = 'yellow'
    elif action == 'Deleting':
        color = 'red'
    else:
        color = 'yellow'
    
    if gl_from != '':
        additional_string = 'from <' + click.style(gl_from, fg='yellow') + '>'
    else:
        additional_string = ''

    print('======================================================================================')
    print()
    click.echo('>>>  [' + click.style(action, fg=color) + '] ' + object_kind + ' <' + click.style(gl_object_name, fg='yellow') + '> ' + additional_string + ' ... <<<')
    print()

    print('======================================================================================')
