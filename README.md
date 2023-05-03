# Galactic Social Network
### To use the application, head to https://galactus.onrender.com/ and signup. Welcome to the Galactus Network.
## Index
1. [About](#about)
2. [Demo](#demo)
3. [Technologies](#tech)
4. [Usage](#usage)
    * [Installation](#installation)
    * [In the Webapp](#webapp)
5. [Developer Features](#dev)
6. [Future Improvements](#future)
    * [Frontend](#front)
    * [Backend](#back)
7. [Credits](#credits) 
8. [License](#license)
 

<a name="about"></a>
## About
Galactic Social Network is an interstellar themed social networking platform that allows users to connect, share, and learn from each other. Additionally, users can communicate, as well as, buy cool galactic equipment in auctions. This platform consists of three major apps that are:

1. **Social Network**: This section allows users to create profiles, follow each other, and share code snippets with the community. The search engine helps users find code snippets they are looking for, and the AI-powered chatbot, ChatGPT from OpenAI, can assist users in finding what they need. Users can like or dislike posts and have the ability to create, edit, or remove their own posts.

2. **Email sending**: This section provides users with an inbox, sent box, and archive, and they can compose and send emails to other users.

3. **Auction**: In this section, users can list their galactic equipment, such as spaceships and clothing, and other users can bid on the items. Each listing has a detailed description, and users can bid, add items to their watchlist, or comment on listings. Users can also end bids or remove their listings as they see fit.

The platform also has authentication features, and users can update their profile information and settings once signed up. Amazon S3 is used for file storage, while Amazon RDS in conjunction with PostgreSQL is used to store data in the cloud. Django and Python are used for the front-end and back-end frameworks.

<a name="demo"></a>
## Demo
| Authentication Page  |
|:----------------------|
|<img src="https://drive.google.com/uc?export=view&id=1mNkU_kPftiDHwoH6WJqsulc4mz7NWUBu" width="100%" height="100%"/> |

| Home View |
|:----------------------|
<img src="https://drive.google.com/uc?export=view&id=1dmkGKMCtF6_sYlMLVYuTtgzITPmeqcrG" width="100%" height="100%"/> |


| Social Media App View |
|:----------------------|
<img src="https://drive.google.com/uc?export=view&id=1c9bgW5ht8ySEVeiWLdAarw6AT8m5TiLz" width="100%" height="100%"/> |


| Mailing App View |
|:----------------------|
<img src="https://drive.google.com/uc?export=view&id=1H6kDwJ8r7ORiyBNytJ0Ng4DiX-GQhds0" width="100%" height="100%"/> |

| Auction App Home View |
|:----------------------|
<img src="https://drive.google.com/uc?export=view&id=1uhXgn3gliAxAx1tiu0J-IN6AsidBB83v" width="100%" height="100%"/> |


| Making Bids in Auction View  | &nbsp;&nbsp;&nbsp; |  Winning Bids in Auction View  |
|:--------:|:-------------:|:--------:|
|<img src="https://drive.google.com/uc?export=view&id=1X1ANmepXFyc9hFlXqCppKMVN4Uo3nc53" style="margin-right: 10px" width="500" height="100%"/> | &nbsp;&nbsp;&nbsp; | <img src="https://drive.google.com/uc?export=view&id=1AnUtIUpzITkHFKChzmSXZJLyWf0bq6xH" width="500" height="100%"/> |


<a name="tech"></a>
## Technologies
- Django
- Python
- Jinga
- HTML, CSS, Javascript
- AWS S3
- AWS RDS
- Postgres
- Open AI ChatGPT3


<a name="usage"></a>
### Usage

To use the application, head to https://galactus.onrender.com/ and signup. To use it locally follow the next section.

<a name="installation"></a>
### Installation

To install Galactic Social Network on your local computer, you need to:

1. Open your favourite IDE.

2. Clone the repository to your local machine.

3. Create a virtual enviornment by executing `virtualenv venv` in the terminal. Then activate the venv. For windows users `.\venv\scripts\activate`. For Linux users `venv/bin/activate`.

4. Install the required packages by running `pip install -r requirements.txt` in your terminal.

5. Set up your database by running `python manage.py makemigrations network mail auction authMain` followed by `python manage.py migrate`.

6. Create a superuser account by running `python manage.py createsuperuser`.

7. Start the development server by running `python manage.py runserver`.

8. Navigate to `http://127.0.0.1:8000` in your browser to access the platform.


### In the Webapp
<a name="webapp"></a>

Welcome to our webapp! Here's a brief overview of what you can expect:

Getting started:
- Upon opening the app, you will be prompted to create an account and register your information. Rest assured that your data will be safely stored in our cloud-based database.

The Three Major Apps:
- Once you've logged in, you will have access to three major apps that are seamlessly interconnected. 

1. The Network App:
- In this app, you can browse through posts created by real users, as well as create and publish your own posts for others to see.
- You can use the search function to look for specific posts or ask our AI-powered search tool for assistance.
- You have the ability to like or dislike posts, follow other users, and add posts to your community.
- Clicking on each post will give you more details and information.

2. The Email App:
- With this app, you can easily send and receive messages with your friends who also have accounts within the app.
- You can archive important messages for future reference.

3. The Auction App:
- In this app, you can bid on listings posted by other users, or create your own listing to sell.
- Listings have detailed information and can be added to your watchlist for easy tracking.
- As a listing holder, you have the power to remove or sell your listing to the highest bidder.

We hope you enjoy using our app and have a great experience connecting with others in our community!


<a name="dev"></a>
## Developer Features

Galactic Social Network uses a range of features, including:

- **User authentication:** The app features robust user authentication measures to ensure that only authorized users have access to the app using Django authentication and decorators libraries.

- **User profile creation and management:** Ability to create and manage user profile. This includes adding personal information, profile picture, and managing account settings.

- **Search engine for code snippets:** This is particularly useful for developers and programmers who need quick access to code snippets for their projects. The feature is made available by using django filters.

- **AI-powered chatbot to assist with searches:** In addition to the search engine, an AI-powered chatbot is used to assist with searching. Simply type in query and the chatbot will provide you with relevant results. This is made available by using OpenAI "gpt-3.5-turbo" engine with 0.5 temperature.

- **Email sending and management:** The email module allows sending and managing emails. This is a convenient feature for users who prefer to keep their communication within the app. The whole app uses "one Page Application" method using Javascript to skip loading for a fast user experience.

- **Auction app for galactic equipment:** The auction module allows you to bid on galactic equipment. This is a fun and engaging feature for users who want to participate in auctions and acquire or sell unique items. CRUD methods are used along side a structured relational databased desgined using Django.

- **Listing management for auctions:** Sellers can create and manage their listings for auctions. This includes adding descriptions, images, and setting starting bids. This is made available by using Django models to create an efficient database.

- **File storage with Amazon S3:** The app integrates with Amazon S3 for file storage, ensuring that files are securely stored and easily accessible whenever needed.

- **Data storage with Amazon RDS and PostgreSQL:** The app's data is stored securely with Amazon RDS and PostgreSQL, ensuring that information is safe and protected at all times.


<a name="credits"></a>
## Credits

- SAMYAR FARJAM (https://github.com/samyarsworld)

If you'd like to contribute to Galactic Social Network, please feel free to submit a pull request or open an issue on our [GitHub repository](https://github.com/samyarsworld/social-network). We welcome all contributions and feedback.

<a name="license"></a>
## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the `LICENSE` file for details.
