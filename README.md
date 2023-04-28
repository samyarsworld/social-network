# Galactic Social Network

Galactic Social Network is a social networking platform that allows users to connect, share, and learn from each other. This platform consists of three major apps that mimic the functionalities of Facebook. The three major apps include:

1. Social network section: This section allows users to create profiles, follow each other, and share code snippets with the community. The search engine helps users find code snippets they are looking for, and the AI-powered chatbot, ChatGPT from OpenAI, can assist users in finding what they need. Users can like or dislike posts and have the ability to create, edit, or remove their own posts.

2. Email sending section: This section provides users with an inbox, sent box, and archive, and they can compose and send emails to other users.

3. Auction app: In this section, users can list their galactic equipment, such as spaceships and clothing, and other users can bid on the items. Each listing has a detailed description, and users can bid, add items to their watchlist, or comment on listings. Users can also end bids or remove their listings as they see fit.

The platform also has authentication features, and users can update their profile information and settings once signed up. Amazon S3 is used for file storage, while Amazon RDS in conjunction with PostgreSQL is used to store data in the cloud. Django and Python are used for the front-end and back-end frameworks.

<a name="demo"></a>
## Demo
| Authentication Page  |
|:----------------------|
|<img src="https://drive.google.com/uc?export=view&id=1mNkU_kPftiDHwoH6WJqsulc4mz7NWUBu" width="100%" height="100%"/> |

| Main Chat Desktop View |
|:----------------------|
<img src="https://drive.google.com/uc?export=view&id=1-QtIt1Bsb4WhgOXa9ATvRelik_WMAO0d" width="700" height="100%"/> |




| Main Chat Mobile View Contacts  | &nbsp;&nbsp;&nbsp; |  Main Chat Mobile View Chat  |
|:--------:|:-------------:|:--------:|
|<img src="https://drive.google.com/uc?export=view&id=1-dIbadCR_qVwcq-nw0t0WhULuGN1t3a5" style="margin-right: 10px" width="500" height="100%"/> | &nbsp;&nbsp;&nbsp; | <img src="https://drive.google.com/uc?export=view&id=1uCXv37W7XtssM-y5RsmXpsv-VnbMzxmR" width="500" height="100%"/> |



## Installation

To install Galactic Social Network, you need to:

1. Clone the repository to your local machine.

2. Install the required packages by running `pip install -r requirements.txt` in your terminal.

3. Set up your database by running `python manage.py migrate`.

4. Create a superuser account by running `python manage.py createsuperuser`.

5. Start the development server by running `python manage.py runserver`.

6. Navigate to `http://127.0.0.1:8000` in your browser to access the platform.

## Features

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

## Contributing

If you'd like to contribute to Galactic Social Network, please feel free to submit a pull request or open an issue on our [GitHub repository](https://github.com/username/repo). We welcome all contributions and feedback.

## Contributors

- SAMYAR FARJAM (https://github.com/samyarsworld)

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the `LICENSE` file for details.
