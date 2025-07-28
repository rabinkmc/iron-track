## tasks


### general

1. Currently, one has workout sessions, where he can add exercises, and track his workout sets.
2. Polishing the UI, add description to the exercises, incorporating gifs to show how to perform the exercise
3. Need to add feature to track progress of lifts, (daily, weekly, monthly )
4. Also track measusres like bodyweight, sleep, water, macros etc

### priorities
1. Progress tracker 
2. Workout templates

### fe
1. Improve UI for google signin
2. Progress tracker
3. load from workout template, i.e previous workout sessions
4. Add validation in the frontend, and flash messages on both success and errors 

### be
1. Progress tracker api
2. enable the use of previous workout templates to create new ones

### api design for progress tracker

/api/progress/<exercise:id>
- the data should be ordered by dates

backend's responsibility is to just send the data

- it is entirely upto fe, for now I am thinking of linear chart. In the chart, we can adjust the views, weekly, monthly ... 
