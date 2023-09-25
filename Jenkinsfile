pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'my-django-app'
        DOCKER_IMAGE_TAG = 'latest'
    }
    
    stages{
        stage('Checkout')
        {
            steps{
                git branch: 'main', url: 'https://github.com/ashokreddy-b/fleet.git'
                sh 'echo "Checkout successfull"'
            }
            
        }
        stage('Build')
        {
            steps
            {
                sh '''
                    python3 -m venv venv
                    chmod +x venv/bin/activate 
                    ./venv/bin/activate
                '''

                // Install dependencies and run migrations
                sh 'pip install -r requirements.txt'
                sh 'pip install django'
                sh'pip install psycopg2-binary'
                sh 'export DJANGO_SETTINGS_MODULE=mysite.settings'
                sh 'python3 manage.py makemigrations'
              //  sh 'python3 manage.py reset_db'
                //sh 'python3 manage.py migrate'

                // Run any additional build steps here, such as collecting static files
              //  sh 'python3 manage.py collectstatic'
              //  sh 'deactivate'
              
            }
        }
        stage('Image Create')
        {
            steps{
                sh 'sudo docker build -t bapathuashokreddy/my-django-app:latest .'
            }
        }
        stage('push Image to docker hub')
        {
            steps{
                withCredentials([usernamePassword(credentialsId: 'Docker', passwordVariable: 'pwd', usernameVariable: 'username')]) {
                    sh "sudo docker login -u ${env.username} -p ${env.pwd}"
                    sh 'sudo docker push bapathuashokreddy/my-django-app:latest'
                }
                
            }
        }
        stage('Deploy')
        {
            steps{
               sh  'sudo docker run -d -p 8000:8000 bapathuashokreddy/my-django-app:latest'
            }
        }
    }
}
