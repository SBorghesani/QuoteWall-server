# QuoteWall API

![image](https://user-images.githubusercontent.com/83084854/145895650-eebfa21b-760e-45a7-b4d3-6da784847778.png)


Quotewall is an app where users can share their favorite quotes. Whether it be from a tv show, movie, book, or even quotes amongst your friends, QuoteWall lets you 
easily remember and explore memorable quotes.

## Local Setup

1. Clone this repository and change to the directory in the terminal.
2. Run `pipenv shell`
3. Run `pipenv install`
4. Run python3 manage.py makemigrations quotewallapi
5. Run python3 manage.py migrate
6. Seed database with python3 manage.py loaddata {table name}

### LoadData Order
1.users
2.tokens
3.groups
4.quotes
5.user_groups
6.admin_groups

Once the database is set up, run the command:

```
python3 manage.py runserver
```

## Documentation

- Register a new user and explore public groups. If the group is public, select 'join' and you'll be added as a member to that group. If the group is private, 
a request to join will be sent to the admin of that group. Once you are approved, you will be able to view the quotes from that group.
- Post relevant quotes to the groups you've joined. Provide some context for the quote for other users.
- Select 'create new group' to make your own QuoteWall group. Set it to private or public depending on your preference. Any group you create you will become the admin. 
- If you are the admin, you are able to delete quotes in your group, regardless of who posted it. A 'requests' tab will also be displayed for admins of users waiting for
approval to join.
