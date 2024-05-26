Building my own webserver 

from codingchallenges.fyi

1. Build basic webserver
Server side:
- receive request string
- return response

2. Serve HTML pages
- www is the localhost root directory
Steps:
- 1/ Receive request
- 2/ Parse: split string by space delimiter -> save elements into a dictionary
- 3/ Form Response --> send to client

Issues/ Learning notes:
- exceptions can be handled better.
- not sure how to structure the http codes so that it accomodates for increasing checks and codes.

3. Handling Multiple Concurrent clients

4. Addressing security risks
