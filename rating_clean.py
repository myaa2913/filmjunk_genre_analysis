import re

#declare rating_clean function 
def rating_clean(url):
    url = str(url)

    try:    
        
        m_5 = re.match('.*stars\dsm_(\d+)\.jpg', url)
        m_4 = re.match('.*stars_sm(\d+)\.jpg', url)


        if m_5:
            
            extract = m_5.groups()[0]
            
            if len(extract) == 1:
                return (extract, 5)
            
            if len(extract) == 2:
                return (extract[0] + '.' + extract[1], 5)


        if m_4:
            
            extract = m_4.groups()[0]
            
            if len(extract) == 1:
                return (extract, 4)
            
            if len(extract) == 2:
                return (extract[0] + '.' + extract[1], 4)


        else:
            return ''

    except AttributeError:
        return ''


print rating_clean('http://www.filmjunk.com/images/site/stars5sm_3.jpg')[1]
