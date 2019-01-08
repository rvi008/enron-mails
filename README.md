# enron-mails
## Instructions:

Compose a Data Summarization Script
You have to write this script in Python.
Please create a script “summarize-enron.py” that can be run from the [Unix] command line in the format:
> python summarize-enron.py enron-event-history-all.csv
The Enron event history (.csv, adapted from the widely-used publicly available data set) is attached to this email. The columns contain:
	*	time - time is Unix time (in milliseconds)
	*	message identifier
	*	sender
	*	recipients - pipe-separated list of email recipients
	*	topic - always empty
	*	mode - always "email"
Your script should produce three outputs:
	*	A .csv file with three columns---"person", "sent", "received"---where the final two columns contain the number of emails that person sent or received in the data set. This file should be sorted by the number of emails sent.
	*	A PNG image visualizing the number of emails sent over time by some of the most prolific senders in (1). There are no specific guidelines regarding the format and specific content of the visualization---you can choose which and how many senders to include, and the type of plot---but you should strive to make it as clear and informative as possible, making sure to represent time in some meaningful way.
	*	A visualization that shows, for the same people, the number of unique people/email addresses who contacted them over the same time period. The raw number of unique incoming contacts is not quite as important as the relative numbers (compared across the individuals from (2) ) and how they change over time.
Assessment
Your solution will be assessed based on:
	*	attention to detail
	*	completion of the tasks
	*	algorithm efficiency
	*	code readability
	*	adherence to common coding practices that best enable sharing, re-using, and extending the code.


## Install requirements
```pip install -r requirements.txt```

## Run script
```python summarize-enron.py enron-event-history-all.csv```

## Results
	* A csv file containing mails sents/received by person
	* A PNG image displaying amount of mails sent by most prolific users over time
	* A PNG image displaying amount of unique correspondents to the most prolific users over time