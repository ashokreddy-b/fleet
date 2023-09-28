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
                sh 'echo "Checkout successfully"'
            }
            
        }
        stage('Build')
        {
            steps
            {

                script {
                    def pythonVersion = '3'  // Modify the Python version as needed
                    def virtualenvName = 'myenv'  // Modify the virtual environment name as needed

                    def venvPath = "${WORKSPACE}/${virtualenvName}"

            // Create a virtual environment
            sh "python${pythonVersion} -m venv ${venvPath}"

            // Activate the virtual environment and install dependencies
            sh "chmod +x ${venvPath}/bin/activate"
            sh "${venvPath}/bin/activate"
            sh 'sudo apt install libpq-dev'
            sh 'sudo apt install libpq-dev libpq5 libssl-dev'
                    sh 'pip install -r requirements.txt'
            // Run Django collect static files
            sh "${venvPath}/bin/activate && python3 manage.py collectstatic --noinput"
                }
               
              
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
