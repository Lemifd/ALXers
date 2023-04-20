try :
    from . import Q1
except:
    import Q1
def title():    
    qus={}
    i=1
    title_={}
    while True:
        try:
            a="Q1.s"+str(i)
            a=eval(a)
            qus[str(i)]=a
            title_[a['title']]=a['title']
        except:
            break
        i=i+1
    return qus,title_
title_list=title()[-1]
