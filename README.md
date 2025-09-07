# Little Lemon Capstone Project

By working through the lessons in this course, you revisited the necessary concepts and knowledge of back-end development. Using the Django REST Framework, you put your skills into practice to build an API for the Little Lemon restaurant.

You completed exercises, received general instructions and code snippets, and utilized links to resources from previous courses to complete this task.

You demonstrated your web development skills by writing code to create an API that handles table bookings for the Little Lemon restaurant.

The API can receive HTTP requests such as GET, POST, PUT and DELETE, and updates the Django models, which in turn, updates the data in a MySQL database.

---

## 📌 Peer Review Instructions

You will participate in a peer review exercise in which you will submit your completed project for two of your peers to review. You will also be required to review a project of two of your peers.

### Grading Criteria
- Does the web application use Django to serve static HTML content?
- Has the learner committed the project to a Git repository?
- Does the application connect the backend to a MySQL database?
- Are the menu and table booking APIs implemented?
- Is the application set up with user registration and authentication?
- Does the application contain unit tests?
- Can the API be tested with the Insomnia REST client?

---

## 🔗 API Paths to Test
- /api/menu/
- /api/bookings/
- /api/registration/
- /api/token/login/
- /api/token/refresh/

---

## 👥 Current Users
**Admin (Admin is also a Manager)**  
- Username: admin  
- Password: 123  
- Token: 7d7f9cb36eb663519d0ea4e9eec003c4a7a300fc  

**Manager**  
- Username: manager1  
- Password: lemon@123!  
- Token: d49508708b06eaf1a5355222df8b5e0309df0eb3  

**Customer**  
- Username: customer1  
- Password: lemon@123!  
- Token: a88aaf06a40c65c65685ea7d54b94fa3ece84382  

**Delivery crew**  
- Username: delivery1  
- Password: lemon@123!  
- Token: 8d5a192946e31cab37e8babc5c7483c10845804f  

---

## 🚀 Submission Steps
1. Click on the **My submission** tab  
2. Provide a Project Title, for example: *Back-end developer capstone project*  
3. Paste the URL of the GitHub repository that contains your capstone project code.

---

## 📋 Additional API Endpoints

This project provides API endpoints for the following functions, aiming for the management of Littlelemon restaurant:
1. User registration and token generation endpoints 
2. Category and menu-items endpoints
3. User group management endpoints
4. Cart management endpoints 
5. Order management endpoints

### Fields needed for some POST methods:
The API routes are working the same as described in https://www.coursera.org/learn/apis/supplement/Ig5me/project-structure-and-api-routes

Here are some notice about the fields needed and accepted type when using POST, PUT or PATCH methods via certain endpoints. They are tested in Insomnia.

```/api/users ```
- **username**: string 
- **email**: email 
- **password**: string

```/api/token/login/ ```
- **username**: string 
- **password**: string

```/api/category```
- **slug**: string 
- **title**: string

```/api/menu-items```
- **title**: string 
- **price**: decimal
- *featured*: (opt.) boolean, default=False
- **category**: integer (you can check the category id via ```/api/category``` endpoint, currently there are 3 categories)

```/api/groups/manager/users```

```/api/groups/delivery-crew/users```
- **username**: string (you can check all the usernames via ```/api/users ``` endpoints with manager token)

```/api/cart/menu-items```
- **menuitem**: integer (you can check teh menuitem id via ```/api/menu-items``` endpoint, currently there are 9 items)
- **quantity**: integer

```/api/orders/{orderId}```
1. Manager: (PATCH is recommended than PUT)
- **delivery_crew**: integer (you can check delivery user_id via ```/api/groups/delivery-crew/users``` endpoint with a manager token)

2. Delivery crew: (PATCH only)
- **status**: boolean
