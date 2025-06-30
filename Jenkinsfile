pipeline {
  agent any

  environment {
    PROJECT_ID = 'euphoric-world-464505-q1'
    TRIGGER_NAME = 'jenkins-cloudrun-trigger'
    GITHUB_REPO_MIRROR = '20481A04K2_jenkinscloudbuildtocloudrun' // first-gen mirrored repo name
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
              gcloud beta builds triggers create \
                --name="$TRIGGER_NAME" \
                --region="$REGION" \
                --repo="$GITHUB_REPO_MIRROR" \
                --branch-pattern="^main\$" \
                --build-config="cloudbuild.yaml" \
                --service-account="$SA_EMAIL" \
                --project="$PROJECT_ID"
            """, returnStatus: true)

            if (result != 0) {
              error "⚠️ Failed to create Cloud Build trigger. Ensure the mirrored GitHub repo exists in Cloud Console: https://console.cloud.google.com/cloud-build/triggers"
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
