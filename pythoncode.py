
import pandas as pd 
f = open("am_am.dump", "r")

N = 1000000000  #1 billion 

read = f.read(N)

headers = read[1003:3140]
headerslist = headers.split('\n')[1:-4] 
headerslist = [h.split("`")[1] for h in headerslist]
df = pd.DataFrame(columns = headerslist)  #48 columns data frame 



def comma_cram(ls):
    k = len(ls)
    ts = ls
    for i in range(k-22): ts.pop(13)
    ts[13]=ts[13]+'TRUNCATED'
    return(ts)



birthday = '1962-08-30'  

fail_string = ['\n']


while(len(read)>100):
    s = read.split(birthday)
    for i in range(len(s)-1):
        try:
            back = s[i][-1000:].split('),(')[-1]
            forward = s[i+1][:3000].split('),(')[0]
            backcomma = back.split(",")
            forwardcomma = forward.split(",")
            if len(backcomma)>27: backcomma=comma_cram(backcomma)
            if len(forwardcomma)>22: forwardcomma=comma_cram(forwardcomma)
            fullline = backcomma[:-1]+[birthday] + forwardcomma[1:] 
            df.loc[len(df)] = fullline
            print fullline
        except: 
            back = s[i][-500:]
            forward = s[i+1][:500]
            fail_string+= [back] + [' '] + [birthday] +[' ']+[forward]+['\n']
            print "failed ...", back, forward 
    read = f.read(N)


       
df.to_csv("look.csv")
fails = open("fail.txt", "w") 
fails.write(' '.join(fail_string))
fails.close()


oregondf= df[df['state'] =='38']


def get_emails(pnum_list):
    ef = open("aminno_member_email.dump", "r")
    eread = ef.read()
    e_list = []
    for pnum in pnum_list:
        print pnum
        tt = eread.split(",("+pnum)
        e_list+=[tt[1].split(',')[1]]
        print tt[1].split(',')[1]
    return(e_list)

#this is really slow, like 15-20 a search.  So don't do it for big files, only smaller ones.  



email_list =  get_emails(list(oregondf['id']))
oregondf['email'] = email_list 
oregondf.to_csv("oregon.csv")

######################################## the following creates zipcode csv

zipcode = 97403
fail_string = [' ']

##zip code only:
zipcode1 = str(zipcode)
zipcode2 = "','"+zipcode1+"',"


while(len(read)>100):
    s = read.split(zipcode2)
    for i in range(len(s)-1):
        try:
            back = s[i][-1000:].split('),(')[-1]
            forward = s[i+1][:3000].split('),(')[0]
            backcomma = back.split(",")
            forwardcomma = forward.split(",")
            if len(forwardcomma)>30: forwardcomma=comma_cram(forwardcomma)
            fullline = backcomma+[zipcode] + forwardcomma 
            df.loc[len(df)] = fullline
            print fullline
        except: 
            back = s[i][-500:]
            forward = s[i+1][:500]
            fail_string+= [back] + [' '] + [birthday] +[' ']+[forward]+['\n']
            print "failed ...", back, forward 
    read = f.read(N)





