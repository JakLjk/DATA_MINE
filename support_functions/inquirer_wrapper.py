import inquirer

def list_options(options: dict, message = "Choose action to perform:"):
    """Accepts dict where key is option text to be displayed, 
    and value is function which will be executed
    if value is tuple with several values, first one of them will
    be regarded as function to be used, and the rest will be arguments"""
    questions = [
        inquirer.List(
                'inquiry',
                message=message,
                choices=list(options.keys()),
            ),]          
    answers = inquirer.prompt(questions)

    values_passed = list(options.values())[0]
    
    if  values_passed is None:
        pass
    if isinstance(values_passed, tuple):
        options[answers['inquiry']][0](", ".join(str(x) for x in options[answers['inquiry']][1:]))
    else:
        options[answers['inquiry']]()
