env = "qa"

# Variables used to initialize Wiz Provider
wiz_service_account_vault_path        = "wizio/wizio/project_sp"
wiz_service_account_client_id_key     = "WIZ_CLIENT_ID"
wiz_service_account_client_secret_key = "WIZ_CLIENT_SECRET"

wiz_iac_cicd_scan_policies = {
 # Refer to documentation in https://docs.wiz.io/wiz-docs/docs/wiz-cicd-scan-policy for more information
 "WIZ-CICD-AKS-QA-AUDIT" = {
    name                              = "TD-ADMISSION-CONTROLLER-AKS-QA-AUDIT"
    description                       = "Wiz CI-CD Admission Controller Audit Policy - AKS. This policy should only have audit rules."
    iac_count_threshold = 1
    severity_threshold  = "INFORMATIONAL"
    rule_lifecycle_targets            = ["DEPLOY"],
    policy_lifecycle_enforcements     = [
      {
        deployment_lifecycle = "ADMISSION_CONTROLLER",
        enforcement_method  = "AUDIT"
      }
    ]
    ignore_rule_ids = [
      "67a22556-55e5-4cde-9f81-bf2f13f4952b",      # RISK_ACCEPTED-gtbdc-CSP-4944-td-istio-envoyFilterProvisioning.yml
      "20c47f7b-182e-47e7-bb34-6c85f9423faa",      # BY_DESIGN-azaks-CSP-999999-td-qa-testing-policy-set-1.yml
      "71973d72-7664-4495-8b17-519a8e38e31d",      # BY_DESIGN-azaks-CSP-999999-td-qa-testing-policy-set-2.yml
      "d6b770ac-1b1b-4849-93fa-e745f36a7b4c"       # BY_DESIGN-azaks-CSP-999999-td-qa-testing-policy-set-3.yml
    ]
    cloud_configuration_rules = [
      "TD-DUMMY-AC-RULE-TO-BE-DELETED-WHEN-ATLEAST-ONE-AC-AUDIT-RULE-EXISTS",
      "TDSTIG-AKS-KSPM-31-WIZ-CCR-K8S-001"
    ]
  },
  "WIZ-CICD-AKS-QA-BLOCK" = {
    name              = "TD-ADMISSION-CONTROLLER-AKS-QA-BLOCK"
    description       = "Wiz CI-CD Admission Controller BLOCK Policy - AKS. This policy should only have block rules."
    iac_count_threshold = 1
    severity_threshold  = "INFORMATIONAL"
    rule_lifecycle_targets            = ["DEPLOY"]
    policy_lifecycle_enforcements     = [
      {
        deployment_lifecycle = "ADMISSION_CONTROLLER",
        enforcement_method  = "BLOCK"
      }
    ]
    ignore_rule_ids = [
      "67a22556-55e5-4cde-9f81-bf2f13f4952b",      # RISK_ACCEPTED-gtbdc-CSP-4944-td-istio-envoyFilterProvisioning.yml
      "20c47f7b-182e-47e7-bb34-6c85f9423faa",      # BY_DESIGN-azaks-CSP-999999-td-qa-testing-policy-set-1.yml
      "71973d72-7664-4495-8b17-519a8e38e31d",      # BY_DESIGN-azaks-CSP-999999-td-qa-testing-policy-set-2.yml
      "d6b770ac-1b1b-4849-93fa-e745f36a7b4c",       # BY_DESIGN-azaks-CSP-999999-td-qa-testing-policy-set-3.yml
      "50c05c7b-4ab9-444a-be1c-6d8637e9b144",       # FALSE_POSITIVE-azaks-CSP-00000-kspm-23-load-balancer.yml
      "ebbd0139-412a-447f-80a1-e9c783b84c49"       # BY_DESIGN-azaks-CSP-92-td-istio-ingress.yml
    ]
    cloud_configuration_rules = [
      "TDSTIG-AKS-KSPM-01-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-02-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-03-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-04-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-05-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-06-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-07-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-08-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-09-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-10-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-12-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-13-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-14-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-15-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-16-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-17-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-18-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-19-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-20-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-21-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-22-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-23-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-24-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-25-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-28-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-29-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-VOLUME-1.0-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-VOLUME-1.1-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-VOLUME-1.2-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-VOLUME-1.3-WIZ-CCR-K8S-001",
      "TDSTIG-GCPPLAT-CSM-01-WIZ-CCR-AKS-001",
      "TDSTIG-GCPPLAT-CSM-02-WIZ-CCR-K8S-001",
      "TDSTIG-GCPPLAT-CSM-04-WIZ-CCR-AKS-001",
      "TDSTIG-GCPPLAT-CSM-10-WIZ-CCR-K8S-001",
      "TDSTIG-GCPPLAT-CSM-21-WIZ-CCR-K8S-001",
      "TDSTIG-GCPPLAT-CSM-27-WIZ-CCR-K8S-001",
      "TDSTIG-GCPPLAT-CSM-28-WIZ-CCR-AKS-001"
    ]
  },
  "WIZ-CICD-GKE-QA-AUDIT" = {
    name              = "TD-ADMISSION-CONTROLLER-GKE-QA-AUDIT"
    description       = "Wiz CI-CD Admission Controller AUDIT Policy - GKE. This policy should only have audit rules."
    iac_count_threshold = 1
    severity_threshold  = "INFORMATIONAL"
    rule_lifecycle_targets            = ["DEPLOY"]
    policy_lifecycle_enforcements     = [
      {
        deployment_lifecycle = "ADMISSION_CONTROLLER",
        enforcement_method  = "AUDIT"
      }
    ]
    ignore_rule_ids = [
      "67a22556-55e5-4cde-9f81-bf2f13f4952b",      # RISK_ACCEPTED-gtbdc-CSP-4944-td-istio-envoyFilterProvisioning.yml
      "20c47f7b-182e-47e7-bb34-6c85f9423faa",      # BY_DESIGN-azaks-CSP-999999-td-qa-testing-policy-set-1.yml
      "71973d72-7664-4495-8b17-519a8e38e31d",      # BY_DESIGN-azaks-CSP-999999-td-qa-testing-policy-set-2.yml
      "d6b770ac-1b1b-4849-93fa-e745f36a7b4c"       # BY_DESIGN-azaks-CSP-999999-td-qa-testing-policy-set-3.yml
    ]
    cloud_configuration_rules = [
      "TD-DUMMY-AC-RULE-TO-BE-DELETED-WHEN-ATLEAST-ONE-AC-AUDIT-RULE-EXISTS"
    ]
  },
  "WIZ-CICD-GKE-QA-BLOCK" = {
    name              = "TD-ADMISSION-CONTROLLER-GKE-QA-BLOCK"
    description       = "Wiz CI-CD Admission Controller BLOCK Policy - GKE. This policy should only have block rules."
    iac_count_threshold = 1
    severity_threshold  = "INFORMATIONAL"
    rule_lifecycle_targets            = ["DEPLOY"]
    policy_lifecycle_enforcements     = [
      {
        deployment_lifecycle = "ADMISSION_CONTROLLER",
        enforcement_method  = "BLOCK"
      }
    ]
    ignore_rule_ids = [
      "67a22556-55e5-4cde-9f81-bf2f13f4952b",      # RISK_ACCEPTED-gtbdc-CSP-4944-td-istio-envoyFilterProvisioning.yml
      "20c47f7b-182e-47e7-bb34-6c85f9423faa",      # BY_DESIGN-azaks-CSP-999999-td-qa-testing-policy-set-1.yml
      "71973d72-7664-4495-8b17-519a8e38e31d",      # BY_DESIGN-azaks-CSP-999999-td-qa-testing-policy-set-2.yml
      "d6b770ac-1b1b-4849-93fa-e745f36a7b4c",       # BY_DESIGN-azaks-CSP-999999-td-qa-testing-policy-set-3.yml
      "50c05c7b-4ab9-444a-be1c-6d8637e9b144",       # FALSE_POSITIVE-azaks-CSP-00000-kspm-23-load-balancer.yml
      "ebbd0139-412a-447f-80a1-e9c783b84c49"       # BY_DESIGN-azaks-CSP-92-td-istio-ingress.yml
    ]
    cloud_configuration_rules = [
      "TDSTIG-AKS-KSPM-01-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-02-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-03-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-04-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-05-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-06-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-07-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-08-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-09-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-10-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-12-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-13-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-14-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-15-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-16-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-17-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-18-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-19-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-20-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-21-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-22-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-23-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-24-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-25-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-28-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-29-WIZ-CCR-K8S-001",
      "TDSTIG-AKS-KSPM-31-WIZ-CCR-K8S-001",
      "TDSTIG-GCPPLAT-GKE-29-WIZ-CCR-GKE-001",
      "TDSTIG-GCPPLAT-GKE-30-WIZ-CCR-GKE-001",
      "TDSTIG-GCPPLAT-GKE-31-WIZ-CCR-GKE-001",
      "TDSTIG-GCPPLAT-CSM-01-WIZ-CCR-AKS-001",
      "TDSTIG-GCPPLAT-CSM-02-WIZ-CCR-K8S-001",
      "TDSTIG-GCPPLAT-CSM-04-WIZ-CCR-AKS-001",
      "TDSTIG-GCPPLAT-CSM-10-WIZ-CCR-K8S-001",
      "TDSTIG-GCPPLAT-CSM-21-WIZ-CCR-K8S-001",
      "TDSTIG-GCPPLAT-CSM-27-WIZ-CCR-K8S-001",
      "TDSTIG-GCPPLAT-CSM-28-WIZ-CCR-AKS-001"
    ]
  }
}
