# Vision: Cloud-Based Queue & Output Sync

## Vision Statement
Transform Whisper from a single-machine workflow into a seamless cross-device system where voice memos recorded on your phone automatically sync to a shared queue accessible from your MacBook Pro, Dell Alienware, and Lambda workstation. The solution must be pragmatic, privacy-respecting, and simple enough to set up in under 1 hour, working reliably for months without constant maintenance while keeping personal audio files separate from the shared codebase.

## Current State Analysis

### What Exists Today
- **Local queue system**: `queue/` directory on each machine for unprocessed audio files
- **Local output organization**: `output/` directory with intelligent titling (e.g., `whisper-app-insights-ideas_2026-01-14_19-38-44/`)
- **Queue processor**: `/process_queue` command that batch-processes all queued audio files with parallel sub-agents
- **Instant capture capability**: `scripts/record_memo.sh` and hotkey setup for direct-to-queue recording
- **Privacy-aware architecture**: Audio files live outside the main repo, separate from code
- **Multi-platform support**: Works on macOS and Ubuntu with sox-based recording

### Current Pain Points
1. **Phone-to-desktop friction**: Recording on phone requires 3-4 manual steps to get audio into queue
   - MacBook: Download from Voice Memos app → manually move to `queue/` folder
   - Ubuntu machines: Upload to Google Drive/email → download → move to `queue/` folder (4 steps)
2. **Siloed queues**: Each machine has its own `queue/` directory; no shared access
3. **Output scattered**: Transcriptions and deliverables only exist on the machine that processed them
4. **No cross-device workflow**: Can't record on phone in the park, then process on work machine
5. **Privacy risk**: Audio files shouldn't live in git repo, but need to be accessible across devices
6. **No backup**: Audio files are journal-like and irreplaceable, but have no automatic backup

### The Gap
Users want to capture thoughts on their phone (the device that's always with them) and have those audio files immediately available in the `queue/` directory on all machines. Current workflow is manual and location-dependent, creating enough friction that voice capture is underutilized despite its value. The gap is **instant, automatic sync** that works transparently across iOS, macOS, and Ubuntu without breaking the existing queue processing workflow.

## Vision Goals
1. **Eliminate phone-to-desktop friction**: Voice memo on phone → appears in `queue/` on all machines within seconds
2. **Unified queue**: Single source of truth for pending audio files, accessible from all devices
3. **Cross-device output access**: Transcriptions and deliverables available everywhere
4. **Maintain privacy**: Personal audio files stay out of the git repo, remain under user control
5. **Battle-tested reliability**: Solution must work consistently for months without debugging
6. **Sub-1-hour setup**: User can set this up tomorrow in spare time with minimal configuration
7. **Zero ongoing maintenance**: No manual syncing, no cron jobs to babysit, no API quotas to monitor

## Implementation Paths

### Path 1: iCloud Drive / Google Drive Native Sync (Simplest)
**Approach**: Move `queue/` and `output/` directories into a native cloud storage folder that auto-syncs on all platforms. Leverage battle-tested consumer sync services that already have iOS/macOS/Ubuntu clients.

**Effort**: Low (15-30 minutes setup)
**Impact**: High (solves phone-to-desktop immediately)
**Risk**: Low (proven technology, millions of users)

**Dependencies**:
- iCloud Drive account (comes with macOS/iOS) OR Google Drive account (free 15GB)
- Cloud sync clients installed on Ubuntu machines

**High-Level Features**:
1. **Move queue to cloud folder**: Relocate `queue/` directory to `~/iCloud Drive/whisper-queue/` or `~/Google Drive/whisper-queue/`
2. **Move output to cloud folder**: Relocate `output/` directory to cloud storage for cross-device access
3. **Update scripts to use cloud paths**: Modify `scripts/record_memo.sh` and queue processor to reference new paths
4. **iOS Shortcuts integration**: Create iOS shortcut that saves Voice Memos directly to cloud folder
5. **Symlink for convenience**: Create symlinks from project directory to cloud folders for transparent access

**High-Level Chores**:
1. **Install cloud sync client on Ubuntu**: Install gnome-online-accounts for iCloud or google-drive-ocamlfuse for Google Drive
2. **Configure environment variable**: Add `WHISPER_QUEUE_DIR` and `WHISPER_OUTPUT_DIR` to .env or shell profile
3. **Update documentation**: Add cloud sync setup instructions to README
4. **Test cross-platform sync**: Verify files sync correctly between iOS, macOS, and Ubuntu

**Trade-offs**:
- ✅ **15-30 minute setup**: Fastest path to working solution
- ✅ **Zero maintenance**: Sync happens automatically in background
- ✅ **iOS integration**: Voice Memos app can save directly to cloud folder via Shortcuts
- ✅ **Battle-tested**: iCloud and Google Drive are used by millions, highly reliable
- ✅ **Privacy maintained**: Files stay in user's personal cloud account, not shared repo
- ✅ **Works offline**: Cloud sync clients queue changes and sync when online
- ✅ **Free tier sufficient**: 5GB iCloud or 15GB Google Drive is plenty for audio files
- ❌ **Proprietary service dependency**: Relies on Apple/Google infrastructure
- ❌ **Sync conflicts possible**: Rare, but can happen if same file modified on multiple devices
- ❌ **Ubuntu setup slightly involved**: Requires third-party clients (gnome-online-accounts or google-drive-ocamlfuse)
- ❌ **No git-based versioning**: Can't branch/merge queue contents (but do you need this?)

**Implementation Steps (30 minutes)**:
1. *(5 min)* Create `~/iCloud Drive/whisper/` folder on Mac, wait for sync to confirm it works
2. *(5 min)* Move existing `queue/` and `output/` into iCloud folder, create symlinks in project
3. *(5 min)* Update `.env` to set `WHISPER_QUEUE_DIR="$HOME/iCloud Drive/whisper/queue"`
4. *(5 min)* Test: record memo on Mac, verify it appears in iCloud folder
5. *(5 min)* Install iCloud client on Ubuntu machines (gnome-online-accounts), verify sync
6. *(5 min)* Create iOS Shortcut: "Record Voice Memo → Save to iCloud Drive/whisper/queue"

---

### Path 2: Syncthing (Decentralized, Privacy-First)
**Approach**: Use Syncthing, an open-source peer-to-peer file sync tool, to synchronize `queue/` and `output/` directories across all devices. No cloud middleman, complete user control, works on macOS/Linux/iOS (via Möbius Sync).

**Effort**: Medium (45-60 minutes setup)
**Impact**: High (solves phone-to-desktop with more control)
**Risk**: Medium (requires iOS third-party app, more moving parts)

**Dependencies**:
- Syncthing installed on all devices
- Möbius Sync app on iOS ($5-10 one-time purchase, or free alternatives like FolderSync)
- At least one device online as "hub" for relay (or configure relay servers)

**High-Level Features**:
1. **Install Syncthing on all devices**: Mac, Ubuntu machines, iOS (via Möbius Sync)
2. **Create shared folders**: Configure `queue/` and `output/` as synced folders
3. **Device discovery**: Link devices using Syncthing device IDs (one-time setup)
4. **Selective sync**: Can choose which devices get which folders (e.g., phone only syncs queue, not output)
5. **Conflict resolution**: Syncthing automatically handles conflicts by creating duplicate files

**High-Level Chores**:
1. **Install Syncthing**: `brew install syncthing` (Mac), `apt install syncthing` (Ubuntu), Möbius Sync (iOS App Store)
2. **Configure folder ignores**: Ensure `.DS_Store` and temp files don't sync
3. **Set up relay/discovery**: Use default public relays or configure private relay
4. **Test sync behavior**: Verify bidirectional sync works between all device pairs
5. **Document device linking process**: Write clear instructions for adding new devices

**Trade-offs**:
- ✅ **Complete privacy**: No cloud service, data only on your devices
- ✅ **Open source**: Full control, can self-host relay servers if desired
- ✅ **No monthly costs**: One-time iOS app purchase (~$5) vs. ongoing cloud storage fees
- ✅ **Works offline**: Devices sync directly when on same network
- ✅ **Versioning built-in**: Syncthing can keep file versions for recovery
- ✅ **Selective sync**: Fine-grained control over what syncs where
- ❌ **iOS app required**: Möbius Sync is paid, not as polished as native iOS integration
- ❌ **Requires one device online**: If all devices offline, sync pauses (but this is rare)
- ❌ **More initial setup**: 45-60 minutes vs. 15-30 for cloud drive
- ❌ **Less mature ecosystem**: Fewer users than iCloud/Google Drive, more potential for edge cases
- ❌ **Voice Memos integration harder**: iOS Voice Memos can't save directly to Syncthing folder (need manual export)

**Implementation Steps (60 minutes)**:
1. *(10 min)* Install Syncthing on Mac: `brew install syncthing`, start service, open web UI at localhost:8384
2. *(10 min)* Install Syncthing on Ubuntu machines, start service, open web UI
3. *(10 min)* Link devices: Copy device IDs, add each device to others' trusted list
4. *(10 min)* Create shared folders: Add `queue/` and `output/` as synced folders on all devices
5. *(10 min)* Install Möbius Sync on iOS, configure connection to Mac/Ubuntu devices
6. *(10 min)* Test: Create file on phone, verify it syncs to all devices within 10 seconds

---

### Path 3: Git LFS + Private GitHub Repo (Version Control for Audio)
**Approach**: Treat `queue/` and `output/` as a separate git repository backed by Git LFS (Large File Storage) for audio files. Push/pull to sync, leveraging GitHub's infrastructure. Enables branching, history, and version control for voice memos.

**Effort**: Medium-High (60-90 minutes setup)
**Impact**: Medium (solves sync, adds powerful versioning, but requires manual git operations)
**Risk**: Medium-High (complex workflow, potential for merge conflicts, iOS integration tricky)

**Dependencies**:
- Private GitHub repository (free for personal use)
- Git LFS installed on all devices
- iOS Git client (Working Copy app, $20) or custom Shortcuts workflow to commit/push
- Understanding of git workflows (branching, conflicts, pull/push)

**High-Level Features**:
1. **Create whisper-data private repo**: New repo for `queue/` and `output/` directories only
2. **Git LFS for audio files**: Configure `.gitattributes` to track `.m4a`, `.wav`, `.mp3` with LFS
3. **Manual sync workflow**: Record → git add/commit/push → pull on other devices
4. **Branch-based workflows**: Could have device-specific branches that merge to main
5. **Full history**: Every voice memo and transcription versioned, can recover deleted files
6. **iOS automation**: Working Copy app or Shortcuts can automate git push after recording

**High-Level Chores**:
1. **Install Git LFS**: `brew install git-lfs` (Mac), `apt install git-lfs` (Ubuntu)
2. **Create private repo**: Set up `whisper-data` repo on GitHub with LFS enabled
3. **Configure .gitattributes**: Track audio formats with LFS to avoid repo bloat
4. **Write sync scripts**: Create `scripts/sync_queue.sh` that does git pull/push
5. **Set up iOS Git client**: Install Working Copy, configure repo, create automation shortcuts
6. **Document workflow**: Write clear instructions on when to pull/push

**Trade-offs**:
- ✅ **Full version control**: Every voice memo has history, can recover anything
- ✅ **GitHub benefits**: Free private repos, web UI to browse files, issue tracking
- ✅ **Branching possible**: Could experiment with queue organization strategies
- ✅ **Audit trail**: Know when each memo was recorded, processed, modified
- ✅ **User already loves GitHub**: Vision doc mentions preference for GitHub
- ❌ **Manual sync required**: Must remember to git pull/push (not automatic)
- ❌ **Merge conflicts possible**: If two devices process same queue file, conflict occurs
- ❌ **iOS complexity**: Working Copy app is powerful but has learning curve
- ❌ **Git LFS storage limits**: GitHub free tier has 1GB LFS storage (upgrade for more)
- ❌ **Requires git knowledge**: User must understand branches, conflicts, pull/push
- ❌ **Not instant**: Must explicitly sync, not transparent like cloud drives

**Implementation Steps (90 minutes)**:
1. *(10 min)* Create private GitHub repo `whisper-data`, initialize with README
2. *(10 min)* Install Git LFS on all devices, initialize in repo
3. *(10 min)* Configure `.gitattributes`: `*.m4a filter=lfs`, `*.wav filter=lfs`, `*.mp3 filter=lfs`
4. *(15 min)* Move `queue/` and `output/` into repo, initial commit/push
5. *(15 min)* Clone repo on Ubuntu machines, set up git credentials
6. *(15 min)* Install Working Copy on iOS, clone repo, configure Voice Memos export
7. *(15 min)* Write `scripts/sync_queue.sh` helper, test bidirectional sync
8. *(10 min)* Document workflow: "Record → Export to Working Copy → Commit → Push → Pull on desktop"

---

### Path 4: Hybrid Approach (Cloud Sync + Git Versioning)
**Approach**: Use iCloud/Google Drive for instant sync (Path 1) while also backing up to a Git LFS repo (Path 3) for versioning and recovery. Best of both worlds: convenience + history.

**Effort**: Medium-High (90-120 minutes setup, combines Path 1 + Path 3)
**Impact**: High (maximum reliability and features)
**Risk**: Medium (more complexity, but redundancy reduces failure risk)

**Dependencies**:
- Everything from Path 1 (cloud sync) + Path 3 (Git LFS)
- Cron job or file watcher to auto-commit cloud folder changes to git

**High-Level Features**:
1. **Primary sync via cloud**: iCloud/Google Drive provides instant cross-device sync (Path 1)
2. **Automatic git backup**: Script or cron job periodically commits cloud folder to Git LFS repo
3. **Recoverable history**: Even if cloud sync fails or files deleted, git has backup
4. **Transparent workflow**: User interacts with cloud folder, git happens automatically
5. **Best-case sync speed**: Cloud drive syncs in seconds, git backup happens in background

**High-Level Chores**:
1. **Set up cloud sync**: Complete Path 1 setup (iCloud or Google Drive)
2. **Set up git repo**: Complete Path 3 setup (Git LFS repo)
3. **Write auto-commit script**: Create `scripts/auto_backup_to_git.sh` that commits cloud folder changes
4. **Configure cron job**: Run auto-commit script every hour (or use file watcher for instant backup)
5. **Test failover**: Verify that if cloud sync fails, can recover from git repo

**Trade-offs**:
- ✅ **Maximum reliability**: Two independent sync systems, very hard to lose data
- ✅ **Best UX**: Cloud sync feels instant, git versioning is invisible
- ✅ **Full history preserved**: Git LFS repo serves as append-only archive
- ✅ **Failover capability**: If cloud service has issues, git repo is backup
- ❌ **Most complex setup**: 90-120 minutes, two systems to understand
- ❌ **Higher maintenance**: Cron job to monitor, two systems that could break
- ❌ **Doubled storage cost**: Files live in cloud + Git LFS (but audio files are small)
- ❌ **Overkill for initial goal**: Adds complexity that may not be needed for months

**Implementation Steps (120 minutes)**:
1. *(30 min)* Complete Path 1 setup (cloud sync)
2. *(60 min)* Complete Path 3 setup (Git LFS repo)
3. *(15 min)* Write auto-commit script: `cd ~/iCloud Drive/whisper && git add . && git commit -m "Auto-backup $(date)" && git push`
4. *(10 min)* Add cron job: `0 * * * * /path/to/auto_backup_to_git.sh` (every hour)
5. *(5 min)* Test: Record memo, verify it syncs via cloud AND gets committed to git within an hour

---

## Path Comparison Matrix

| Criteria | Path 1 (Cloud) | Path 2 (Syncthing) | Path 3 (Git LFS) | Path 4 (Hybrid) |
|----------|----------------|-------------------|-----------------|----------------|
| **Setup Time** | 15-30 min | 45-60 min | 60-90 min | 90-120 min |
| **Time to Value** | Fast (works today) | Fast (works today) | Medium (works after setup) | Medium (works after setup) |
| **Technical Complexity** | Low | Medium | Medium-High | High |
| **User Impact** | High | High | Medium | High |
| **Maintenance Burden** | None | Low | Medium | Medium-High |
| **Scalability** | High | High | Medium | High |
| **Privacy** | Medium (cloud) | High (P2P) | Medium (GitHub) | Medium |
| **iOS Integration** | Excellent (native) | Good (paid app) | Fair (Working Copy) | Excellent (native) |
| **Offline Support** | Good (cache) | Excellent | Poor (needs push) | Good |
| **Version History** | None | Optional | Full | Full |
| **Conflict Handling** | Automatic | Automatic | Manual (git) | Automatic + Manual |
| **Recovery from Loss** | Cloud backup only | Peer devices | Full git history | Both cloud + git |
| **Cost** | Free tier sufficient | $5-10 iOS app | Free (LFS limits) | Free + $5-10 |

## Recommended Approach

**Start with Path 1 (iCloud/Google Drive), evolve to Path 4 if needed**

For your constraint of "<1 hour setup, works for months," **Path 1 is the clear winner**. Here's why:

### Phase 1: Path 1 (Cloud Sync) - Tomorrow
Set up iCloud Drive or Google Drive sync in **under 30 minutes**. This immediately solves your biggest pain point (phone-to-desktop friction) with battle-tested technology that requires zero maintenance.

**Why Path 1 is ideal for you:**
1. **15-30 minute setup**: Fits your "spare time tomorrow" requirement perfectly
2. **Works for months**: iCloud/Google Drive are rock-solid, millions of users rely on them daily
3. **iOS native**: Voice Memos app integrates beautifully via Shortcuts
4. **Zero maintenance**: Set it and forget it, syncs automatically
5. **Ubuntu support exists**: gnome-online-accounts for iCloud, native for Google Drive
6. **Solves the core problem**: Phone → queue in seconds, not 3-4 manual steps

### Phase 2: Path 4 (Add Git Backup) - Optional, Later
If after a few months you want version control and extra redundancy, layer on Path 3's Git LFS backup. The beauty of this approach: Path 1 keeps working while you add git versioning on top.

**Why add git later:**
- Cloud sync proves reliable, but you want recovery history
- You discover you're deleting/modifying processed memos and want undo capability
- You want to experiment with branching workflows for different memo types

**Why This Order:**
1. **Solve pain now**: Path 1 eliminates phone-to-desktop friction immediately
2. **Validate usage**: Use cloud sync for 2-3 months to confirm Whisper fits your workflow
3. **Avoid premature optimization**: Don't build complex git workflows until you know you need them
4. **Learn what matters**: Real usage reveals whether versioning, conflict handling, or other features matter

### Why NOT Syncthing (Path 2)?
Syncthing is excellent for privacy and control, but:
- **45-60 min setup** (too close to your 1-hour limit, risks running over)
- **iOS app less polished** than native Voice Memos + iCloud integration
- **More moving parts** = more potential for issues
- Path 1 is simpler and achieves the same goal

### Why NOT Git LFS (Path 3) initially?
Git is powerful, but:
- **Manual sync required** (must remember to push/pull)
- **60-90 min setup** exceeds your time budget
- **Merge conflicts** are a real risk if multiple devices process queue
- **Overkill for the problem**: You need sync, not version control (yet)

## Path Dependencies Diagram

```
Start Here
    ↓
Path 1: Cloud Sync (iCloud or Google Drive)
    ↓ [Use for 2-3 months]
    ↓
Decision Point: Need version control?
    ├─ No → Keep using Path 1 (done!)
    ├─ Yes → Add Path 3 (Git LFS backup)
    │   ↓
    │   Path 4: Hybrid (Cloud + Git)
    │
    └─ Want more privacy? → Migrate to Path 2 (Syncthing)
```

## Next Steps

### Tomorrow (Under 1 Hour): Implement Path 1

**Choose your poison:** iCloud Drive or Google Drive?
- **iCloud** if you use Mac/iOS primarily, prefer Apple ecosystem
- **Google Drive** if you use Google Workspace, want best cross-platform support

**iCloud Drive Setup (30 minutes):**
1. *(5 min)* On MacBook, create `~/Library/Mobile Documents/com~apple~CloudDocs/whisper/` folder structure with `queue/` and `output/` subdirs
2. *(5 min)* Create symlinks in whisper project: `ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/whisper/queue queue-cloud` and `ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/whisper/output output-cloud`
3. *(5 min)* Update `.env` file: Add `WHISPER_QUEUE_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/whisper/queue"` and `WHISPER_OUTPUT_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/whisper/output"`
4. *(5 min)* Update `scripts/record_memo.sh` to use `$WHISPER_QUEUE_DIR` instead of hardcoded `queue/` path
5. *(5 min)* Test: Record memo on Mac using script, verify file appears in iCloud folder AND syncs to iCloud.com
6. *(5 min)* On Ubuntu machines, install gnome-online-accounts: `sudo apt install gnome-online-accounts`, add iCloud account in GNOME Settings → Online Accounts

**iOS Shortcuts Setup (10 minutes):**
1. Open Shortcuts app on iPhone
2. Create new shortcut: "Record Voice Memo → Save to iCloud Drive/whisper/queue"
3. Add actions:
   - "Record Audio" (wait for user to stop)
   - "Set Name" (use timestamp: `memo_YYYY-MM-DD_HH-MM-SS`)
   - "Save File" to iCloud Drive/whisper/queue
4. Test: Run shortcut, record 5-second memo, verify it appears in iCloud folder on Mac within 10 seconds
5. Add shortcut to Home Screen or Lock Screen for instant access

**Validation:**
- Record voice memo on iPhone using shortcut
- Within 10-20 seconds, verify file appears in `~/Library/Mobile Documents/com~apple~CloudDocs/whisper/queue/` on MacBook
- Within 60 seconds, verify file syncs to Ubuntu machines (if online)
- Run `/process_queue` on any machine, verify transcription works and output saves to cloud folder
- Verify processed output appears on all devices

### After 2-3 Months: Evaluate Need for Git Versioning

**If you're happy with cloud sync alone:**
- Done! You've solved the problem in 30 minutes.

**If you want version control and history:**
- Implement Path 3 (Git LFS) as a backup layer
- Write auto-commit script to periodically snapshot cloud folder to git
- Upgrade to Path 4 (Hybrid) for maximum reliability

## Open Questions

1. **iCloud vs. Google Drive preference?**
   - **Recommendation**: iCloud if you're Mac/iOS-first (better native integration, Voice Memos shortcuts work seamlessly). Google Drive if you need best Ubuntu support.

2. **Keep queue and output separate or together?**
   - **Recommendation**: Keep both in same cloud folder (`whisper/queue` and `whisper/output`) for simplicity. Can split later if one grows too large.

3. **Archive directory: cloud or local?**
   - **Recommendation**: Keep archive local initially. Audio files in archive are already processed; no need to sync everywhere. Can move to cloud later if you want universal access.

4. **Automatic queue processing?**
   - This vision focuses on sync, but consider: Should queue processor auto-run when new files sync? (e.g., file watcher triggers `/process_queue`)
   - **Recommendation**: Keep manual for now (`/process_queue` on demand). Add auto-processing later once sync is proven stable.

5. **What if cloud storage fills up?**
   - **Recommendation**: Periodically archive old output directories to local storage or secondary backup. 5GB iCloud should handle ~500 hours of voice memos (at ~10MB/hour).

6. **Should we support multiple cloud backends?**
   - **Recommendation**: Start with one (iCloud or Google Drive), make paths configurable via `.env`. Add Dropbox/OneDrive support later if users request it.

## Future Considerations

1. **Mobile app**: Build native iOS/Android app for Whisper with built-in recording and queue management (long-term, way beyond 1 hour)

2. **Shared queues**: Multiple users syncing to same queue for team voice memo processing (requires conflict resolution strategy)

3. **Smart sync**: Only sync queue files, not output (reduces bandwidth if outputs are large)

4. **Encryption at rest**: Encrypt audio files in cloud for extra privacy (could use rclone with encryption)

5. **Self-hosted sync**: Host own Nextcloud or Seafile instance for complete control (Path 2.5 between cloud and Syncthing)

6. **Voice Memos app integration**: Explore if Voice Memos app can auto-export to cloud folder via automation (better than Shortcuts)

7. **Bandwidth optimization**: Compress audio files before syncing, decompress on processing (reduces cloud storage usage)

8. **Offline queue**: Allow queue processing to work fully offline, sync outputs when online

9. **Multi-cloud redundancy**: Sync to both iCloud AND Google Drive automatically for maximum safety (probably overkill)

---

## Research Sources

### Cloud Sync on Ubuntu
- [How to set up iCloud on Ubuntu](https://www.omgubuntu.co.uk/2021/02/use-icloud-ubuntu-linux-gnome)
- [gnome-online-accounts iCloud support](https://gitlab.gnome.org/GNOME/gnome-online-accounts)
- [google-drive-ocamlfuse for Ubuntu](https://github.com/astrada/google-drive-ocamlfuse)

### Git LFS for Audio Files
- [Git Large File Storage](https://git-lfs.github.com/)
- [GitHub Git LFS pricing and bandwidth](https://docs.github.com/en/billing/managing-billing-for-git-large-file-storage/about-billing-for-git-large-file-storage)

### Syncthing Documentation
- [Syncthing: Open Source Continuous File Synchronization](https://syncthing.net/)
- [Möbius Sync: Syncthing for iOS](https://www.mobiussync.com/)
- [Syncthing on Android](https://play.google.com/store/apps/details?id=com.nutomic.syncthingandroid)

### iOS Shortcuts & Voice Memos
- [How to use Shortcuts with Voice Memos](https://support.apple.com/guide/shortcuts/welcome/ios)
- [Save files to iCloud Drive using Shortcuts](https://support.apple.com/guide/shortcuts/use-icloud-drive-apd621a1ad7a/ios)

### Working Copy (Git on iOS)
- [Working Copy: Powerful Git client for iOS](https://workingcopyapp.com/)
- [Working Copy automation with Shortcuts](https://workingcopyapp.com/manual/shortcuts)
