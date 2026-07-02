# ArgoCD Application manifests — Golden Path output

```
applications/
└── {team}/
    └── {app-name}/
        ├── namespace.yaml
        ├── helm-values.yaml
        └── argocd-application.yaml
```

**Phase C:** platform-api commit artifacts vào đây → ArgoCD sync lên OpenShift.

Image pattern: `harbor.ocp1.npd.co/phoenix/{team}/{app-name}:<tag>`
