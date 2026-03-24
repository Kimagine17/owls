The Owl Crew Report (Alex, Almendra, Kimberly)

Our project takes the livestream footage of an owl box and scans the image to determine what elements are present in the current frame. It then saves the found data to a database where it can be queried later. 

 

Diagram of the system, with bottlenecks and limits marked::
<img width="1600" height="676" alt="image" src="https://github.com/user-attachments/assets/d2d6946c-e752-4b2c-9da9-d68fbbe45ca5" />

ERD:
<img width="1056" height="426" alt="image" src="https://github.com/user-attachments/assets/65caef58-bdf5-4e89-a8a4-754242c0fabd" />

Key learnings from the project (please try to come up with at least 3)

Almendra:

I learned about the video recognition program YOLO that makes it possible to convert what is shown in videos to data. 
Microsoft has a database management system that uses Kusto which is similar to SQL. I learned how to translate the queries I wrote with mySQL syntax to convert it to KQL.
We can produce an abundance of data just from a short amount of time from a live video feed. It’s not only important to know how to collect your data, but to filter out what data is worth keeping. 


Alex:

How Kusto works to optimize their data entry. In comparison to a lot of other database services they are able to have fast and frequent writes to the database even if there are multiple writes happening in a second.
I also looked at how to apply some higher level programming patterns to best make the codebase so that it can easily be modified and changed over time. This was to approach the differences between the csv and Kusto connectors.
Something important I also learned is that if we stored data as text when it is formatted as JSON there is additional overhead cost to call the row and then to parse the JSON instead of inserting specific fields into a row in the database. This is why we chose to make sure to insert each value in its own column in the database.


Kimberly: 

It’s worth it to integrate with existing technologies. This project uses YOLOv5 and Kusto Azure Data explorer. Having these systems already existing meant we could focus on more interesting parts of the project instead of debugging a hand-built database. In summary, It takes time to learn a new system, but then saves time later.
I learned a lot about Kusto and Azure Data Explorer! I hadn’t heard of it before this class, and now I am comfortable using it. In particular, I learned a lot about the dot commands (it took me forever to find the .clear table owls data command, and for a while I was dropping and rebuilding the table to empty it)
I learned about uploading real time data. Kusto is designed to work in real time, which is great for the owl video streams. However, the Kusto connection we are using only lasts for 15 minutes, meaning it can’t be open for 8 hours overnight. Currently we write to a CSV file, then upload that later. I am going to see if I can find a more persistent connection for the future. 
 

Failover strategy:

There is not currently a failover strategy, but there is a try catch around the insertion to the database. We could write the failed row to a CSV file (like failed_entries.csv) to review and reupload later.

 

Video Recording:

(Video description: a short demonstration on a prerecorded owl video. You can see the command to run YOLO and output screen showing which rows are being inserted. Then, the azure data explorer is pulled up, and a few queries are demonstrated.)

 

Conclusion:

Thank you for reading this! We enjoyed working on this project, and would love to answer additional questions. Or if you have great ideas for the owls, drop them below! 

 

Follow the owls on instagram at @screech_owls or find the live stream under the youtube channel cesium13


GitHub link: 

https://github.com/Kimagine17/owls

Deep Learning Owls Assignment

[Call with Alex and 1 other-20250411_171553-Meeting Recording.mp4
](https://byu.sharepoint.com/sites/CS452Winter2025/Shared%20Documents/Final%20Project%20Presentations/Call%20with%20Alex%20and%201%20other-20250411_171553-Meeting%20Recording.mp4)
