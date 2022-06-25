# coding: utf8
# --------------------------------------------------------------------------------
# Imports

import time
from functions import *


# --------------------------------------------------------------------------------
# Variables

query = []
results = [] # results from searches in Google/Bing + scrap
scrap = [] # temporary results for deduplication
domains = [] # domains found
domains_final = [] # final domains list
domains_final2 = [] # final domains list
domains_available = [] # available domains list
domains_undedup = []
domains_to_check = []
domains_to_check2 = []
domains_unavailable = []

# --------------------------------------------------------------------------------
# Run

while True:
  
  time_start = time.time()

  print("\nGo =========================================================>")

  # Reading first line of KW file
  read_first_line('tx_kw.txt', query)
  query = query[0] # variable from list to str
  if query == False:
    break

  # -----------------------------------------------------------------------------
  # Searching for results from query
  search(query, results, 100)
  results = list(set(results))
  print('\n{} url to scrap.'.format(len(results)))

  # -----------------------------------------------------------------------------
  # Scraping for URL in results
  scraping(results, scrap)
  results = results + scrap
  results = list(set(results))
  
  # -----------------------------------------------------------------------------
  # Extrating domains
  extract_domains(results, domains)
  domains = list(set(domains))
  
  # -----------------------------------------------------------------------------
  # Cleaning domains
  remove_sht(domains, domains_final)
  remove_sht2(domains_final, domains_final2)


  # -----------------------------------------------------------------------------
  #  Deduplicating domains found with existing domains from file
  read_to_list('tx_domains_to_check.txt',domains_undedup)
  domains_final2 = domains_final2 + domains_undedup
  domains_final2 = list(set(domains_final2))
  rewrite_to_file(domains_final2,'tx_domains_to_check.txt')
  
  # -----------------------------------------------------------------------------
  # Save kw analysed to text file
  write_to_file_one_line(query, 'tx_kw-done.txt')

  # -----------------------------------------------------------------------------
  #  Erase kw analysed from source text file
  erase_first_line('tx_kw.txt')
  print('\n[{}] removed from KW list.'.format(query))

  # -----------------------------------------------------------------------------
  #  Comparing domains to check to unavailable domains
  read_to_list('tx_domains_to_check.txt',domains_to_check)
  read_to_list('tx_domains_to_check_2.txt',domains_to_check2)
  read_to_list('tx_domains_unavailable.txt',domains_unavailable)

  rewrite_to_file('','tx_domains_to_check_2.txt')
  print('Domains to check : {}'.format(len(domains_to_check)))
  print('Domains to check 2 : {}'.format(len(domains_to_check2)))
  print('Domains unavailable : {}'.format(len(domains_unavailable)))

  domains_to_check = domains_to_check + domains_to_check2
  domains_to_check= list(set(domains_to_check))
  print('Domains to check Dedup: {}'.format(len(domains_to_check)))

  remove_list_values(domains_to_check, domains_unavailable)

  print('Domains to check All: {}'.format(len(domains_to_check)))

  rewrite_to_file(domains_to_check,'tx_domains_to_check_2.txt')

  # -----------------------------------------------------------------------------
  # Check domains availability
  domain_test2('tx_domains_to_check_2.txt','tx_domains_available.txt','tx_domains_unavailable.txt')

  rewrite_to_file('','tx_domains_to_check.txt')
  rewrite_to_file('','tx_domains_to_check_2.txt')

  # -----------------------------------------------------------------------------
  # Time & performance
  time_finish = time.time()
  print('\nIt took {}s to look for {}.'.format((time_finish-time_start), query))
  if time_finish-time_start < 45:
    wait_random(60)

  # -----------------------------------------------------------------------------
  # Reset variables
  query = []
  del results[:]
  del scrap[:]
  del domains[:]
  del domains_final[:]
  del domains_final2[:]
  del domains_undedup[:]
  del domains_to_check[:]
  del domains_to_check2[:]
  del domains_unavailable[:]