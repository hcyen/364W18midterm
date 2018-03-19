**What this app is about?**

Pretend we are a headhunter company – the objective is to help businesses find good employees to fill positions, as well as helping people find good jobs in companies. Part of our service entails having a database to store people’s names, companies, and industries in which the companies fall into, as well as the information of employees, and the information of positions to be filled.

This application uses Yelp API (required: pip install yelpapi), to allow user to search the best five businesses given a business category, city, and state. It will display the top five businesses, as well as their respective names, phone numbers, addresses, and Yelp business web URLs.

It also creates tables for names, industries, companies, and employees in the postgresql database: hcyenmidtermdb_1

It allows the user to add name (duplicated data allowed).

It allows the user to add company and the industry it falls into. (duplicated data is not allowed)

It allows the user to add employee, the company the employee works for, and the position in the company only if the company is in the database already. If the company is not in the database yet, it will display the company form to allow you to add the company first. (duplicated data is not allowed)

It provides links to display all the names in the names table, all the employees in the employees table, all the companies in the companies table, and all the industries in the industries table.

The industries and companies tables have a one to many relationship.
Likewise, the companies and employees tables have a one to many relationship. 

A list of all of the routes that exist in the app and the names of the templates each one should render.
	/ -> base.html
	/names -> name_example.html
	/yelp_search -> yelp_search.html
	/yelp_result -> list.html
	/company -> company.html
	/employee -> employee.html
	/all_employees -> all_employees.html
	/all_companies -> all_companies.html
	/all_industries -> all_industries.html

Requirements to complete for 1800 points (90%) -- an awesome, solid app
(I recommend treating this as a checklist and checking things off as you get them done!)
Documentation Requirements (so we can grade the assignments)
•	Note: See To Submit for submission instructions.
•	Create a README.md file for your app that includes the full list of requirements from this page. The ones you have completed should be bolded. (You bold things in Markdown by using two asterisks, like this: **This text would be bold** and this text would not be)
•	The README.md file should include a list of all of the routes that exist in the app and the names of the templates each one should render (e.g. /form -> form.html, like the list we provided in the instructions for HW2).
•	The README.md file should contain at least 1 line of description of what your app is about or should do.
Code Requirements
Note that many of these requirements go together!
•	  **Ensure that the SI364midterm.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up)**
•	  **Add navigation in base.html with links (using a href tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, like this )**
•	  **Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.** 
The provided code for base.html has the block content1, I added block content to display the html page name and its purpose. When the child templates inherit base.html, I overwrote and filled in the details. http://flask.pocoo.org/docs/0.12/patterns/templateinheritance/ https://stackoverflow.com/questions/31613507/jinja-doesnt-render-anything-when-extending-layout-template
Jinja doesn't let child templates output anything that isn't in a parent template block. (In other words, block names must match.)

•	  **Include at least 2 additional template .html files we did not provide.**
I provided 7 additional template html files: yelp_search.html, list.html, company.html, employee.html, all_employees.html, all_companies.html, and all_industries.html

•	  **At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.
These could be in the same template, and could be 1 of the 2 additional template files.**
For loop is in all of the templates except yelp_search.html, 
If condition is in list.html, company.html, employee.html, all_employees.html, all_companies.html, and all_industries.html

•	  **At least one errorhandler for a 404 error and a corresponding template.**
404.html is provided in the template directory.
•	  **At least one request to a REST API that is based on data submitted in a WTForm.** 
Yelp Business Search API is used in the app.
•	  **At least one additional (not provided) WTForm that sends data with a GET request to a new page.**
 	Yelp_search.html sends data with a GET request.

•	  **At least one additional (not provided) WTForm that sends data with a POST request to the same page.**
Company.html and employee.html both send data with a POST request to the same page.

•	  **At least one custom validator for a field in a WTForm.**
custom validator - validate_employee_name is used in WTForm - EmployeeForm

•	  **At least 2 additional model classes.**
I added 3 additional model classes - Industry, Company, and Employee

•	  **Have a one:many relationship that works properly built between 2 of your models.**
Industry:Company  has a one:many relationship
Company:Employee has a one:many relationship

•	  **Successfully save data to each table.**
The data are successfully saved in names, industries, companies, and employees tables

•	  **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).**
In the helper functions: get_or_create_industry, get_or_create_company, get_or_create_employee, we successfully query data for one column.
In the view functions: all_names, company, view_all_employees, see_all_companies, and see_all_industries, we successfully query all data.

•	  **Query data using an .all() method in at least one view function and send the results of that query to a template.**
all_names, view_all_employees, see_all_companies, and see_all_industries are using an .all() method and send the results of that query to templates.

•	 ** Include at least one use of redirect. (HINT: This should probably happen in the view function where data is posted...)**
The view functions – home, company, employee have redirect

•	  **Include at least one use of url_for. (HINT: This could happen where you render a form...)**
The view functions – home, company, employee have url_for
The template files – base.html, yelp_search.html, company.html, all_industries.html, employee.html, all_companies.html, and all_employees.html have url_for

•	  **Have at least 3 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of base.html.)**
We have yelpsearch, resultyelp, company, employee, view_all_employees, see_all_companies, see_all_industries not provided in the code.
Additional Requirements for an additional 200 points (to reach 100%) -- an app with extra functionality!

•	**(100 points) Include an additional model class (to make at least 4 total in the application) with at least 3 columns. Save data to it AND query data from it; use the data you query in a view-function, and as a result of querying that data, something should show up in a view. (The data itself should show up, OR the result of a request made with the data should show up.)**
We have total 4 model classes: Name, Industry, Company, and Employee.
The Company Model has 3 columns and the Employee Model has 4 columns.
Data has been successfully saved in those tables. In the helper functions and most of the view functions, like company and employee, we query data from the models/tables.  The view_all_employees and view_all_companies view functions rendering the all_employees.html and all_ companies.html show the data.

•	**(100 points) Write code in your Python file that will allow a user to submit duplicate data to a form, but will not save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3).**
When you enter the company and industry form, if the company is new but the industry already exists in the database, it will save the company but not the industry. Likewise, when you enter the employee form, the employee is saved but not the company.

