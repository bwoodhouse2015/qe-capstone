**Refactor #1**
Before:
  search_talks() was responsible for:
    -accepting user input
    -normalizing search text
    -querying the database
    -formatting API output
  Multiple responsibilities existed in the same workflow.


  
