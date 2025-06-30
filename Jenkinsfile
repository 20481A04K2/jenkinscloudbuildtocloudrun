pipeline {
  agent any

  environment {
    PROJECT_ID = 'euphoric-world-464505-q1'
    TRIGGER_NAME = 'jenkins-cloudrun-trigger'
    GITHUB_REPO_NAME = 'jenkinscloudbuildtocloudrun'
    GITHUB_REPO_OWNER = '20481A04K2'
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
                --name=$TRIGGER_NAME \
                --region=$REGION \
                --repo-name=$GITHUB_REPO_NAME \
                --repo-owner=$GITHUB_REPO_OWNER \
                --branch-pattern='^main\$' \
                --build-config=cloudbuild.yaml \
                --project=$PROJECT_ID \
                --service-account=$SA_EMAIL
            """, returnStatus: true)

            if (result != 0) {
              echo "⚠️ Failed to create Cloud Build GitHub trigger. Make sure GitHub is connected in Cloud Console: https://console.cloud.google.com/cloud-build/triggers/connect"
              currentBuild.result = 'UNSTABLE'
            } else {
              echo "✅ Trigger successfully created."
            }
          } else {
            echo "✅ Trigger already exists: $TRIGGER_NAME"
          }
        }
      }
    }

    stage('Trigger Build') {
      when {
        expression {
          return currentBuild.result != 'FAILURE'
        }
      }
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
    unstable {
      echo "⚠️ Trigger was not created due to GitHub repo not being connected to Cloud Build."
    }
  }
}
