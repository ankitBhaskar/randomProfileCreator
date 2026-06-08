# randomProfileCreator — Claude Development Guide

## Project Overview
A Flask + Angular app that generates random fictional Australian profiles for software testing and demos. Deployed at `randomprofilecreator.vercel.app`. Auth via Firebase (Google sign-in). Download history stored in Firestore.

## Stack
- **Frontend**: Angular 21, standalone components, signals, `@angular/fire` v20
- **Backend**: Flask (Python), Vercel serverless functions in `api/`
- **Auth**: Firebase Authentication (Google popup)
- **Database**: Firestore (user docs + download history)
- **Deploy**: Vercel — `main` branch auto-deploys

## Project Structure
```
/
├── api/
│   ├── profile.py          # GET /api/profile → JSON profile
│   └── employees.py        # GET /api/employees?count=N → CSV
├── frontend/
│   └── src/
│       ├── app/
│       │   ├── app.ts              # Root component
│       │   ├── app.html            # Root template
│       │   ├── app.css             # All styles (single file)
│       │   ├── app.config.ts       # Firebase providers
│       │   ├── auth.service.ts     # Google sign-in, lastLoginAt
│       │   ├── history.service.ts  # Firestore download history
│       │   ├── profile.service.ts  # HTTP /api/profile
│       │   └── profile.model.ts    # Profile interface
│       ├── environments/
│       │   ├── environment.ts      # Dev Firebase config
│       │   └── environment.prod.ts # Prod Firebase config
│       └── index.html
├── profile_generator.py    # Fun-name profile logic
├── employee_generator.py   # Bulk CSV generator
├── app.py                  # Flask dev server (not used on Vercel)
├── vercel.json             # Build + routing config
└── CLAUDE.md               # ← this file
```

## Key Rules
- **DO NOT** modify `profile_generator.py`, `employee_generator.py`, or `app.py` unless the user explicitly asks
- **DO NOT** push to any branch other than `main` (or the designated feature branch)
- Always use `npm install --legacy-peer-deps` — `@angular/fire@20` has a peer dep conflict with Angular 21
- All styles live in `frontend/src/app/app.css` — no separate component stylesheets
- Design language is documented in `design.md` — follow it for any new UI

## Local Dev
```bash
# Frontend
cd frontend
npm install --legacy-peer-deps
npm start          # http://localhost:4200 (proxies /api to localhost:5000)

# Backend
pip install -r requirements.txt
python app.py      # http://localhost:5000
```

## Vercel Deployment
- Auto-deploys from `main`
- `vercel.json` routes `/api/*` to Python serverless functions, everything else to Angular SPA
- Build command: `cd frontend && npm install --legacy-peer-deps && npm run build`
- Output: `frontend/dist/frontend/browser`

## Firebase
- Project: `randomprofilecreator`
- Auth: Google provider, authorized domain `randomprofilecreator.vercel.app`
- Firestore collections:
  - `users/{uid}` — profile doc (name, email, photoURL, createdAt, lastLoginAt)
  - `users/{uid}/downloads` — subcollection of download records (type, label, timestamp)

## Adding New Features
1. Read `design.md` before writing any CSS
2. New pages/sections go in `app.html` and `app.css`
3. New services go in `frontend/src/app/*.service.ts`
4. If reading from Firestore, add to `history.service.ts` or create a new service
5. Commit with clear messages, push to `main`
