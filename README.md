# Galactic Social Network
### To use the application, head to https://galactus.onrender.com/ and signup. Welcome to the Galactus Network.
## Index
1. [About](#about)
2. [Demo](#demo)
3. [Usage](#usage)
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

| Main Chat Desktop View |
|:----------------------|
<img src="https://drive.google.com/uc?export=view&id=1-QtIt1Bsb4WhgOXa9ATvRelik_WMAO0d" width="100%" height="100%"/> |




| Main Chat Mobile View Contacts  | &nbsp;&nbsp;&nbsp; |  Main Chat Mobile View Chat  |
|:--------:|:-------------:|:--------:|
|<img src="https://drive.google.com/uc?export=view&id=1-dIbadCR_qVwcq-nw0t0WhULuGN1t3a5" style="margin-right: 10px" width="500" height="100%"/> | &nbsp;&nbsp;&nbsp; | <img src="https://drive.google.com/uc?export=view&id=1uCXv37W7XtssM-y5RsmXpsv-VnbMzxmR" width="500" height="100%"/> |


<a name="usage"></a>
## Usage

To use the application, head to https://galactus.onrender.com/ and signup. Welcome to the Galactus Network. To use it locally follow the next section.

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



<a name="dev"></a>
## Developer Features

Galactic Social Network offers a range of features, including:

- User authentication
- User profile creation and management
- Search engine for code snippets
- AI-powered chatbot to assist with searches
- Email sending and management
- Auction app for galactic equipment
- Listing management for auctions
- File storage with Amazon S3
- Data storage with Amazon RDS and PostgreSQL

<a name="credits"></a>
## Credits

- SAMYAR FARJAM (https://github.com/samyarsworld)

If you'd like to contribute to Galactic Social Network, please feel free to submit a pull request or open an issue on our [GitHub repository](https://github.com/username/repo). We welcome all contributions and feedback.

<a name="license"></a>
## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the `LICENSE` file for details.
