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
            environment {
                PYTHONPATH = "${env.WORKSPACE}/HeatMaster/test/mock"
            }
            steps {
                ansiColor('xterm') {
                    echo 'Testing..'
                    sh "env"
                    sh "~/.local/bin/nosetests  HeatMaster --with-xunit"
                }
            }
            post {
                always {
                    junit 'nosetests.xml'
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
