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
               sh 'python3 -m venv venv'
                sh 'chmod +x /var/lib/jenkins/workspace/DjangoApplicationPipeline/venv/bin/activate'
                sh 'venv/bin/activate'
                sh 'pip install -r requirements.txt'
                sh 'python3 manage.py collectstatic --noinput'
                sh 'deactivate'
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
