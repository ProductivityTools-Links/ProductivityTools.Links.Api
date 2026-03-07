pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                echo 'Hello from ProductivityTools.Links.Api Pipeline!'
            }
        }

        stage('Identify User') {
            steps {
                script {
                    echo "Checking Jenkins user..."
                    
                    echo "Username (whoami):"
                    sh 'whoami'

                    echo "User details (id):"
                    sh 'id'

                    echo "Finished user identification."
                }
            }
        }

        stage('deleteWorkspace') {
            steps {
                deleteDir()
            }
        }

         stage('clone') {
            steps {
                // Get code from the GitHub repository
                git branch: 'main',
                url: 'https://github.com/ProductivityTools-Links/ProductivityTools.Links.Api.git'
            }
        }

        stage('stop application') {
            steps {
                script {
                    echo "Stopping application"
                    // Adjust 'links-api' to match the actual name of your systemd service
                    sh 'sudo systemctl stop links-api || true'
                }
            }
        }

        stage('Deploy and Build in /opt/PT.Links.Api') {
            steps {
                script {
                    echo "Deploying files and installing dependencies to /opt/PT.Links.Api"
                    sh '''
                        umask 002
                        
                        # Ensure the target directory exists
                        mkdir -p /opt/PT.Links.Api
                        
                        # Copy project files to the target directory 
                        # Using rsync helps exclude unnecessary files like .git or __pycache__
                        rsync -avq --exclude='.git/' --exclude='venv/' --exclude='__pycache__/' ./ /opt/PT.Links.Api/
                        
                        # Switch to the target directory
                        cd /opt/PT.Links.Api
                        
                        # Create a virtual environment if it doesn't already exist
                        python3 -m venv venv
                        
                        # Install required packages
                        ./venv/bin/pip install -r requirements.txt
                    '''
                }
            }
        }
        
        stage('start application') {
            steps {
                script {
                    echo "Starting application"
                    // Adjust 'links-api' to match the actual name of your systemd service
                    sh 'sudo systemctl start links-api'
                }
            }
        }
    }
}
