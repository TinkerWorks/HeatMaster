#!/usr/bin/env groovy

pipeline {
    agent any

    stages {
        stage('Environment preparation') {
            steps {
                echo "... preparing python environment required for project ..."
                sh "pip3 install -r requirements.txt"
                sh "pip3 install coverage nose"
            }
        }
        stage('UnitTest') {
            steps {
                echo 'Testing..'
                sh "~/.local/bin/nosetests  HeatMaster --with-xunit"
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
