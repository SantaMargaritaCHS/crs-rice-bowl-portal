# CRS Lenten Alms Portal

**Project**: Santa Margarita Catholic High School Lenten Almsgiving Portal
**Repository**: https://github.com/SantaMargaritaCHS/crs-rice-bowl-portal
**Deployed**: Railway (auto-deploys on push to main)
**Last Updated**: February 23, 2026

---

## Quick Reference

| Resource | Value |
|----------|-------|
| Live Site | https://ricebowl.up.railway.app |
| Admin Panel | /admin (login required) |
| Database | PostgreSQL on Railway |
| Framework | Flask + SQLAlchemy |

---

## Project Structure

```
crs-site/
├── app/                    # Flask application
│   ├── routes/             # API and admin routes
│   ├── templates/admin/    # Admin dashboard templates
│   ├── models.py           # Database models
│   └── config.py           # Configuration
├── public/                 # Static frontend
│   ├── index.html          # Main landing page
│   ├── css/style.css       # Styles
│   ├── js/app.js           # Frontend JavaScript
│   └── images/             # CRS logo and assets
├── Dockerfile              # Railway deployment
└── railway.toml            # Railway config
```

---

## Key Models

- **SchoolClass**: Class name + `rice_bowl_amount` (donation tracking)
- **Quiz**: Weekly quizzes with country, forms link, winners
- **Setting**: Key-value store for totals, CRS link, etc.
- **Announcement**: Timed announcements for public page

---

## Terminology

**IMPORTANT**: The site uses "Lenten Alms" and "Class Donations" terminology (NOT "Rice Bowl") in the UI, but the database field is still `rice_bowl_amount` for backward compatibility.

- Public-facing: "Class Donations", "Lenten Alms"
- Database/code: `rice_bowl_amount` (legacy field name)

---

## Deployment

Railway auto-deploys when you push to main:

```bash
git add .
git commit -m "Description"
git push origin main
```

**Database**: PostgreSQL on Railway - data persists between deployments.

---

## February 2026 Updates

### Visual Enhancements
- Added CRS logo to header and footer
- Added "Top 3 Participating Classes" podium display
- Added donation thermometer showing grand total
- Moved navigation above hero section
- Applied cleaner UI with purple/gold Lenten theme

### Terminology Updates
- Renamed "Rice Bowl" to "Class Donations" throughout
- Updated admin templates (dashboard, classes, totals)
- Public page uses "Lenten Alms" terminology

### Infrastructure
- Added PostgreSQL support (psycopg2-binary)
- Fixed postgres:// to postgresql:// URL conversion
- Set up PostgreSQL database on Railway for data persistence

### Bug Fixes
- Fixed quiz saving (form action URL was incorrect)

### February 23 - Excel Upload for Class Donation Totals
- Added `openpyxl` dependency for Excel parsing
- New upload flow: Admin uploads `.xlsx` payment form export -> preview -> confirm
- Parses teacher last name (col N), period (col M), amount (col P) from row 3+
- Matches to `SchoolClass` via case-insensitive last name + period number
- Amounts are **added** to existing totals (never replaced)
- SHA-256 file hash dedup prevents double-counting same file
- Files: `admin.py` (2 new routes), `totals.html` (upload card), `upload_preview.html` (new)

---

## Admin Pages

- `/admin/` - Dashboard with stats
- `/admin/classes` - Manage participating classes
- `/admin/totals` - Set donation amounts per class + Excel upload
- `/admin/totals/upload` - Upload payment form export (.xlsx)
- `/admin/totals/upload/confirm` - Confirm and apply uploaded amounts
- `/admin/quizzes` - Configure weekly quizzes
- `/admin/announcements` - Manage announcements

---

## API Endpoints

- `GET /api/data` - All public data (classes, totals, quizzes)
- `GET /api/health` - Health check for Railway

---

## Notes

- Classes are sorted by donation amount (descending) for leaderboard
- Grand total = Online Alms + Class Donations
- Thermometer displays grand total without a target goal
- Quiz visibility controlled by schedule_mode (auto/manual)
- Excel upload column mapping: col 12=period, col 13=teacher, col 15=amount (0-indexed)
- Upload dedup hashes stored in `Setting` key `upload_hashes` (JSON list, keeps last 20)

---

## Developer Tools

### Codanna (Semantic Code Search)
- **Index location**: `.codanna/` (gitignored)
- **Re-index**: `codanna index .` (run after major code changes)
- **MCP server**: Connected via Claude Code MCP (auto-available in sessions)
- **Usage**: Semantic search, symbol lookup, call graph analysis, impact analysis

### Beads (Issue Tracker)
- **Database**: `.beads/` (git-tracked)
- **Commands**: Run `bd` from project root
  - `bd new "title"` - Create issue
  - `bd list` - List open issues
  - `bd show <id>` - View issue details
  - `bd close <id>` - Close issue
  - `bd comment <id> "text"` - Add comment
