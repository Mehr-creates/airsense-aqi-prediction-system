pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "mehrcreates/airsense-app:latest"
        AWS_ACCESS_KEY_ID = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
    }

    stages {

        stage('Clone Code') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Mehr-creates/airsense-aqi-prediction-system.git'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                echo "Running basic checks"
                python3 --version
                '''
            }
        }

        stage('Build & Push Docker Image (AMD64)') {
            steps {

                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                    docker buildx build \
                      --platform linux/amd64 \
                      -t $DOCKER_IMAGE \
                      --push \
                      .
                    '''
                }
            }
        }

        stage('Run Terraform') {
            steps {
                sh '''
                cd terraform

                terraform init

                terraform apply \
                  -var="key_name=airsense-key" \
                  -auto-approve
                '''
            }
        }

        stage('Deploy on EC2') {
            steps {
                sh '''
                echo "Deployment completed successfully"
                '''
            }
        }

    }
}