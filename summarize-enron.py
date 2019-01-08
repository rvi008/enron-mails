#!/usr/bin/env python # -*- coding: UTF-8 -*-
"""
Compose a Data Summarization Script
You have to write this script in Python.
Please create a script “summarize-enron.py” that can be run from the [Unix] command line in the format:
> python summarize-enron.py enron-event-history-all.csv
The Enron event history (.csv, adapted from the widely-used publicly available data set) is attached to this email. The columns contain:
	•	time - time is Unix time (in milliseconds)
	•	message identifier
	•	sender
	•	recipients - pipe-separated list of email recipients
	•	topic - always empty
	•	mode - always "email"
Your script should produce three outputs:
	•	A .csv file with three columns---"person", "sent", "received"---where the final two columns contain the number of emails that person sent or received in the data set. This file should be sorted by the number of emails sent.
	•	A PNG image visualizing the number of emails sent over time by some of the most prolific senders in (1). There are no specific guidelines regarding the format and specific content of the visualization---you can choose which and how many senders to include, and the type of plot---but you should strive to make it as clear and informative as possible, making sure to represent time in some meaningful way.
	•	A visualization that shows, for the same people, the number of unique people/email addresses who contacted them over the same time period. The raw number of unique incoming contacts is not quite as important as the relative numbers (compared across the individuals from (2) ) and how they change over time.
Assessment
Your solution will be assessed based on:
	•	attention to detail
	•	completion of the tasks
	•	algorithm efficiency
	•	code readability
	•	adherence to common coding practices that best enable sharing, re-using, and extending the code.

"""

import pandas as pd
import re
from collections import Counter
from matplotlib import pyplot as plt
from os import sys

NAMES = ['time', 'message identifier', 'sender', 'recipients', 'topic', 'mode']



class Mail_corpus:
	'''This class implements the solution to proposed case, it has methods to parse enron dataset, compute mail sent/received and plot them in a meaningful way''' 
	def __init__(self, path):
		self.path = path
		self.inp = pd.read_csv(path, names=NAMES)
		self.inp['sender'] = [Mail_corpus.clean_name(str(n)) for n in self.inp['sender'].tolist()]
		self.sents = Counter(self.inp.sender.tolist()) 
		self.received = Counter([Mail_corpus.clean_name(n) for n in Mail_corpus.split_name_list(self.inp['recipients'].values.tolist())])
		self.entries = pd.DataFrame([self.sents, self.received]).T.sort_values(by=0, ascending=False)

		#Create a new dictionary containing both keys and 

	def split_name_list(name_list, concat=True):
		'''Util function to build columns based on a "|" separated string'''
		name_list = map(lambda x:str(x).split('|'), name_list)
		d = pd.DataFrame.from_records(name_list)

		if concat: 
			return pd.concat([d[col] for col in d]).dropna() #Return all the recipients names in one column
		else: 
			return d #Return all the recipients name in distinct columns corresponding to the posistion in the "to" field

	def clean_name(s):
		'''Util function to perform cleaning on senders/receiver string field'''
		s = re.sub('\.', string=re.sub(r'\s*[@\/].*|\s*at\s+\w+', string=s.lower(), repl=''), repl=' ')#Clean the strings 
		s = re.sub('\W', string=s, repl=' ')
		return s.strip()


	def output_communications(self, file_name):
		'''This method implements the solution to the first request, namely, output a count of mail sent/received by person'''
		self.entries.columns = ['no of mail sents', 'no of mail received']
		self.entries.to_csv(file_name)#The dataset outputed is sorted by mail sent count decreasing (see __init__) 
		print('File of email sent/received by person outputed to '+file_name)

	def plot_mail_count_from_prolific_senders(self, file_name, no_persons=5):
		'''This method does the mandatory transformations for plotting the count of mail sent by the most prolific users, then it calls the plotting function'''
		prolifics = self.inp[self.inp['sender'].isin(self.entries.index[:no_persons].tolist())][['time','sender']] #Filter on most prolific users
		prolifics['count'] = 1 #Add this field to perfom running sum on the count of mails sent
		piv = pd.pivot_table(prolifics, values='count', index='time', columns='sender').sort_index(ascending=True)#We pivot the Dataframe in order to count mails by senders

		for col in [c for c in piv.columns if c !='sender']:
			piv[col] = piv[col].cumsum().fillna(method='ffill') #Forward filling as the time series are disrupted

		time = piv.index
		piv['date'] = pd.to_datetime(time, unit='ms') 
		Mail_corpus.plot_line_chart(piv, file_name, 1)
		print('PNG graph of emails sent over time for prolific users saved in: '+file_name)

	def plot_mail_count_distinct_to_prolifics(self, file_name, no_persons=5):
		'''This method does the mandatory transformations for plotting the count of unique senders contacting the most prolific users, then it calls the plotting function'''
		r = Mail_corpus.split_name_list(self.inp['recipients'].values.tolist(), False) #Resplit recipient column but keep names in columns

		for col in r.columns:
			r[col] = r[col].map(lambda x: Mail_corpus.clean_name(str(x))) #Clean strings in each column

		temp = pd.concat([self.inp, r], axis=1).drop(['recipients', 'message identifier', 'mode', 'topic'], axis=1) #Dataframe with time, sender & all recipients columns
		df_list = []

		for p in self.entries.index[:no_persons].tolist():
			t = temp[temp[temp.columns[2:]].isin([p]).T.any()].copy() #Only keep mail sent to most prolific users
			t['unique_count'] = Mail_corpus.rolling_unique(t) #Count unique senders in a running count of uniques
			t['recipient'] = p
			df_list.append(t[['time', 'unique_count', 'recipient']].copy())

		df = pd.concat(df_list, axis=0)
		piv = pd.pivot_table(df, values='unique_count', index='time', columns='recipient').sort_index(ascending=True)
		piv['date'] = pd.to_datetime(piv.index, unit='ms')

		for col in [c for c in piv.columns if c !='date']:
			piv[col] = piv[col].fillna(method='ffill') #Forward filling as the time series are disrupted


		Mail_corpus.plot_line_chart(piv, file_name, 2)
		print('PNG graph of unique senders over time to prolific users saved in: '+file_name)

	def rolling_unique(df):
		'''Util function to perfom running counts of values over time'''
		distinct_users = set()
		unique_count = []

		for index, row in df.iterrows():
			distinct_users.add(row['sender'])
			unique_count.append(len(distinct_users)) #Keep the unique count by getting the length of senders set

		return unique_count 


	def plot_line_chart(piv, file_name, type_chart):
		''' Util function to plot & save line chart in the provided file_name'''
		piv.plot(x='date', y=[c for c in piv.columns if c !='date'])

		if type_chart == 1:
			plt.title('Mails sent over time for prolific users')
		else:
			plt.title('Unique users having sent mails over time to prolific users')

		plt.legend(loc='best')
		plt.savefig(file_name)


if __name__ == '__main__':
	m = Mail_corpus(sys.argv[1])
	m.output_communications("out.csv")
	m.plot_mail_count_from_prolific_senders('sent_mails.png')
	m.plot_mail_count_distinct_to_prolifics('unique_contacts.png')


	