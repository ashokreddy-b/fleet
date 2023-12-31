pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'my-django-app'
        DOCKER_IMAGE_TAG = 'latest'
    }
    
    stages{
        stage('Checkout from code from github')
        {
            steps{
                git branch: 'main', url: 'https://github.com/ashokreddy-b/fleet.git'
                sh 'echo "Checkout successfully"'
            }
            
        }
        stage('Build the Application')
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
           // sh 'sudo apt install libpq-dev'
                   sh'pip install psycopg2-binary'
            sh 'pip install -r requirements.txt'
            // Run Django collect static files
            sh "${venvPath}/bin/activate && python3 manage.py collectstatic --noinput"
                }
               
              
            }
        }
        stage('Create Docker Image')
        {
            steps{
                sh 'sudo docker build -t bapathuashokreddy/my-django-app:latest .'
            }
        }
        stage('Docker hub login and push Image to docker hub')
        {
            steps{
                withCredentials([usernamePassword(credentialsId: 'Docker', passwordVariable: 'pwd', usernameVariable: 'username')]) {
                    sh "sudo docker login -u ${env.username} -p ${env.pwd}"
                    sh 'sudo docker push bapathuashokreddy/my-django-app:latest'
                }
                
            }
        }
        stage('Run the container')
        {
            steps{
               sh  'sudo docker run -d -p 8000:8000 bapathuashokreddy/my-django-app:latest'
            }
        }
    }
     post {
        success {
            emailext (
                subject: "Fleet Pipeline Status: ${currentBuild.currentResult}",
                body: "The build status is: ${currentBuild.currentResult}",
                recipientProviders: [[$class: 'CulpritsRecipientProvider']],
                to: "bapathu.ashokreddy@avinsystems.com" 
            )
        }
         failure {
            // This stage will always run, regardless of the build result
            emailext (
                subject: "Fleet Pipeline Status: ${currentBuild.currentResult}",
                body: "The build status is: ${currentBuild.currentResult}",
                recipientProviders: [[$class: 'CulpritsRecipientProvider']],
                to: "bapathu.ashokreddy@avinsystems.com"  // Replace with the recipient's email address
            )
        }
    }
}
