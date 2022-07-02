# coding: utf8
# --------------------------------------------------------------------------------
# Imports

import csv

import time
import random

import urllib
import requests
import tldextract
import io

from bs4 import BeautifulSoup

# --------------------------------------------------------------------------------
# Functions

# ===========================================================================
# File management

## Text file to list
def read_to_list(file, data):
  f = io.open(file, 'r+', encoding="utf-8", errors='ignore')
  for line in f.readlines():
    data.append(line.strip())
  f.close()

## Text file first line to list
def read_first_line(file, data):
  print('\nGetting data from KW list.')
  data.append(open(file, 'r').readline().strip())
  
## List to text file
def write_to_file(data, file):
  with open(file, 'a') as f:
    for item in data:
      f.write("%s\n" % item)

def write_to_file_one_line(data, file):
  with open(file, 'a') as f:
    f.write('\n{}'.format(data))

## List to texte file (rewrite : erase + write) >
def rewrite_to_file(data, file):
  with io.open(file, 'w', encoding="utf-8", errors='ignore') as f:
    for item in data:
      f.write('%s\n' % item)

## Erase first line in text file
def erase_first_line(file):
  with open(file, 'r') as fin:
    data = fin.read().splitlines(True)
  with open(file, 'w') as fout:
    fout.writelines(data[1:])

# ===========================================================================      
## Timeout
def wait(waiting_time):
  print('Waiting {}s'.format(waiting_time))
  time.sleep(waiting_time)

## Random Timeout
def wait_random(waiting_time):
  waiting = waiting_time
  waiting += random.randint(-5, 20)
  print('Waiting {}s ---------------------------------------'.format(waiting))
  time.sleep(waiting)

## Extract domains
def extract_domains(input, output):
  for i in input:
    list = tldextract.extract(i)
    domain_name = list.domain + '.' + list.suffix
    output.append(domain_name)

# Filterting domains and removing the ones ending by '.'
def remove_sht(data, output):
  for i in data:
    if i[-1] != '.':
      output.append(i)

def remove_sht2(data, output):    
  exclus = ['viagra','xn','porn','nude','sex','webcam','voyance','ugg','nike','theglobe','.movie','.futbol','.equipment','.management','.construction','.vacations','.investments','.builders','.mr','.pe','.gal','.casino','.casa','.works','.br','.forum','.ink','.cool','.lease','.bw','.st','.camp','.cam','.mom','.tt','.gs','.paris','.social','.vegas','.consulting','.sh','.li','.kim','.bj','.am','.limited','.family','.lat','.sd','.xxx','.gt','.ec','.sx','.mp','.rw','.mn','.ltd','.Us','.coupons','.guide','.fo','.om','.do','.gd','.recipes','.bt','.dev','.expert','.iq','.osaka','.group','.is','.fj','.love','.center','.soy','.tj','.rentals','.no','.farm','.gratis','.church','.legal','.clinic','.reviews','.pn','.mw','.wang','.africa','.menu','.vg','.cat','.kg','.gp','.Tires','.tn','.ky','.cheap','.tw','.ma','.rs','.moe','.cx','.cars','.cash','.ms','.ph','.surgery','.tc','.best','.capital','.ba','.racing','.diamonds','.eg','.help','.la','.agency','.gm','.solutions','.page','.support','.vc','.report','.training','.digital','.design','.sn','.university','.coach','.red','.my','.city','.zone','.monster','.luxury','.sk','.bg','.bike','.tech','.hn','.so','.im','.football','.industries','.ie','.holdings','.ge','.sa','.taxi','.PL','.game','.boutique','.fyi','.run','.cm','.mx','.news','.hu','.cloud','.md','.tools','.host','.games','.media','.loan','.cz','.marketing','.ae','.business','.credit','.dating','.graphics','.insure','.loans','.money','.pics','.properties','.technology','.tf','.blog','.ps','.deals','.estate','.finance','.mk','.amsterdam','.az','.market','.gr','.fail','.schule','.gh','.sg','.watch','.global','.Academy','.ug','.london','.ly','.berlin','.ag','.tr','.date','.ng','.blue','.rent','.sale','.actor','.doctor','.mba','.nyc','.pt','.lt','.ke','.ooo','.bet','.lv','.college','.directory','.ninja','.app','.nu','.work','.click','.accountant','.christmas','.faith','.dj','.pk','.webcam','.si','.dk','.il','.it','.education','.reisen','.fi','.international','.by','.press','.wales','.today','.poker','.bz','.za','.services','.zm','.hk','.email','.auction','.fund','.pink','.rocks','.systems','.hr','.asia','.cricket','.fashion','.nl','.et','.ne','.name','.life','.se','.review','.stream','.trade','.as','.pub','.tips','.icu','.tg','.nagoya','.tokyo','.cl','.es','.ee','.at','.photography','.al','.live','.bid','.party','.club','.guru','.mobi','.de','.science','.su','.qa','.ir','.ca','.lk','.men','.co','.id','.jp','.ml','.ua','.tv','.ro','.cc','.cf','.tz','.win','.to','.ch','.mz','.ga','.world','.ws','.xyz','.uk','.one','.download','.online','.band','.pet','.toys','.uno','.video','.uz','.pl','.gdn','.shop','.website','.th','.site','.nz','.in','.cn','.fm','.vip','.ru','.tk','.kz','.gq','.kr','.vn','xn','.pw','.us']
  
  trier = [x for x in data if
                all(y not in x for y in exclus)]

  for i in trier:
      output.append(i)

# Remove values from list B in list A
def remove_list_values(a, b):
  for x in b:
    try:
      a.remove(x)
    except ValueError:
      pass
  return a

# ===========================================================================
# ===========================================================================
def search(kw, data, num):

  # Searching
  print('\nSearching for [{}], {} results'.format(kw,num))
  ## User-agent
  USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
  MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

  # Scrap Google and Bing. Query > Google and Bing > Scrap > Data
  kw = kw.replace(' ', '+')
  
  # ========> Google
  URL = 'https://google.fr/search?q={}&num={}'.format(kw,num)
  # Change number to get more or less results. 10 results per page, num=10 = results on first page
  
  # Proxies
  """
  proxy = random.randint(0, len(ip_adresses) - 1)
  proxies = {"http":ip_adresses[proxy], "https":ip_adresses[proxy]}
  print(proxies)
  """
  
  headers = {"user-agent": USER_AGENT}
  resp = requests.get(URL, headers=headers, timeout=30)
  # resp = requests.get(URL, headers=headers, proxies=proxies, timeout=30)

  # --------------------------------------------------------------------------
  # Testing Google's status
  if resp.status_code == 200:
    print("\nGoogle scrapped")
  
  if resp.status_code != 200:
    headers = {"user-agent": MOBILE_USER_AGENT}
    resp = requests.get(URL, headers=headers, timeout=30)

    if resp.status_code != 200:
      x = 300
      t = time.localtime()
      current_time = time.strftime("%H:%M:%S", t)
      print('\nGoogle KO. Waiting {} s - {} - :('.format(x, current_time))
      # Waiting 20min for Google when KO
      time.sleep(1200)

  # --------------------------------------------------------------------------
  # Getting data from Google
  soup = BeautifulSoup(resp.content, "html.parser")
  for g in soup.find_all('div', class_='g'):
    anchors = g.find_all('a')
    if anchors:
        try:
          link = anchors[0]['href']
          data.append(link)
        except:
          pass
  """"
  # ========> Google News
  dates = ['2018','2017','2016','2015','2014','2013','2012','2011','2010']
  
  for i in dates:
    try:
      kw_dates = kw+i
      URL = 'https://news.google.com/search?q={}&hl=fr&gl=FR&num={}&ceid=FR:fr'.format(kw_dates,num)
    # Change number to get more or less results. 10 results per page, num=10 = results on first page

      headers = {"user-agent": USER_AGENT}
      resp = requests.get(URL, headers=headers, timeout=30)

      # --------------------------------------------------------------------------
      # Testing Google's status
      if resp.status_code == 200:
        print('\nGoogle News scrapped')
      
      if resp.status_code != 200:
        print('\nGoogle KO. Waiting 20min :(')
        # Waiting 20min for Google when KO
        time.sleep(1200)

      # --------------------------------------------------------------------------
      # Getting data from Google
      soup = BeautifulSoup(resp.content, "html.parser")
      for g in soup.find_all('div', class_='NiLAwe'):
          anchors = g.find_all('a')
          if anchors:
              link = anchors[0]['href']
              data.append('https://news.google.com'+link[1:])

      wait_random(60)

    except:
      pass
  """
  # ========> Bing
  URL = 'http://www.bing.com/search?q={}count={}'.format(kw,num)
  # Change number to get more or less results. 10 results per page, num=10 = results on first page

  # Proxies
  """
  proxy = random.randint(0, len(ip_addresses) - 1)
  proxies = {"http": ip_addresses(proxy), "https": ip_addresses(proxy)}
  Print(proxies)
  """

  headers = {"user-agent": USER_AGENT}
  resp = requests.get(URL, headers=headers, timeout=30)
  # resp = requests.get(URL, headers=headers, proxies=proxies, timeout=30)

  # --------------------------------------------------------------------------
  # Testing Bing's status
  if resp.status_code == 200:
    print("\nBing scrapped")
  
  if resp.status_code != 200:
    headers = {"user-agent": MOBILE_USER_AGENT}
    resp = requests.get(URL, headers=headers, timeout=30)

    if resp.status_code != 200:
      x = 300
      t = time.localtime()
      current_time = time.strftime("%H:%M:%S", t)
      print('\nBing KO. Waiting {} s - {} - :('.format(x, current_time))
      # Waiting 20min for Bing when KO
      time.sleep(1200)

  # --------------------------------------------------------------------------
  # Getting data from Bing
  soup = BeautifulSoup(resp.content, "html.parser")

  for g in soup.find_all('li', class_='b_algo'):
      anchors = g.find_all('a')
      if anchors:
          link = anchors[0]['href']
          data.append(link)
  
  print('\n{} links found on Google, Google News and Bing'.format(len(data)))
  print('\nSearch Engines scrap finished')

# ===========================================================================
# ===========================================================================
def scraping(data, output):
  print('\nScraping -->')

  l = len(data) # Data for completion statement
  pause = 10 # Setting for pause count down
  
  for i in data:
    # Setting headers
    headers = requests.utils.default_headers()
    headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

    error = 0

    # Passing some file types or domains
    if 'pdf' in i:
      pass
    elif 'aspx' in i:
      pass
    elif 'youtube.com' in i:
      pass
    else :
      try:
        req = requests.get(i, headers, timeout=30)

      # Getting Errors
      except:
        error = 1
        print('====================================> Get error for {} <===================================='.format(i))

      if error == 0:
        try:
          soup = BeautifulSoup(req.content, 'html.parser', from_encoding="utf-8")
        except:
          error = 1
          print('====================================> HTML error for {} <===================================='.format(i))

      # When no errors, getting inlinks from result
      if error == 0:
        all_a = soup.select('a')
        for a in all_a:
          try:
            if a['href'] != '#':
             output.append(a['href'])
          except:
            pass

        # Printing stamement for scrap completion
        print('Searched for {}, {} links founded. {} links in total. {} to go.'.format(i, len(all_a), len(output), l))
        l -= 1

        # Pause each 10 scraps
        """
        pause -= 1
        if pause == 0:
          wait_random(6) # random pause
          pause = random.randint(10, 40) # random scrap to pause
        """

# ===========================================================================
# ===========================================================================
"""
Testing domains availibility
"""
def domain_test2(file_data, file_domains_OK, file_domains_KO):
  print('\nTesting domains -->')

  domains_list =[]
  read_to_list(file_data, domains_list)
  remain = len(domains_list) - 1

  print('testing {} domains'.format(len(domains_list)))

  for i in domains_list:
    try:

      url = "https://api.gandi.net/v5/domain/check"
      querystring = {"name":i}
      headers = {'authorization': 'Apikey ma_cle_api_gandi'}
      response = requests.request("GET", url, headers=headers, params=querystring)
      
      print('Checking {} > {} domains remaining'.format(i, remain))
      remain -= 1
      answer = response.json()
      print(answer['products'][0]['status'])

      try:
        # Checking domains
        if 'error' in answer:
          pass

        elif answer['products'][0]['status'] == 'available':
          write_to_file_one_line(i, file_domains_OK)
          print('\n-----------------------> {} is available'.format(i))

        else:
          write_to_file_one_line(i,file_domains_KO)
      
      except:
        pass
    
      erase_first_line(file_data)

    except:
      pass
    
    # Time out
    wait(0.5)
