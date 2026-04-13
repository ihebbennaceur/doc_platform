# Copy-Paste These Variables Into Vercel Project Settings

## Instructions
1. Go to: https://vercel.com/dashboard
2. Select your project
3. Click: Settings → Environment Variables
4. For EACH variable below:
   - Paste the Name (left side)
   - Paste the Value (right side)
   - Check: ☑️ Production  ☑️ Preview  ☑️ Development
   - Click: Save

---

## Variable 1: NEXT_PUBLIC_API_URL
**Name:**
```
NEXT_PUBLIC_API_URL
```
**Value:**
```
https://backenddoccheck-production.up.railway.app/api
```

---

## Variable 2: NEXT_PUBLIC_DOCCHECK_API_URL
**Name:**
```
NEXT_PUBLIC_DOCCHECK_API_URL
```
**Value:**
```
https://doccheckservice-copy-production.up.railway.app/api
```

---

## Variable 3: NEXT_PUBLIC_APP_NAME
**Name:**
```
NEXT_PUBLIC_APP_NAME
```
**Value:**
```
PFE Seller Platform
```

---

## Variable 4: NEXT_PUBLIC_APP_VERSION
**Name:**
```
NEXT_PUBLIC_APP_VERSION
```
**Value:**
```
1.0.0
```

---

## After Adding All 4 Variables

✅ Vercel will automatically redeploy your project (takes 2-3 minutes)

✅ Go to: https://docfrontend-beta.vercel.app/auth/register

✅ Open DevTools (F12) → Network tab

✅ Click Register button

✅ Check the request URL:
- Must be: `https://backenddoccheck-production.up.railway.app/api/register/`
- NOT: `http://localhost:8000/api/register/`

✅ If still shows localhost, do: `Ctrl+Shift+R` (hard refresh)

---

## If You Need to Upload .env File Instead

Vercel ALSO accepts `.env` files. Here's the format:

**.env.production**
```
NEXT_PUBLIC_API_URL=https://backenddoccheck-production.up.railway.app/api
NEXT_PUBLIC_DOCCHECK_API_URL=https://doccheckservice-copy-production.up.railway.app/api
NEXT_PUBLIC_APP_NAME=PFE Seller Platform
NEXT_PUBLIC_APP_VERSION=1.0.0
```

Then:
1. Add file to your project root
2. Commit: `git add .env.production && git commit -m "Add production env"`
3. Push: `git push origin main`
4. Vercel auto-detects it and uses it automatically

---

**Recommended:** Use Vercel UI (Method 1) - it's more secure and easier to update
