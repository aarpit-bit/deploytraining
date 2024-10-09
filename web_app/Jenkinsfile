pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t myflaskapp .'
            }
        }
        stage('Push Docker Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_HUB_PASSWORD', usernameVariable: 'DOCKER_HUB_USERNAME')]) {
                    sh 'docker tag myflaskapp:latest $DOCKER_HUB_USERNAME/myflaskapp:latest'
                    sh 'docker login -u $DOCKER_HUB_USERNAME -p $DOCKER_HUB_PASSWORD'
                    sh 'docker push $DOCKER_HUB_USERNAME/myflaskapp:latest'
                }
            }
        }
        stage('Deploy to EC2') {
            steps {
                sshagent(credentials: ['ec2-ssh-key']) {
                    sh 'ssh -o StrictHostKeyChecking=no ubuntu@ec2-instance-ip "docker stop myflaskapp || true && docker rm myflaskapp || true"'
                    sh 'ssh -o StrictHostKeyChecking=no ubuntu@ec2-instance-ip "docker run -d -p 5000:5000 $DOCKER_HUB_USERNAME/myflaskapp:latest"'
                }
            }
        }
    }
}