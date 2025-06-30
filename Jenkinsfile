pipeline {
  agent any

  environment {
    PROJECT_ID = 'euphoric-world-464505-q1'
    REGION = 'asia-east1'
    TRIGGER_NAME = 'vamsi-trigger'
  }

  stages {
    stage('Trigger Build') {
      steps {
        echo "▶️ Triggering Cloud Build using trigger: ${TRIGGER_NAME}"
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
    success {
      echo "✅ Cloud Build trigger executed successfully."
    }
    failure {
      echo "❌ Pipeline failed. Check Cloud Build logs in GCP Console."
    }
  }
}
