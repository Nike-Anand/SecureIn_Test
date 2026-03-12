# SecureIn_Test

### This project Mainly Focuses on the Backend code testing . 
steps :
1) download the xml file
2) create a database and table
3) create a config file for SQL connect
4) create a parsing code based on the XMl file
5) once parsed and stored on db
6) create a file for the backend using flask (request as full python not node.js)
7) once created run the requrements file and install depencency
8) run the backned file using `cd backend && python app.py`

## get the results from the PostMan or the using the curl commands

this command help us to reterive the page and page limited data stored on DB

<br>

`http://localhost:5000/api/cpes?page=1&limit=10`


<br>


<img width="888" height="892" alt="image" src="https://github.com/user-attachments/assets/e5c116ab-7bce-4e89-bc9b-5807097fcf8b" />
<br>
### this command help to Search CPEs 

<br>


`http://localhost:5000/api/cpes/search?cpe_title=cisco`

<br>



<img width="913" height="918" alt="image" src="https://github.com/user-attachments/assets/2c2c2b83-59ad-4034-8378-e5b20c5a58f6" />
