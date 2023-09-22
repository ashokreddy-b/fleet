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

                // Run any additional build steps here, such as collecting static files
                sh 'python3 manage.py collectstatic --noinput'
              
            }
        }
        stage('Image Create')
        {
            steps{
                script {
                    docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}")
                }
            }
        }
        stage('push Image to docker hub')
        {
            steps{
                withCredentials([usernamePassword(credentialsId: 'Docker', passwordVariable: 'pwd', usernameVariable: 'username')]) {
                    sh "docker login -u ${env.username} -p ${env.pwd}"
                    sh 'docker push "${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"'
                }
            }
        }
        stage('Deploy')
        {
            steps{
               sh  'docker run -d -p 8000:8000 "${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"'
            }
        }
    }
}
