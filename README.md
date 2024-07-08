

# ACCESS KEY MANAGER APPLICAION
## Project Objective
Micro-Focus Inc., a software company has built a school management platform that is
multitenant allowing various schools can set up on the platform as though the platform was
built specifically for them. They have decided to use an access key-based approach to
monetize it rather than building payment features into the school software. 

## Customer Requirements
### School IT Personnel
1. <b>Signup and Login</b>: Includes signup & log in with an email and password with account verification.
2. <b>Password Recovery</b>: Includes Password reset feature to recover lost passwords
3. Can see a list of all access keys granted: active, expired or revoked.
4. For each access key, the personnel can be able to see the status, date of
procurement and expiry date.
5. A user can not be able to get a new key if there is an active key already assigned to
him/her. Only one key can be active at a time.

## Micro-Focus Admin
1. <b>Signup and Login</b>:Can be able to log in with an email and password.
2. <b>Rvoke Key</b>: Can be able to manually revoke a key
3. <b>List of Keys</b>: Can be able to see all keys generated on the platform and see the status, date of procurement and expiry date.
5. <b>Endpoint For Integration</b>:Can be able to access an endpoint, such that if the school email is provided, the
endpoint should return status code 200 and details of the active key if any is found, else
it should return 404. This is to enable them to integrate their school software with your
key manage

## FEATURES
1. User authentication (signup, login, password recovery)
2. Access key management for school IT personnel
3. Admin functionalities for managing and viewing access keys
4. Integration endpoint for checking active keys

## TECHNOLOGIES USED
1. <b>Django</b>: Web framework for building the application
2. <b>PostgreSQL</b>: Database for storing user and key information

## DEPLOYED SITE: https://asanteprince.pythonanywhere.com/

## INSTALLATION
1. git clone the repository:
    ```bash
    git clone https://github.com/protoncodecoin/Access-Key-Manager.git
    cd access-key-manager
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser for accessing the admin site:
    ```bash
    python manage.py createsuperuser
    ```

6. Create two Groups (MicroAdmin and Personnel) in the admin pannel to assign staffs and personnels respectively.
     - Permission for MicroAdmin: can view access key
     - Permission for Personnel: can add access key
  
7. Set up all environment variables

8. Run the development server:
    ```bash
    python manage.py runserver
    ```
