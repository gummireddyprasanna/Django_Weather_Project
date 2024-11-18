
# Deploy Django Project on AWS EC2

## 1. Prepare Your Django Project

### a. Update `settings.py`

- Set `DEBUG = False`:
  
  ```python
  DEBUG = False
  ```

- Configure `ALLOWED_HOSTS`:

  ```python
  ALLOWED_HOSTS = ['your-ec2-public-dns']
  ```

- Static and Media Files Configuration:

  ```python
  STATIC_URL = '/static/'
  STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
  MEDIA_URL = '/media/'
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
  ```

### b. Create `requirements.txt`

Generate this file that lists all your project dependencies:

```bash
pip freeze > requirements.txt
```

### c. Create a `Procfile` (Optional)

This step is optional when using Apache but useful if you switch to other deployment methods later. For now, focus on your Apache setup.

---

## 2. Launch and Configure Your EC2 Instance

### a. Launch an EC2 Instance

1. **Log in to AWS Management Console**:  
   Go to the [AWS Management Console](https://aws.amazon.com/console/).

2. **Navigate to EC2**:  
   Find EC2 under the "Compute" services.

3. **Launch an Instance**:
   - Click "Launch Instance".
   - Choose an Amazon Machine Image (AMI), such as **Amazon Linux 2 AMI**.
   - Choose an instance type, like **t2.micro** (free tier eligible).
   - Configure instance details and add storage as needed.
   - Configure the security group to allow **HTTP (port 80)** and **SSH (port 22)**.
   - Review and launch your instance. Create a key pair or use an existing one, and download the key pair file (`.pem`).

### b. Connect to Your EC2 Instance

1. **Obtain Public DNS**:  
   Find the public DNS or IP address of your instance in the EC2 console.

2. **Connect via SSH**:

   ```bash
   ssh -i /path/to/your-key.pem ec2-user@your-ec2-public-dns
   ```

---

## 3. Set Up Your Django Project on EC2

### a. Install Necessary Software

1. **Update Packages**:

   ```bash
   sudo yum update -y
   ```

2. **Install Python and Pip**:

   ```bash
   sudo yum install python3 python3-pip -y
   ```

3. **Install Apache and mod_wsgi**:

   ```bash
   sudo yum install httpd httpd-tools -y
   sudo yum install mod24_wsgi python3-mod_wsgi -y
   ```

4. **Install and Configure Virtual Environment**:

   ```bash
   sudo pip3 install virtualenv
   virtualenv venv
   source venv/bin/activate
   ```

5. **Install Project Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### b. Transfer Your Django Project to EC2

1. **Upload Your Code**:  
   Use `scp` or an SFTP client to copy your project to the EC2 instance:

   ```bash
   scp -i /path/to/your-key.pem -r /path/to/your/project ec2-user@your-ec2-public-dns:/home/ec2-user/
   ```

### c. Configure Your Django Project

1. **Navigate to Your Project Directory**:

   ```bash
   cd /home/ec2-user/your-project
   ```

2. **Apply Migrations and Collect Static Files**:

   ```bash
   python3 manage.py migrate
   python3 manage.py collectstatic --noinput
   ```

### d. Configure Apache

1. **Create an Apache Configuration File**:  
   Create a file named `/etc/httpd/conf.d/django.conf` with the following content:

   ```apache
   <VirtualHost *:80>
       ServerName your-ec2-public-dns
       DocumentRoot /home/ec2-user/your-project

       WSGIDaemonProcess your_project_name python-path=/home/ec2-user/your-project:/home/ec2-user/your-project/venv/lib/python3.7/site-packages
       WSGIProcessGroup your_project_name
       WSGIScriptAlias / /home/ec2-user/your-project/your_project_name/wsgi.py

       <Directory /home/ec2-user/your-project/your_project_name>
           <Files wsgi.py>
               Require all granted
           </Files>
       </Directory>

       Alias /static/ /home/ec2-user/your-project/staticfiles/
       <Directory /home/ec2-user/your-project/staticfiles>
           Require all granted
       </Directory>

       Alias /media/ /home/ec2-user/your-project/media/
       <Directory /home/ec2-user/your-project/media>
           Require all granted
       </Directory>

       ErrorLog /var/log/httpd/django_error.log
       CustomLog /var/log/httpd/django_access.log combined
   </VirtualHost>
   ```

2. **Start and Enable Apache**:

   ```bash
   sudo systemctl start httpd
   sudo systemctl enable httpd
   ```

---

## 4. Access and Test Your Application

1. **Open Your Application URL**:  
   Visit `http://your-ec2-public-dns` in your web browser to access your deployed Django application.


