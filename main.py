#7.1. Parse to SQL
import Translator



nick = 'Dalibor Andrs'
username = 'Dalibor'
comm = f'fff'
#print(tr.to_sql(nick,'\'); select 1; --'))
sentence = 'if you’re going to Prague, visit 25 Londynska, Praha because it is really nice place.'

# print(tr.word_counter(sentence))
tr = Translator.Translate()

# print(tr.to_sql(nick,comm))
file = 'text.xml'
# print(tr.person_search(file))
password = 'ea2Ealwabrawdi#'
print(tr.password_policy_check(username,password))
