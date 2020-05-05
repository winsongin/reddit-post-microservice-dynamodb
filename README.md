# reddit-post-microservice-dynamodb

## Prerequisites

There are modules and updates that need to be installed beforehand:

- **\$ sudo apt update**
- **\$ sudo apt install --yes awscli**
- **\$ aws configure**
  - AWS Access Key ID [None]: **fakeMyKeyId**
  - AWS Secret Access Key [None]: **fakeSecretAccessKey**
  - Default region name [None]: **us-west-2**
  - Default ouptut format [None]: **table**
- **\$ sudo apt install --yes python3-boto3**
- **\$ pip3 install --user flask-dynamo**
- In addition, you must have JRE (Java Runtime Environment) or JDK installed on your computer
  - The JRE can be found at: https://www.oracle.com/java/technologies/javase-jre8-downloads.html
  - The JDK can be found at: https://www.oracle.com/java/technologies/javase-downloads.html

## Steps to start and run this microservice:

**Note:** You need all three of these terminal windows to be present while running the microservcie

1. Open a terminal window and change directory (using the **cd** command) to the **dynamodb_local_latest** directory

   - Run the following command: **java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb**

2. Open a second terminal window

   - Make sure you are in the directory of this project folder

     1. Run the following command: **flask init**

        **Note:** **flask init** is needed in order to create the DynamoDB table

     2. Run the following command: **flask run**

3. Open a third terminal window

   - To run the scripts:

     - **Note:** The scripts contain the different HTTP requests such as POST, GET, and DELETE
     - Make sure you are in the **scripts** directory
     - Run the following command: **sh filename.sh** (Replace filename with the bash file that you would like to run)

   - If you would like to test the HTTP requests manually, listed below are the different **curl** commands:

     - POST requests:

       - curl -H "Content-Type: application/json" -d '{"postID":"0", "title":"Testing1", "text":"This is Testing1", "community":"CSUF", "username":"User1"}' -X POST http://localhost:5000/api/v1.0/resources/collections

       - curl -H "Content-Type: application/json" -d '{"postID":"1", "title":"Testing2", "text":"This is Testing2" "community":"CompSci", "url":"http://fullerton.edu", "username":"User2"}' -X POST http://localhost:5000/api/v1.0/resources/collections

     - GET requests:

       - curl "http://localhost:5000/api/v1.0/resources/collections?postID=0&community=CSUF"

       - curl "http://localhost:5000/api/v1.0/resources/collections/recent?community=CSUF&amount=1"

       - curl "http://localhost:5000/api/v1.0/resources/collections/any?amount=2"

     - DELETE requests:

       - curl -X DELETE "http://localhost:5000/api/v1.0/resources/collections?postID=0&community=CSUF"
