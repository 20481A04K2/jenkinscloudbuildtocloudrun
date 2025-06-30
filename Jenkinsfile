pipeline {
  agent any

  environment {
    PROJECT_ID = 'euphoric-world-464505-q1'
    TRIGGER_NAME = 'jenkins-cloudrun-trigger'
    GITHUB_REPO_NAME = 'jenkinscloudbuildtocloudrun'
    GITHUB_REPO_OWNER = '20481A04K2'
    GITHUB_REPO_FULL = '20481A04K2/jenkinscloudbuildtocloudrun'
    SA_EMAIL = '519516300720-compute@developer.gserviceaccount.com'
    REGION = 'asia-east1'
  }

  stages {
    stage('Create Trigger If Missing') {
      steps {
        script {
          def triggerExists = sh(script: """
            gcloud beta builds triggers list \
              --project=$PROJECT_ID \
              --filter="name=$TRIGGER_NAME" \
              --format="value(name)"
          """, returnStdout: true).trim()

          if (!triggerExists) {
            echo "🚀 Trigger does not exist. Attempting to create Cloud Build trigger..."

            def result = sh(script: """
              gcloud beta builds triggers create github \
                --name="$TRIGGER_NAME" \
                --region="$REGION" \
                --repository="$GITHUB_REPO_FULL" \
                --branch-pattern="^main\$" \
                --build-config="cloudbuild.yaml" \
                --service-account="$SA_EMAIL" \
                --project="$PROJECT_ID"
            """, returnStatus: true)

            if (result != 0) {
              error "⚠️ Failed to create Cloud Build GitHub trigger. Make sure GitHub is connected in Cloud Console: https://console.cloud.google.com/cloud-build/triggers/connect"
            }
          } else {
            echo "✅ Trigger already exists: $TRIGGER_NAME"
          }
        }
      }
    }

    stage('Trigger Build') {
      steps {
        echo "▶️ Manually starting the build using Cloud Build trigger..."
        sh """
          gcloud beta builds triggers run $TRIGGER_NAME \
            --branch=main \
            --project=$PROJECT_ID
        """
      }
    }
  }

  post {
    failure {
      echo "❌ Pipeline failed. Check Cloud Build logs in GCP Console."
    }
    success {
      echo "✅ Cloud Build trigger created (if needed) and started."
    }
  }
}
