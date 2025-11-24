This is a simple Task managing CLI app that I made for completing roadmap.sh .
To use this CLI you need to envoke python over the main.py file add add comand line arguments.
The commands are.

add "Task description"                  -- Make new task
update task-id "Updated description"    -- Update existing task
delete taks-id                          -- Delete task

mark-to-do task-id                      -- Mark task as to-do
mark-in-proggress task-id               -- Mark task as in-progress
mark-done task-id                       -- Mark task as done

list                                    -- List all tasks
list "taks status"                      -- List all tasks that have a sprecific status


Next upgrade to this project would be to use slqlite database.

Same logic could be used to make a web app.