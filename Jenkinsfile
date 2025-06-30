pipeline {
  agent any

  environment {
    PROJECT_ID = 'euphoric-world-464505-q1'
    REGION = 'asia-east1'
    TRIGGER_NAME = 'jenkins-cloudrun-trigger'
    REPO_ID = '20481A04K2-jenkinscloudbuildtocloudrun'  // from the linked repo name
    SA_EMAIL = '519516300720-compute@developer.gserviceaccount.com'
  }

  stages {
    stage('Create Trigger If Missing') {
      steps {
        script {
          def triggerExists = sh(script: """
            gcloud beta builds triggers list \
              --project=${PROJECT_ID} \
              --region=${REGION} \
              --filter="name=${TRIGGER_NAME}" \
              --format="value(name)"
          """, returnStdout: true).trim()

          if (!triggerExists) {
            echo "🚀 Trigger does not exist. Creating Cloud Build trigger..."

            sh """
              gcloud beta builds triggers create \
                --name=${TRIGGER_NAME} \
                --region=${REGION} \
                --repository=${REPO_ID} \
                --branch-pattern="^main\$" \
                --build-config=cloudbuild.yaml \
                --service-account=${SA_EMAIL} \
                --project=${PROJECT_ID}
            """
          } else {
            echo "✅ Trigger already exists: ${TRIGGER_NAME}"
          }
        }
      }
    }

    stage('Trigger Build') {
      steps {
        echo "▶️ Manually starting the build using Cloud Build trigger..."
        sh """
          gcloud beta builds triggers run ${TRIGGER_NAME} \
            --branch=main \
            --region=${REGION} \
            --project=${PROJECT_ID}
        """
      }
    }
  }

  post {
    failure {
      echo "❌ Pipeline failed. Check Cloud Build logs in GCP Console."
    }
    success {
      echo "✅ Trigger created (if needed) and build triggered successfully."
    }
  }
}
