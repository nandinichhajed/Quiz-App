# Quiz-App
A website in which the user can play a quiz. Here the user has multiple questions and can select options and submit the quiz. In the end, the total score of the quiz will be displayed. this website is build using the Python Django web framework and Fauna.


Fauna is a client-side serverless document database that makes use of GraphQL and the Fauna Query Language (FQL) to support a variety of data types and particularly relational databases in a serverless API. 

## Tech Used
- Django
- Python
- postgresql
- Html
- CSS
- JS

## Run Locally

**Clone project**

```bash
git clone https://github.com/nandinichhajed/Tubers.git
```

**Get project forlder**

```bash
cd tubers
```

**Create virtual Environment**

```bash
virtualenv venv
```

**Activate virtual Environment**

```bash
.\venv\Scripts\activate
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Migrate**

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

**Creating The Collections in Fauna**

create four collections `Users`, `Quiz`, `Question` and `Answers`.

**Creating the Fauna Indexes**

We will need to create eight Fauna indexes that will allow us to scroll through data added to our database. The indexes are the; `user`, `quiz_index`, `quiz_get_index`, `question_index`, `question_get_index`,`question_answer`,`answer_score_index` and the `answer_get_index`.

- The `user` index will have a term for `username` and will be a unique field that will allow querying of the User collection. 

- The `quiz_index` index will have a term for `name` and will be a unique field that will allow querying and creating new documents in the Quiz collection. 

- The `quiz_get_index` index will have a term for `status` which will also allow querying of the Quiz collection. 

- The `question_index` index will have a term for `question_asked` which will allow querying of the Question collection. 

- The `question_get_index` will have a term for "name" which will allow querying and matching with of the data in the Question collection. 

- The `question_answer` index will have a term for `correct_answer` which will also allow querying and matching of Question collection. 

- The `answer_score_index` will have a term for `user` and `quiz` which will allow matching and querying of the Answers collection. 

- The `answer_get_index` will have a term for `user` and `question` which will also allow matching and querying of the Answers collection.


### Run server

```bash
python manage.py runserver
```
( * Running on http://127.0.0.1:8000/)

## Feedback

Give a ⭐️ if this project helped you!

These samples may be updated from time to time so you might want to get updates
using `git pull`.  Also if there are bugs, you are welcome to submit
a Pull Request on github.Either
Reach out to me on [LinkedIn](https://linkedin.com/in/nandinichhajed)

<h2>Author</h2>
<blockquote>
  Nandini Chhajed<br>
  Email: nandinichhajed08@gmail.com
</blockquote>

<div align="center">
    <h3>========Thank You !!!=========</h3>
</div>
