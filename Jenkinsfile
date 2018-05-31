// Hudya Lib Deployment Jenkinsfile

@Library('hudya-jenkins') _


pipeline {
  agent any

  options {
    disableConcurrentBuilds()
  }

  environment {
    // jenkins room
    SPARK_DEST_ROOMID = "Y2lzY29zcGFyazovL3VzL1JPT00vZmYxMDdiMTAtZTMzOS0xMWU2LWFlZGEtM2JmMjFmMTFjZDBi"
    SPARK_ACCESS_TOKEN = credentials('spark-bearer-token')
  }


stages {
  stage("configure-pypi-rc") {
        environment {
            PYPI_USER = credentials("hudya-pypi-username")
            PYPI_PASSWORD = credentials("hudya-pypi-password")
            PYPI_REPO = "https://pypi.hudya.io"
        }
        steps {
          script {
            sh "envsubst < .pypirc.TEMPLATE > .pypirc"
          }
        }
    }

    stage("build-package") {
        steps {
          sh "docker build . -t ${env.IMAGE_ID}"
        }
    }

    stage("push-to-pypi") {
        steps {
          script {
            if( env.BRANCH_NAME == "master" ) {
                sh "docker run ${env.IMAGE_ID} ."
            }
          }
        }
    }
  }

  post {
    always {
      script {
        try {
            sh "docker rm -v bumpversion || true"
            sh "docker rmi -f bumpversion || true"
        } catch(ex) {
            echo "problem: ${ex}" // in most cases we don't have image
        }
      }

      // cleans up workspace
      step([$class: 'WsCleanup'])
    }

   success {
      sendJenkinsBuildComplete(true)
    }

    failure {
      sendJenkinsBuildComplete(false)
    }
  }
}


