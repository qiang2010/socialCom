#coding=UTF-8
from BeautifulSoup import BeautifulSoup
import urllib2
import time
import random

if __name__ == '__main__':
	movieids = ['25805741','6973376','24843198','11529526','10574468','10545939','25779218','24525283','4746257','24879820','25870084','5165819','1309163','20433139','25789352','10463953','24879858','25777330','3319755','6082518','24404677','24745500','11610281','4739952','2124724','1291832','1291548','4202982','1889243','4206507']
	
	m_id = 0
	p_id = 0
	i_id = 0
	flastlog = open('log/lastlog.log', 'r')
	print 'recover last log...'
	path = "E:/data/"
	
	for line in flastlog:
		if(len(line) < 3):
			continue
		pars = line.split(',')
		m_id = int(pars[0])
		p_id = int(pars[1])
		i_id = int(pars[2])

	print 'recover log: movie %d, page %d, item %d'%(m_id, p_id, i_id)
	flastlog = open(path+'log/lastlog.log', 'w')

	movie_num = 0
	for movieid in movieids:
		movie_num += 1
		while movie_num < m_id:
			continue

		timestr = time.strftime('%Y%m%d_%H%M',time.localtime(time.time())) 
		flog = open(path+'log/' + timestr + '_Mid' + movieid + '.log','w')

		lastPageIndex = 5000
		if m_id == 0 and p_id == 0 and i_id == 0:							
			f = open(path+'data/' + movieid + '.txt', 'w')
		else:
			f = open(path+'data/' + movieid + '.txt', 'a')
	
		count = 0
		while count < lastPageIndex:
			while count < p_id:
				count += 1
				continue
			
			print '%d/%d  movie:%d/%d'%(count, lastPageIndex, movie_num, len(movieids))
			fromItem = 20 * count

			url = "http://movie.douban.com/subject/"+movieid+"/comments?start="+str(fromItem)+"&limit=20&sort=new_score"
			req = urllib2.Request(url, headers = {
				'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'
            #                                             'Connection': 'Keep-Alive',
            #                                             'Accept': 'text/html, application/xhtml+xml, */*',
            #                                             'Accept-Language': 'zh_CN,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            #                                             'User-Agent': 'Mozilla/4.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
			})

			pageo = urllib2.urlopen(req)
			page = pageo.read()
			soup = BeautifulSoup(page)
		
			str1 = soup.find(name='span',attrs={'class':'fleft'}).string
			total_com = 0
			i = 0
			while not(str1[i] >= '0' and str1[i]<= '9'):
				i += 1
			while str1[i] >= '0' and str1[i] <= '9':
				total_com = total_com * 10 + int(str1[i]) - int('0')
				i += 1
			print '%d'%total_com
			
			if total_com / 20 < lastPageIndex:
				lastPageIndex = total_com / 20
			
			try:	
				comments = soup.findAll(name='div', attrs={'class':'comment-item'})
			except:
                                etime = time.strftime('%Y%m%d_%H%M',time.localtime(time.time()))
				ferrorlog = fopen('log/error' + etime + '.log', 'w')
				ferrorlog.write('Error at soup.findAll()\n')
				f.close(ferrorlog)
				break

			c_num = 0
			for comment in comments:
				#while c_num < i_id:
				#	c_num += 1
				#	continue

				try:
					avatar = comment.find(name='div', attrs={'class':'avatar'})
					top = avatar.find(name='a')
					votes = comment.find(name='span', attrs={'class':'votes pr5'}).string
					date = comment.find(name='span', attrs={'class':''}).string.strip()
					myRating = comment.find(name='span', attrs={'class':'comment-info'}).find(name='span')
				except:
                               		etime = time.strftime('%Y%m%d_%H%M',time.localtime(time.time()))
                                	ferrorlog = fopen('log/error' + etime + '.log', 'w')
                               		ferrorlog.write('Error at commit.find()\n')
					ferrorlog.write('%s\n'%(str(comment)))
                                	f.close(ferrorlog)
					break

				allstar = myRating['class']
				userName=top['href'].split('/')[4]

				if len(allstar) < 9:
					continue;
			
				rating = allstar[7]

				f.write(userName + '\n')
				f.write(top['href'] + '\n')
				f.write(rating + '\n')
				f.write(date + '\n')
				f.write(votes + '\n')

				flog.write('%d/%d, %d, movie:%d/%d\n'%(count, lastPageIndex, c_num, movie_num, len(movieids)))
				flastlog.write('%d,%d,%d\n'%(movie_num, count + 1, c_num))
				c_num += 1
			
			
			time.sleep(float(random.randint(6,16)) / 10.0)

			count += 1

		f.close()
		flog.close()
		flastlog.close()
