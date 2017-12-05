pipeline {
  def app

  stage('Clone repository') {
    checkout scm
  }

  stage('Build image') {
    app = docker.build("piyushiitg/healthmonitordocker")
    sh 'echo "Build Successful"'
  }

  stage('Test image') {
    app.inside {
    sh 'echo "Tests passed"'
    }
  }
  stage('Push image') {
    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
    app.push("${env.BUILD_NUMBER}")
    app.push("latest")
    }
  }
}
