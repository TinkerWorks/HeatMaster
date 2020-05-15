#!/usr/bin/env groovy

pipeline {
    agent any

    stages {
        stage('Environment preparation') {
            steps {
                echo "... preparing python environment required for project ..."
                sh "pip3 install -r requirements.txt"
            }
        }
        stage('Build') {
            steps {
                echo 'Building not required in python ..'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
