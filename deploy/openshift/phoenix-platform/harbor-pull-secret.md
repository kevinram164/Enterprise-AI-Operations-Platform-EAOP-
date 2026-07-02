# Harbor pull secret

Tạo secret để OpenShift pull image từ Harbor:

```bash
oc create secret docker-registry harbor-pull-secret \
  --docker-server=harbor.ocp1.npd.co \
  --docker-username='<robot-account>' \
  --docker-password='<token-from-vault>' \
  -n phoenix-platform

oc secrets link default harbor-pull-secret --for=pull -n phoenix-platform
```

Credentials lấy từ Vault: `secret/phoenix/ci/harbor`

Hoặc dùng **External Secrets Operator** sync từ Vault (recommended production).
