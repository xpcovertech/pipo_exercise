# Pipo Saúde Exercise

[Pipo](https://www.piposaude.com.br/) is a Brazilian Startup in the healthcare industry with the bold goal of revolutionizing people's experience with health services. As part of their hiring process, they ask potential software engineers to develop a solution to two of their main challenges: procurement process flow and data management. The goal of the solution I've developed is to address those two challenges through a simplified workflow for their clients' HR person and a lean data structure for Pipo. The code is the bridge between those two things.

This system would be used by HR people at corporations in charge of managing employee's benefits. Each provider requires different information at enrollment and employees might switch benefits at different times. In short, everything can change at any time. From the type of data (information) the provider requires, to the employee's data in the database.

DISCLAIMER: Pipo did not ask me to develop a solution as complete as this. They are very open and accomodating as to what part of the solution you'd like to develop and how long do you'd need to do it. In hindsight, I know I could have focused more on input checking for example, but I chose to take a "bird's eye view" approach. It was my own choice to develop this. 


## Motivation

Besides getting hired ;), my main motivation was to find the most effective way to solve a real-world problem. As I mentioned to them, I've had my own share of problems with health insurance companies and their not-so-smart way of doing things. Those two things were enough to motivate me through the development of this solution. 

I've decided to use Python because of my familiarity with the language and speed in prototyping. For a large-scale platform such as Pipo’s, Python and SQL would not be an efficient solution for deployment. 


## Workflow & Usage

*For this solution I've only focused on people and benefits management. In a real-world situation, there should also be profiles for companies and providers. For simplicity's sake, I've decided to forgo those two. Therefore, there's no "admin" management and no way to register new companies through the platform. That can be done only thru the bash script in the setup folder. See below for more information.*

*Glossary:
A person is every employee registered in the database. 
The benefit is the name of any type of benefit plan. Ex. Health Insurance.
The company is an employer of people that have benefits registered to them, allowing people to be enrolled in those benefits.
Type of data is the type of information that a benefit plan requires from a person at enrollment. Ex. Date of Birth*

Here is how it works and some of my software design choices told as a story. 

![Homepage after login](/documents/index.png)

HR person from "Wonka Industries" can log in with their CPF number and choose either **People** or **Benefits** on the menu. Both will lead to the "same destination", but from very different perspectives. On the **People** link, they can choose to register, search or see a list of all registered employees. At registering they only need to input the employee's name and their CPF (Brazilian "ID" number). On the same page, they can choose to sign up to a benefit plan by selecting from a list of registered benefits. They can also choose to register the employee without selecting any benefits. Flexibility is key here. 

If they selected one or more benefits, they will be taken to another page where the combined data necessary for enrollment is shown. The goal here is to avoid duplicates and unnecessary work. One form for all the benefits selected. Once that information is filled out and sent, everything is done. 

Until, as it usually goes, something changes.

Once the HR person (I'll call them user, from here on) selects an employee either from the list or through the search page, they are taken to the employee's profile where they can see and edit their benefits and additional data (information required when they signed up for a benefit). 

If the user wishes to enroll the employee in a new benefit (or more), they can do so by clicking on a checkbox. Once submitted the user is taken to another page where they can add any new data (if required by the new benefit plan) or update anything that might need to be updated. Only data needed for enrollment in the new plan (or new plans) is shown on the screen. 

![Enrollment of existing employee in a new benefit](/documents/registering_benefit.png)

Data such as Name and CPF cannot be changed. The same goes for Date of Enrollment, which is generated automatically as a timestamp once the user is registered to a new benefit. Some data should be easy to be changed, others shouldn't. The other data necessary for enrollment, if in the database, is preloaded on each respective field. The idea here is to avoid typing and human errors. 

On the same page, and at the same time, the selection of a new benefit happens the user can unenroll an employee from a benefit plan. If they do so, the information stays on the database. The data is "attached" to the employee and not the benefit plan. The benefit can simply "see" that information when it requests it at enrollment. 

The data stays there for as long as the employee is with the company. The data is only deleted if and when, the employee's "profile" is deleted. Then all data is deleted, included those additional ones. The data science enthusiast in me hates this idea, but I've decided to move towards that direction for privacy policy reasons. 

On the **Benefits** link, the user can register a new benefit, search or see a list of all registered benefits offered by their employer. The same way an HR person using the platform can only see their company employees, they can only see their own benefit plans. 

On the benefit plan profile page, they can see and edit a list of the required data for enrollment and a list of current employees enrolled in that benefit plan. Once the employee's name is clicked, the employee's "registration form profile" (ficha de cadastro) is shown on the screen. On this page, which can be also accessed from the employee's profile, is where **employee data** and **benefit plan** meet. Not so much in the database. A pdf of the database schema (in Portuguese, sorry) is in the documentation folder if you want to take a look at it. 

![Employee's registration form with a notification that the benefit requires new data](/documents/benefit_registration_form_with_notification.png)

Now, let's say a benefit plan now asks for the employee's zodiac sign. All the user has to do is go on the profile of the (exoteric) benefit plan, click on edit types of data and see if that type is already registered on the platform. I said on the platform because all types of data are shared across all plans and companies on the platform. This way the user doens't have to type Date of Birth every single time he is registering a new benefit that requires that information. This way it's also easier to keep the database more organized and avoids duplicates. Duplicates are evil and eat resources. 

The whole schema was designed trying to find the right balance between too much code (read too much processing) and too much data (read storage). I think I learned more in favor of more code in order to have a prettier schema. And yes, I know the code could be much shorter. It's on the To-do list below. ;)

Back to the story, if no benefit plan has ever asked for the employee’s zodiac sign, the user can add that information on the "Add New Type of Data" form. There they can type the name of the type of data the benefit plan is asking for (Zodiac Sign) and they can (and should) also type an example. Examples are important in filling out forms. In this case, the user can type something like "Ex. Aries, Taurus, Gemini..." And that's it. Done. 

I believe the in order to solve complex problems you need a combination of design, communication, and technology. It is necessary to understand why people behave the way they do, and apply technology to it to either enforce that behavior or redirect it. For example, the simple act of having an example written on the screen before the human has to fill out a form field does this at a very low cost. 

I really enjoyed developing this solution and thinking through its challenges. I'm grateful for the opportunity. 

PS: There are more screenshots available in the Documents folder. 

## Running it

To play around with the platform, simply make sure you have the requirements installed and clone the project.

In termintal, inside the setup folder run:
```bash
./setup.sh
```
or
```bash
bash setup
```

This way you'll have a pre-populated database with information for three users and employees from three fictitious companies.

To log in as:

:: Wonka Industries use CPF 230.841.911-31.

:: Tio Patinhas Bank use CPF 985.105.727-47

:: Acme Co use CPF 985.105.727-47

I recommend using [Gerador de CPF](https://www.geradorcpf.com/) to generate new CPFs if you want to create new users. This is needed because of the CPF checker/validator. 


## Technologies

  - Python 3.9.2
  - SQLite 3.32.3
  - SQLAlchemy 1.4.7
  - Flask 1.1.2
  - Jinja 2.11.3
  - Bootstrap 4

 
## Todo
  
  - Refactor, refactor and refactor. Some functions and SQL queries can be split into two, others combined. As I've heard before but related to art: "You never finish an art piece, you give up on it." 
  - Unit testing. Even though I did my best to test the functions, I feel like I needed to do more unit tests to make sure it won't crash. 
  - Implement a robust input checking algorithm for the most common types of data / information. 
  - Implement some form of authentication and/or security measures.




