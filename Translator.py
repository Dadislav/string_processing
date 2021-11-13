from TooShortException import TooLongCommentException, TooLongNicknameException, PossibleSqlInjection, TooShortCommentException, TooShortNicknameException, NotStringInInput
import re
import numpy as np
import xml.etree.ElementTree as elt


class Translate:
    try:
        def to_sql(self, nickname, comment):
            help = '"'
            backslash = r'\\'
            if type(nickname) is not str or type(comment) is not str:
                raise NotStringInInput
            if len(nickname) < 1:
                raise TooShortNicknameException
            if len(comment) < 2:
                raise TooShortCommentException
            if len(nickname) > 100:
                raise TooLongNicknameException
            if len(comment) > 250:
                raise TooLongCommentException

            # 7.4. SQL Injection
            if x := re.search(f"({help})|{backslash}|/|;| drop | select | insert | alter ", nickname, re.IGNORECASE) or re.search(f"({help})|{backslash}|/|;| drop | select | insert | alter ", comment, re.IGNORECASE):
                print(x)
                raise PossibleSqlInjection

            # 7.2. Cenzura
            # pro Ondrej|Ondra Mandik
            if x := re.search("^(ondra|ond(r|ř)ej) (mand(i|í)k)$", nickname, re.IGNORECASE):
                found_name = ''
                for i in range(x.start(), len(nickname), 1):
                    found_name += nickname[i]
                nickname = nickname.replace(found_name, '[AUTOMATICKY CENZUROVÁNO]')

            elif x := re.search("(mand(i|í)k)$", nickname, re.IGNORECASE):
                found_name = ''
                for i in range(x.start(), len(nickname), 1):
                    found_name += nickname[i]
                nickname = nickname.replace(found_name, '[AUTOMATICKY CENZUROVÁNO]')

            # pro Alena|Aja Reichlova
            if x := re.search("^(alena|(a|á)ja) (reichlov(a|á))$", nickname, re.IGNORECASE):
                found_name = ''
                for i in range(x.start(), len(nickname), 1):
                    found_name += nickname[i]
                nickname = nickname.replace(found_name, '[AUTOMATICKY CENZUROVÁNO]')

            elif x := re.search("reichlov(a|á)$", nickname, re.IGNORECASE):
                found_name = ''
                for i in range(x.start(), len(nickname), 1):
                    found_name += nickname[i]
                nickname = nickname.replace(found_name, '[AUTOMATICKY CENZUROVÁNO]')

            # pro Jára|Jaroslav Cimrman
            if x := re.search('^(j(á|a)ra) (cimrman)$', nickname, re.IGNORECASE):
                found_name = ''
                for i in range(x.start(), len(nickname), 1):
                    found_name += nickname[i]
                nickname = nickname.replace(found_name, '[AUTOMATICKY CENZUROVÁNO]')

            elif x := re.search("cimrman$", nickname, re.IGNORECASE):
                found_name = ''
                for i in range(x.start(), len(nickname), 1):
                    found_name += nickname[i]
                nickname = nickname.replace(found_name, '[AUTOMATICKY CENZUROVÁNO]')

            return f'INSERT INTO PRISPEVEK (AUTHOR, TEXT) VALUES ({str(nickname)!r}, {str(comment)!r})'

    except TooShortNicknameException:
        print('moc kratke nebo zadne jmeno')
    except TooShortCommentException:
        print('moc kratky komentar nebo zadny')
    except NotStringInInput:
        print('spatny input, input musi byt v textovem retezci')
    except PossibleSqlInjection:
        print('je mozne ze vas nickname/ komentar obsahuje sql injection')
    except TooLongCommentException:
        print('vas komentar je moc dlouhy')
    except TooLongNicknameException:
        print('vas nickname je moc dlouhy')

        # 7.3 Analýza textu

    def word_counter(self, sentence):
        word_list = sentence.split()
        sent_length = 0

        if x := re.search('[a-z]+’[a-z]+', sentence, re.IGNORECASE):
            arr = np.array(x.span())
            found_name = ''
            for i in range(arr[0], arr[1], 1):
                found_name += sentence[i]
            sent_length += 2
            word_list.remove(found_name)

        if x := re.search('[a-z]+ [1-3]{1}[0-9]{1}[a-z]{2} [1-2][0][0-2][0-9]', sentence, re.IGNORECASE):
            arr = np.array(x.span())
            found_name = ''
            for i in range(arr[0], arr[1], 1):
                found_name += sentence[i]
            sent_length += 1
            found_list = found_name.split()
            for i in range(len(found_list)):
                word_list.remove(found_list[i])

        if x := re.search('[0-9]+ ([A-Z]+,) ([A-Z]+( )*)', sentence, re.IGNORECASE):
            arr = np.array(x.span())
            found_name = ''
            for i in range(arr[0], arr[1], 1):
                found_name += sentence[i]
            sent_length += 1
            found_list = found_name.split()
            for i in range(len(found_list)):
                word_list.remove(found_list[i])

        for i in word_list:
            sent_length += 1

        return sent_length

    # 7.5. Parsování XML
    def person_search(self, xml):
        x = elt.parse(xml)
        name = ''
        a = elt.tostring(x.getroot(), encoding='unicode')
        if x := re.findall('<ns2:J>(.*)</ns2:J>\n<ns2:P>(.*)</ns2:P>', a):
            for osoba in x:
                arr = np.array(osoba)
                name += arr[0] + " "
                name += arr[1] + "\n"
            return name

    # 7.6. Passsword policy
    def password_policy_check(self, username, password):
        final_text = ''
        comb_list = []
        for k in range(len(username)):
            for i in range(k + 3, len(username) + 1):
                comb_list.append(username[k:i])

        if x := re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*(/|!|@|#|%))\S{10,}$', password):
            for a in comb_list:
                if re.search(a, password):
                    final_text = 'vase heslo nesplnuje policy'
                    break
                else:
                    final_text = f'your password: {password}, passes the check'
        else:
            final_text = 'vase heslo nesplnuje policy'
        return final_text
