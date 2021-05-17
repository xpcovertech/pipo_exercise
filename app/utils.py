import re

def is_int(num):
    if num is None:
        raise TypeError
    if isinstance(num, bool):
        return False
    if not isinstance(num, int):
        return False
    else:
        return True

def is_string(string):
	if string is None:
		raise TypeError
	if not isinstance(string, str):
		return False
	if len(string) == 0:
		raise Exception
	else:
		return True

def isCpfValid(cpf):
    """
    Code written by Rafael Lobo:
    https://github.com/rafahlobo/cpfValidator 
    If cpf in the Brazilian format is valid, 
    it returns True, otherwise, it returns False. 
    """

    # Check if type is str
    if not isinstance(cpf,str):
        return False

    # Remove some unwanted characters
    cpf = re.sub("[^0-9]",'',cpf)
    
    # Verify if CPF number is equal
    if cpf=='00000000000' or cpf=='11111111111' or cpf=='22222222222' or cpf=='33333333333' or cpf=='44444444444' or cpf=='55555555555' or cpf=='66666666666' or cpf=='77777777777' or cpf=='88888888888' or cpf=='99999999999':
        return False

    # Checks if string has 11 characters
    if len(cpf) != 11:
        return False

    sum = 0
    weight = 10

    """ Calculating the first cpf check digit. """
    for n in range(9):
        sum = sum + int(cpf[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifyingDigit = 11 -  sum % 11

    if verifyingDigit > 9 :
        firstVerifyingDigit = 0
    else:
        firstVerifyingDigit = verifyingDigit

    """ Calculating the second check digit of cpf. """
    sum = 0
    weight = 11
    for n in range(10):
        sum = sum + int(cpf[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifyingDigit = 11 -  sum % 11

    if verifyingDigit > 9 :
        secondVerifyingDigit = 0
    else:
        secondVerifyingDigit = verifyingDigit

    if cpf[-2:] == "%s%s" % (firstVerifyingDigit,secondVerifyingDigit):
        return True
    return False

def get_header(session):
    """ Receives session (dict) generated at login and returns the header (dict) 
    that will be used across the website"""
    try: 
        header = {"name": session["name"],
                    "company": session["company"],
                    "admin": session["admin_name"],
                    "id": session["id"]}
    except:
        header = {"name": "",
                    "company": "",
                    "admin": "",
                    "id": ""}
    return header



## NOT TESTED ##
## NOT TESTED ##

def str_to_int(string):
    try:
        if isinstance(string, str):
            int_str = int(string)
            return int_str
        else:
            return 0
    except:
        return 0


def str_list_to_int(s_list):
    try:
        temp = []
        for s in s_list:
            if isinstance(s, str):
                temp.append(int(s))
            else:
                return None
        return temp
    except:
        return None




