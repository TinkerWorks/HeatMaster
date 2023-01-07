#!/usr/bin/env groovy

String daily_cron_string = BRANCH_NAME == "master" ? "@daily" : ""

pipeline {
    agent {
        kubernetes {
            yamlFile 'kubepods.yaml'
            defaultContainer 'python'
        }
    }
    options {
        timeout(time: 10, unit: 'MINUTES')
    }

    triggers { cron(daily_cron_string) }

    stages {
        stage('flake8') {
            steps{
                container('flake8') {
                    sh "flake8"
                }
            }
        }

        stage('pylint duplication') {
            steps{
                container('pylint') {
                    sh "pylint --disable=all --enable=duplicate-code homesensorhub"
                }
            }
        }

        stage('... Environment preparation ...') {
            steps {
                echo "... preparing python environment required for project ..."
	            sh "pip install -r requirements.txt"
                sh "pip install -r tests/requirements.txt"
            }
        }
        stage('UnitTest') {
            steps {
                ansiColor('xterm') {
                    echo '... Testing ...'
                    sh "nose2 --with-coverage --junit-xml"
                }
            }
            post {
                always {
                    junit 'nose2-junit.xml'
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
