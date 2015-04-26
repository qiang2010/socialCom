# coding=utf-8
from bs4 import BeautifulSoup
import html5lib
import urllib
import urllib2
import time
import re
import os
from email import _name
import Comment
if __name__ == '__main__':
    
    movieids = ['1889243']#['4206507'] 
    for movieid in movieids:
        lastPageIndex = 5000
       # path = os.path.normcase("E:/data/")
        path = "E:/data/";
        f = open(path+movieid + '.txt', 'w')
        count = 0
        while count < lastPageIndex:
            print '%d / %d'%(count,lastPageIndex)
            fromItem=20*count
            
            url = "http://movie.douban.com/subject/"+movieid+"/comments?start="+str(fromItem)+"&limit=20&sort=time"
            req = urllib2.Request(url, headers = {
                                                         'Connection': 'Keep-Alive',
                                                         'Accept': 'text/html, application/xhtml+xml, */*',
                                                         'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                                                         'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
            })
            #req = urllib.open()#urlopen("http://movie.douban.com/subject/"+movieid+"/comments?start="+str(fromItem)+"&limit=20&sort=time")
            pageo = urllib2.urlopen(req)
            
            
            page = pageo.read()
            
            soup = BeautifulSoup(page)
            str1 = soup.find(name='span',attrs={'class':'fleft'}).string
            total_com = 0
            i = 0 
            while not(str1[i] >= '0' and str1[i]<= '9'):
                i = i+1
            while str1[i] >= '0' and str1[i] <= '9' :   
                total_com = total_com * 10 + int(str1[i]) - int('0')
                i = i+1
            print '%d\n'%total_com
            
            if total_com / 20 < lastPageIndex:
                lastPageIndex = total_com / 20
                    
            comments = soup.find_all(name='div', attrs={'class':'comment-item'})
            myComments = []
           
            for comment in comments:
                time.sleep(1)
                avatar = comment.find(name='div', attrs={'class':'avatar'})
                top = avatar.find(name='a')
                votes = comment.find(name='span', attrs={'class':'votes pr5'}).string
                date = comment.find(name='span', attrs={'class':''}).string.strip()
                myRating = comment.find(name='span', attrs={'class':'comment-info'}).find(name='span')
                #print str(myRating)
                allstar = myRating['class']
                userName=top['href'].split('/')[4]
                if len(allstar) < 2:
                    continue
    
                
                rating = allstar[0][7]
                myComment = Comment.Comment(userName, top['href'], rating, date, votes)
                myComments.append(myComment)
                #print(myComment.userName)
                #print(myComment.url)
                #print(myComment.rating)
                #print(myComment.date)
                #print(myComment.votes)
                #print('***************************')
                
                f.write(myComment.userName + '\n')
                f.write(myComment.url + '\n')
                f.write(myComment.rating + '\n')
                f.write(myComment.date + '\n')
                f.write(myComment.votes + '\n')
                
            count+=1
            
        f.close()
    # print(comments)
#         f=open('25805741:'+str(count)+'.html','w')
#         f.write(page)
#         f.close()
    
    

