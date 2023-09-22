# CORO - Programming App for Church Choirs

CORO is a programming app for church choirs that allows staff to have a solid management on the music of the church.

I started this app with much care during my time in [Coding Temple](https://www.codingtemple.com/software-engineering/)'s Full-Stack Software Engineering, [Brian Stanton](https://www.linkedin.com/in/brian-stanton-5aa63270/) and [Sarah Stodder](https://www.linkedin.com/in/sarah-stodder-0317b3153/) instructors.


## React + Flask

To create this first iteration of CORO, I used React.js (Vite, TypeScript) for the Front-End, Flask for the Back-End. SQLite and Postman to manage the DataBase.

Live Demo: https://coro-c0530.web.app/

If you would like to watch a short demo, and hear me sing a demo of one of my favorite choral pieces, check out this YouTube video:

[CORO - Programming App for Church Choirs](https://youtu.be/OY7DaGMgrXw?si=ZhS4kehPlP2sI3vj)

To install this on your end, follow these instructions

1. Clone both repositories

```yml
   $ git clone https://github.com/composercordero/CORO-frontend.git
   $ git clone https://github.com/composercordero/CORO-backend.git
```
2. Open the Back-End Flask App:
```md
   # Create a Virtual Environment (venv):
   $ python -m venv venv
   (if mac, python3...)

   # Install the modules in requirements.txt:
   $ pip install -r requirements.txt
   (if mac, pip3...)

   # Run the app:
   $ flask --debug run --port 8080

```
3. Now open the Front-End project

```md
   # Run the app:
   $ npm run dev

   # Open the link from your terminal in your browser:
   
   It will be something like
   http://localhost:5173/
```

## First Iteration

09/15/2023: This version is the demo, including text generated in [Neil deGrasse Tyson Ipsum](http://neilipsum.pw/). The app allow users to create an account, add hymns and research them.

## Next Iterations

I am looking forward to add many more features, such as:

- Contact form
- Bulletin and Reporting Printing (PDF)
- Hymn Suggestions based on scriptures and dates
- My Library section
- Other Hymnals besides Glory To God (Presbyterian Hymn)
- Ultimately pair this web app with an iPad application (Reason why the website is not responsive).

## Vision
The Concert Programming App that you always needed. CORO helps you plan, report, and keep your organization's repertoire up to date. Streamline your process and focus on what your rehearsals more.

## Contact
If you are interested in collaborating or have questions, please contact me at composer.cordero@gmail.com

## Muchas Gracias
With many thanks to Brian Stanton, Sarah Stodder, and the team at hymmnary.org, Dr. Harry Platinga, Will Groenendyk, and Ann Brown. 