# Task 0.2: Register Application in Microsoft Entra ID

**Phase:** 0 - Project Setup & Azure Registration
**Estimated Time:** 1-2 hours
**Dependencies:** Microsoft 365 Developer Tenant (free)

---

## Description

Register a new application in Microsoft Entra ID (formerly Azure AD) to enable OAuth 2.0 authentication with Microsoft Graph API. This is a prerequisite for accessing user calendar data.

We use a **Microsoft 365 Developer Tenant** for app registration because it provides full admin control without corporate IT restrictions.

---

## Acceptance Criteria

### Developer Tenant Setup

- [ ] Microsoft 365 Developer Program account created
- [ ] Developer tenant provisioned
- [ ] Admin access confirmed

### App Registration Complete

- [x] Application registered in Microsoft Entra ID
- [x] Application (client) ID obtained and documented
- [x] Directory (tenant) ID obtained and documented
- [x] Client secret generated and stored securely
- [x] Redirect URIs configured for local development

### API Permissions Configured

- [x] Microsoft Graph API permissions added:
  - [x] `Calendars.Read` (Delegated)
  - [x] `User.Read` (Delegated)
  - [x] `offline_access` (Delegated) for refresh tokens
- [x] Admin consent granted (you're the admin!)

### Authentication Settings

- [x] Platform set to "Web" or "Mobile and desktop applications"
- [x] Redirect URI added: `http://localhost:8000/callback`
- [ ] Optional: Additional redirect URI for production
- [x] ID tokens enabled (if using implicit flow)
- [x] Access tokens enabled

### Security Configured

- [x] Client secret expiration set appropriately (12-24 months)
- [x] Client secret value copied (only shown once!)
- [x] Client secret stored in password manager or Azure Key Vault
- [x] NOT stored in code or version control

---

## Step-by-Step Instructions

### 0. Create Microsoft 365 Developer Tenant (One-Time Setup)

1. Go to [developer.microsoft.com/microsoft-365/dev-program](https://developer.microsoft.com/microsoft-365/dev-program)
2. Click "Join now" and sign in with any Microsoft account
3. Fill out the profile (select "Personal projects" for use case)
4. Click "Set up E5 subscription"
5. Create your admin username and password (save these!)
6. Complete phone verification
7. Wait for tenant provisioning (usually instant, sometimes a few minutes)

Your dev tenant admin account will be: `admin@yourdomain.onmicrosoft.com`

> **Note:** The dev tenant renews automatically if you're actively using it. Add some sample data to keep it active.

### 1. Navigate to Azure Portal

1. Go to [https://portal.azure.com](https://portal.azure.com)
2. **Sign in with your dev tenant admin account** (not your work account)
3. Verify you're in the right tenant (check top-right corner)
4. Search for "Microsoft Entra ID" or "Azure Active Directory"
5. Click on "App registrations" in the left menu

### 2. Register New Application

1. Click "+ New registration"
2. Fill in details:
   - **Name:** "Magic Umbrella - Time Allocation"
   - **Supported account types:** "Accounts in any organizational directory (Any Microsoft Entra ID tenant - Multitenant)"
   - **Redirect URI:**
     - Platform: Web
     - URI: `http://localhost:8000/callback`
3. Click "Register"

> **Why multi-tenant?** This allows you to sign in with your work account (Tenant A) even though the app is registered in your dev tenant.

### 3. Note Application IDs

After registration, copy these values:
- **Application (client) ID:** `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- **Directory (tenant) ID:** `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

Save these in `.env` file (not committed to git):
```
AZURE_CLIENT_ID=your-client-id
AZURE_TENANT_ID=common
```

> **Why `common`?** This allows sign-ins from any tenant (your work account or dev tenant account).

### 4. Generate Client Secret

1. Click "Certificates & secrets" in left menu
2. Click "+ New client secret"
3. Description: "Magic Umbrella Dev"
4. Expires: 12 months (or 24 months)
5. Click "Add"
6. **IMMEDIATELY COPY** the "Value" (shown only once!)
7. Save in `.env` file:
```
AZURE_CLIENT_SECRET=your-client-secret-value
```

### 5. Configure API Permissions

1. Click "API permissions" in left menu
2. Click "+ Add a permission"
3. Select "Microsoft Graph"
4. Select "Delegated permissions"
5. Add these permissions:
   - `Calendars.Read`
   - `User.Read`
   - `offline_access`
6. Click "Add permissions"

> **Admin consent:** Since you're the admin of your dev tenant, click "Grant admin consent for [your dev tenant]" to pre-approve these permissions. When signing in with your work account, you'll be prompted separately (see Testing section).

### 6. Configure Authentication

1. Click "Authentication" in left menu
2. Under "Platform configurations", verify redirect URI
3. Under "Implicit grant and hybrid flows":
   - ✅ Check "ID tokens"
   - ✅ Check "Access tokens" (optional)
4. Under "Allow public client flows":
   - Set to "No" (we're using web flow)
5. Click "Save"

---

## Security Checklist

- [X] Client secret stored in `.env` file
- [X] `.env` file added to `.gitignore`
- [X] Client secret NOT in code or documentation
- [X] Client secret backed up in password manager
- [X] Expiration date noted for renewal
- [X] Only minimum required permissions granted

---

## References

- Research Document: [research/initial-research.md](../../research/initial-research.md) (Lines 123-229)
- Azure App Registration: [research/initial-research.md](../../research/initial-research.md) (Lines 224-228)

---

## Validation Steps

1. Navigate to app registration in Azure Portal
2. Verify all permissions show "Granted" status
3. Test authentication in next phase (Task 1.1)
4. Confirm redirect URI works locally

---

## Testing: Which Calendar to Use

You have two options for testing:

### Option A: Work Account Calendar (Preferred)

Try signing in with your work account (Tenant A) to access your real calendar:

1. Run the app and trigger the OAuth flow
2. Sign in with your work email
3. You'll see a consent prompt for the permissions
4. **If you can accept** → You're using your real calendar data
5. **If it says "Need admin approval"** → Your work tenant blocks this; use Option B

### Option B: Dev Tenant Calendar (Fallback)

If your work tenant blocks consent, use your dev tenant's calendar:

1. Sign in with your dev tenant admin account
2. Create some test calendar events in Outlook
3. Use this account for development
4. Later, work with your IT team for production access if needed

> **Tip:** You can add sample users and data to your dev tenant at:
> [developer.microsoft.com/microsoft-365/dev-program](https://developer.microsoft.com/microsoft-365/dev-program) → Dashboard → Sample data packs

---

## Troubleshooting: Work Account Consent Issues

If you see "Need admin approval" when signing in with your work account:

### Why This Happens
Your work tenant (Tenant A) has disabled user consent for apps from external tenants.

### Options

1. **Use dev tenant calendar** for now (Option B above)
2. **Ask IT** to approve the app — they can visit:
   ```
   https://login.microsoftonline.com/{work-tenant-id}/adminconsent?client_id={your-app-client-id}
   ```
3. **Request a policy exception** for this specific app

---

## Background: Why We Use a Dev Tenant

This section documents the blockers encountered and the reasoning behind our approach.

### The Original Goal

Register an app to access calendar data via Microsoft Graph API using a corporate Azure subscription.

### Blockers Encountered

1. **Separate tenants:** The Azure subscription (Tenant B) is in a different Entra ID tenant than where the calendar/M365 data lives (Tenant A).

2. **Multi-tenant registration blocked:** To allow a user from Tenant A to authenticate with an app in Tenant B, the app must be registered as "multi-tenant." However, Tenant B's policies block creating multi-tenant app registrations.

3. **No app registration access in Tenant A:** Unable to register apps directly in Tenant A where the calendar data resides.

4. **Graph permissions are tied to app registration:** Microsoft Graph API permissions are configured within the app registration itself — they cannot be set up separately from the Azure Portal app registration.

### Why Dev Tenant Solves This

| Blocker | How Dev Tenant Helps |
|---------|---------------------|
| Can't create multi-tenant apps | You're the admin — no restrictions |
| Can't register apps in calendar tenant | Multi-tenant app can accept sign-ins from any tenant |
| Need Graph permissions | Full control to configure any permissions |
| Need admin consent | You're the admin — can grant consent |

### Trade-offs

- **Pro:** Complete control, no IT dependencies, free
- **Pro:** Can still attempt to use real work calendar (if Tenant A allows user consent)
- **Con:** If work tenant blocks consent, must use dev tenant's calendar for testing
- **Con:** Extra account to manage

### Future Production Considerations

For production use with real work calendar data, you may eventually need:
- IT approval in Tenant A for the external app
- Or: App registration moved to Tenant A
- Or: Corporate policy exception
