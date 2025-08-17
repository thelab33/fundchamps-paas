
---

### `paas_docs/MULTITENANCY.md`
```markdown
# 🏗️ Multitenancy Architecture

FundChamps PaaS supports **multi-tenant** operations:

1. **Tenant Configs**  
   - Each tenant has a JSON config under `app/tenants/<slug>/config.json`.
   - This defines branding, fundraising goal, logo, and sponsor tiers.

2. **Database Strategy**  
   - Single shared Postgres DB.
   - Tenant ID column is enforced on all models.
   - Migrations are global, data is isolated.

3. **Routing**  
   - Tenants are resolved by subpath:  
     `/tenant/<slug>/...`  
   - (Optional) Subdomain support can be enabled via NGINX ingress.

4. **Static Assets**  
   - Logos and custom banners live under `/static/tenants/<slug>/`.

This ensures every tenant has isolation but runs on the same platform.
