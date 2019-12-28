# AutoTasks

This is a simple program that I use to keep track of the lessons I lose.

It works in 3 steps:

- It reads my Google Calendar through the Google Calendar API
- It scans my notes' directory looking for tex files with specific date (using a regex argoument)
- It write on Google Tasks the missing lecture with its date
