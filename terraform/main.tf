# Security Group
resource "aws_security_group" "airsense_sg" {

  name        = "airsense-sg"
  description = "Allow SSH and Streamlit access"

  ingress {
    description = "SSH Access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Streamlit Access"
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "AirSense-Security-Group"
  }
}

# EC2 Instance
resource "aws_instance" "airsense_ec2" {

  ami           = "ami-0a1b0c508e1fa9fce"   # Ubuntu 22.04 (ap-south-1)
  instance_type = var.instance_type
  key_name      = var.key_name

  associate_public_ip_address = true

  vpc_security_group_ids = [
    aws_security_group.airsense_sg.id
  ]

  root_block_device {
    volume_size = 30
    volume_type = "gp2"
  }

  user_data = <<-EOF
#!/bin/bash

# Update packages
apt update -y

# Install Docker
apt install docker.io -y

# Start Docker
systemctl start docker
systemctl enable docker

# Pull AirSense Docker image
docker pull mehrcreates/airsense-app:latest

# Remove old container if exists
docker rm -f airsense-container || true

# Run container
docker run -d \
  --name airsense-container \
  -p 8501:8501 \
  mehrcreates/airsense-app:latest

EOF

  tags = {
    Name = "AirSense-EC2"
  }

}
