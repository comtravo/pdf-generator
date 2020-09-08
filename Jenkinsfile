pipeline {

  agent { label 'worker' }

  options {
    ansiColor('gnome-terminal')
    authorizationMatrix inheritanceStrategy: nonInheriting(), permissions: []
    buildDiscarder(logRotator(numToKeepStr: '30'))
    skipDefaultCheckout()
    timestamps()
  }

  stages {
    stage("Checkout SCM") {
      steps {
        script {
          ctCheckout(revision: getMultiBranchName(), wipeWorkspace: true, noTags: true, url: 'git@github.com:comtravo/pdf-generator.git')
        }
      }
    }

    stage("Build") {
      steps {
        script {
          ctDockerHubLogin()

          sh(label: 'Building docker image', script: "docker-compose build")
          sh(label: 'Pushing docker image', script: "docker-compose push")
        }
      }
    }
  }
}
