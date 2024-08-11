# Overview #

The **AirBnB clone - The console** is the starting point of building the first full web application - a clone of AirBnB. Here, we:<br/>
- put in place a parent class (called BaseModel) to take care of the initialization, serialization and deserialization of your future instances
- create a simple flow of serialization/deserialization: Instance <-> Dictionary <-> JSON string <-> file
- create all classes used for AirBnB (User, State, City, Place…) that inherit from BaseModel
- create the first abstracted storage engine of the project: File storage
- create all unittests to validate all our classes and storage engine, and
- buid a console to interact with our our objects from the command line. The console will enable us to:
  - create a new object (ex: a new User or a new Place)
  - retrieve an object  or all objects from our storage (file or database)
  - do operations on objects like count, compute, etc
  - update attributes of an object
  - destroy an object

## What is AirBnB_clone_v4? ##
It's the fourth step in buiding our [AirBnb_clone](). In this step of the journey, we add we make our project to load data from our database so it's dynamic. The features it adds are as follows:
- First

<br/>
## The Console Explained ##
### How to Use ###
1. Clone repository to your local machine
2. `cd` into repository.
```
e.g.
$ cd /AirBnB_clone
```
3. Once inside the cloned repository, locate the "console.py" file and run it as follows:
```
/AirBnB_clone$ ./console.py
```
4. When this command is run, this prompt would appear
```
(hbnb)
```
5. The prompt shows you are in the "HBnB" console.
There are a variety of commands available within the console program.

### Commands ###
| COMMAND | DESCRIPTON                | USAGE                 | EXAMPLE
|---------|---------------------------|-----------------------|-----------------------------|
| `create` | Creates new instance of a given class<br/><ul><li>prints `id` fo class if operation was successful</li><li>prints an error message on error</li></ul> | `create <class_name>` | `create User` |
| `destroy` | Destroys an object by its `class` and `uuid`<br/></ul><li>prints nothin on success.</li><li>prints error message on failure</li></ul> | `destroy <class> <uuid>` | `delete User 0963d9b6-981c-488d-9c96-3c0208e39715` |
| `show`  | Shows an object based on class and UUID<br/><ul><li>prints string representation of <class> instance matching <uuid></li><li>prints error message if no match is found</li></ul> | `show <class> <uuid>`<br/>Alternative Syntax:<br/>`<class>.show(<uuid>)` | `show User 0963d9b6-981c-488d-9c96-3c0208e39715`<br/>`User.show(0963d9b6-981c-488d-9c96-3c0208e3971)` |
| `all` | Shows all instances of:</br/><ul><li> all objects of <class> in storage<li><li>all instances of all objects in storage</li></ul> | `all [<class>]`</br>Alternative Syntax:<br/>`<class>.all()` |`all User`<br/>`all`<br/>`User.all()` |
| `update` | Updates existing attributes of an object based on its <class> and <uuid> | `update <class> <attr> <value>`<br/><ul><li>where `value` contains a space, it should be wrapped in quotes: `\' or \"` </li><li>prints nothing on success</li><li>prints error message if error occurs</li><li>can also be called on the <class> itself</li></ul> | `update User 61327bb5-1e2b-4b4e-9c47-ba6f0222bdb8 name Nameless`</br/>`User.update(61327bb5-1e2b-4b4e-9c47-ba6f0222bdb8, name Nameless)` |
| `quit` | Exits the program<ul><li>`EOF` does the same</li></ul> | `quit` | `quit` |

<hr />
<br/>
### Examples
#### Main Commands Syntax

###### Example 0: Create an object
Usage: create <class_name>
```
(hbnb) create State
```
```
(hbnb) create State
3aa5babc-efb6-4041-bfe9-3cc9727588f8
(hbnb)
```
###### Example 1: Show an object
Usage: show <class_name> <_id>

```
(hbnb) show State 3aa5babc-efb6-4041-bfe9-3cc9727588f8
[State] (3aa5babc-efb6-4041-bfe9-3cc9727588f8) {'id': '3aa5babc-efb6-4041-bfe9-3cc9727588f8', 'created_at': datetime.datetime(2020, 2, 18, 14, 21, 12, 96959), 
'updated_at': datetime.datetime(2020, 2, 18, 14, 21, 12, 96971)}
(hbnb)
```
###### Example 2: Destroy an object
Usage: destroy <class_name> <_id>
```
(hbnb) destroy State 3aa5babc-efb6-4041-bfe9-3cc9727588f8
(hbnb) show State 3aa5babc-efb6-4041-bfe9-3cc9727588f8
** no instance found **
(hbnb)
```
###### Example 3: Update an object
Usage: update <class_name> <_id>
```
(hbnb) update User b405fc64-9724-498f-b405-e4071c3d857f first_name "person"
(hbnb) show User b405fc64-9724-498f-b405-e4071c3d857f
[User] (b405fc64-9724-498f-b405-e4071c3d857f) {'id': 'b405fc64-9724-498f-b405-e4071c3d857f', 'created_at': datetime.datetime(2020, 2, 18, 14, 33, 45, 729889), 
'updated_at': datetime.datetime(2020, 2, 18, 14, 33, 45, 729907), 'first_name': 'person'}
(hbnb)
```
<hr/>

#### Alternative Commands Syntax ####
###### Example 0: Show all User objects
Usage: <class_name>.all()
```
(hbnb) User.all()
["[User] (99f45908-1d17-46d1-9dd2-b7571128115b) {'updated_at': datetime.datetime(2020, 2, 19, 21, 47, 34, 92071), 'id': '99f45908-1d17-46d1-9dd2-b7571128115b', 'created_at': datetime.datetime(2020, 2, 19, 21, 47, 34, 92056)}", "[User] (98bea5de-9cb0-4d78-8a9d-c4de03521c30) {'updated_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134362), 'id': '98bea5de-9cb0-4d78-8a9d-c4de03521c30', 'created_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134343)}"]
```

###### Example 1: Destroy a User
Usage: <class_name>.destroy(<_id>)
```
(hbnb) User.destroy("99f45908-1d17-46d1-9dd2-b7571128115b")
(hbnb)
(hbnb) User.all()
(hbnb) ["[User] (98bea5de-9cb0-4d78-8a9d-c4de03521c30) {'updated_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134362), 'id': '98bea5de-9cb0-4d78-8a9d-c4de03521c30', 'created_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134343)}"]
```
###### Example 2: Update User (by attribute)
Usage: <class_name>.update(<_id>, <attribute_name>, <attribute_value>)
```
(hbnb) User.update("98bea5de-9cb0-4d78-8a9d-c4de03521c30", name "Todd the Toad")
(hbnb)
(hbnb) User.all()
(hbnb) ["[User] (98bea5de-9cb0-4d78-8a9d-c4de03521c30) {'updated_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134362), 'id': '98bea5de-9cb0-4d78-8a9d-c4de03521c30', 'name': 'Todd the Toad', 'created_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134343)}"]
```
###### Example 3: Update User (by dictionary)
Usage: <class_name>.update(<_id>, <dictionary>)
```
(hbnb) User.update("98bea5de-9cb0-4d78-8a9d-c4de03521c30", {'name': 'Fred the Frog', 'age': 9})
(hbnb)
(hbnb) User.all()
(hbnb) ["[User] (98bea5de-9cb0-4d78-8a9d-c4de03521c30) {'updated_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134362), 'name': 'Fred the Frog', 'age': 9, 'id': '98bea5de-9cb0-4d78-8a9d-c4de03521c30', 'created_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134343)}"]
```
<br/>

## Folder Details ###
- **Date Created:** Mar 4 2024.
- **Authors:**
	- [William Inyam](https.//github.com/thecypherzen)
- **Project Timeline:**
  - **Released:** Aug 8, 2024 - 6am.
  - **1st Deadline:** Aug 12, 2024 - 6am.
  - **Duration:** 4 days.


<br/>

## File Tree ##
Coming soon

<br/>

## Technologies ##
- All files written using using python3 (version 3.8.5)
- File types can be identified by their extensions
- Code tested on Ubuntu 20.04 LTS.

<br/>

## Files###
- *Here is a detailed list of all files in the repo and their description*.

| SN | File            | Description                                        |
|----|-----------------|----------------------------------------------------|
| 1. | [console.py](https://github.com/thecypherzen/) | The HBNB command line interpreter program |
| 2. | [genauthors.sh]() | A script that generates 'Authors File' for a repository. |
| 3. | [AUTHORS]() | The repo authors' file. Contains info of all contributors to this repo. |
| 4. | [models]() | Package of all modules that define object classes. |
| 5. | [tests]() | Package of all modules that define unittests. |
| 6. | [web_static]() | Folder containing all HBNB static files for the web |
| 7. | [api]() | Api definition for our AirBnB_clone.
