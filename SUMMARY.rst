================
Economist Task
================


Summary 
~~~~~~~~~~~~~

The polling page contains a list of polls from a presidential election in a hypothetical country.
The election will be held on the 10th of October, 2024.

This PollScraper package will serve as a scraper tool, used to pull the polls off the polling page, convert them to a CSV, and create a poll average based on those polls. 
This must be robust to all the normal issues we see in aggregate polling lists:

    * Some days have no polls, some have multiple
    * Some pollsters do not include line items for all candidates
    * Some pollsters will conduct multiple polls with hypotheticals (e.g. what if this candidate dropped out?)
    * The order of candidates on the page may change
    * Formatting may be inconsistent

As well as the normal things that happen during election campaigns:

    * Opinions can shift suddenly
    * A candidate might drop out
    * A candidate might join the race late
    * There may be big gaps in the polling record (for example, around Christmas or for this country’s two-week public holiday in June)
    * There may be significant data entry errors
    * Notes might be attached to specific polls or numbers

The poll tracker page will add more polls over time.


Requirements 
~~~~~~~~~~~~~



The structure of the table will never change, and its design is pretty simple.
The code base should provide error monitoring, and will detect or alert the user in the event of a major error. 


Results
~~~~~~~~~~~~~

This script should output two CSVs, called polls.csv and trends.csv (for the averages).
The polls file should have columns for date, pollster, n (sample size), and each candidate (by name); the trends file just date and a column for each candidate.
Values for polls and trends should be a number from 0 to 1.
The polls file should have a row for each poll. The trends file should have a row for each day, starting with October 11th, 2023.
Examples are shown in the ``data/polls.example.csv`` and ``data/trends.example.csv`` files.



Assumptions
~~~~~~~~~~~~~

It can be assumed that the structure of the source table will never change. As such, I am assuming that this table reflects a complete
record of all polling data available up to the current date, and that this data will all be served in one table. This simplifies the code,
as it allows me to not handle multiple tables being read, or to persist and then combine polling data between runs. This also means that when
a candidate drops out, their historical data should remain on the polling records.



Notes
~~~~~~~~~

Note, scraped values are sorted first by date and then alphabetically by Pollster. This ordering may differ from the source html, but is equivalent. 