pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "mehrcreates/airsense-app:latest"
        AWS_ACCESS_KEY_ID = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
        EC2_HOST = "65.0.85.64"
        EC2_USER = "ubuntu"
        EC2_KEY = "airsense-key"
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
                    docker logout || true

                    echo "$DOCKER_PASS" | docker login \
                        -u "$DOCKER_USER" \
                        --password-stdin

                    docker buildx create --use || true

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

        withCredentials([
            sshUserPrivateKey(
                credentialsId: 'ec2-ssh-key',
                keyFileVariable: 'SSH_KEY'
            )
        ]) {

            sh '''
            echo "Deploying on EC2..."

            ssh -o StrictHostKeyChecking=no \
                -i $SSH_KEY \
                ubuntu@65.0.85.64 << EOF

            docker pull mehrcreates/airsense-app:latest

            docker stop airsense-app || true
            docker rm airsense-app || true

            docker run -d \
                -p 8501:8501 \
                --name airsense-app \
                mehrcreates/airsense-app:latest

            EOF
            '''
        }
    }
}

    }
}