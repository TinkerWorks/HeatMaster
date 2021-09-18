#!/usr/bin/env groovy

pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
metadata:
  label: pythontest
  namespace: jenkins
spec:
  containers:
  - name: pythontest
    image: python:latest
    command:
    - sleep
    args:
    - infinity
'''
            defaultContainer 'pythontest'
        }
    }

    stages {
        stage('... Environment preparation ...') {
            steps {
                echo "... preparing python environment required for project ..."
	            sh "pip install -r requirements.txt"
                sh "pip install -r tests/requirements.txt"
                sh "make prepare-test"
            }
        }
        stage('UnitTest') {
            steps {
                ansiColor('xterm') {
                    echo '... Testing ...'
                    sh "make nosetest"
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
