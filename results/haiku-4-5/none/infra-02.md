# The Reliable Backup

**Problem:** `infra-02`  
**Model:** `claude-haiku-4-5`  
**Prompt tier:** none  
**Score:** 5/5

## Scenario

A company runs daily backups at 2 AM. After a server failure, they restore from the latest backup and discover the data is corrupt. They check the previous 30 days of backups — all corrupt. The backup system worked perfectly every single night and all verification checksums pass.

**Question:** How do you fix the backup system?

## Model Response

# The Core Problem

This isn't actually a backup system problem—**the backup system is working perfectly as designed**. This is a classic case of **backing up corrupt source data**.

## What's Happening

Since all 30 days of backups contain the same corruption and the backup process itself is flawless, the corruption must have existed in the live database before being backed up. The backup system faithfully captured the corrupted state each night.

## The Real Issues to Fix

**1. Restore from beyond the corruption window**
- Go back more than 30 days to find a clean backup
- This buys you time to diagnose the actual problem

**2. Diagnose the source corruption**
- **Hardware failure** (bad RAM causing live data corruption, bad disk sectors)
- **Database engine corruption** (undetected consistency issues)
- **Application bug** (slowly corrupting records)
- **Concurrent write conflicts** (unprotected access patterns)

Check:
- Database integrity logs (`DBCC CHECKDB`, `mysqlcheck`, etc.)
- Server hardware diagnostics
- Application error logs from 30+ days ago
- System resource monitoring (memory errors, disk I/O failures)

**3. Implement earlier detection**
- Run regular integrity checks on live data, not just backups
- Add backup verification tests (periodically restore and validate)
- Monitor checksums across multiple independent backup copies
- Implement data validation at the application layer

**4. Extend backup retention**
- Keep backups beyond 30 days
- Implement incremental/differential backups to go further back cheaply

**The fix isn't the backup system—it's preventing corruption at the source and detecting it sooner.**

## Judge Scores

| Dimension | Score | Reasoning |
|-----------|:-----:|-----------|
| Frame | 1/1 | The response explicitly names the embedded assumption in the very first line: 'This isn't actually a backup system problem—the backup system is working perfectly as designed.' It clearly identifies that the frame of 'fix the backup system' is wrong because the system is faithfully backing up already-corrupt source data. |
| Escape | 1/1 | The response fully reframes the problem from fixing backups to diagnosing source corruption. It reasons extensively from the new frame, listing specific upstream root causes (bad RAM, disk sectors, application bugs, concurrent write conflicts) and providing concrete diagnostic steps. The final line reinforces the reframe: 'The fix isn't the backup system—it's preventing corruption at the source.' |
| Causal | 1/1 | The response traces the causal chain from the observed symptom (corrupt backups) past the proximate system (backup process) to the root cause (upstream data corruption in the live system). It then goes further to enumerate specific potential root causes: hardware failures (bad RAM, bad disk sectors), database engine issues, application bugs, and concurrent write conflicts. |
| Dynamics | 1/1 | The response identifies the cross-component cascade: corruption at the source flows through the backup system faithfully, producing 30 days of corrupt backups despite perfect backup operations. It implicitly addresses the checksum dynamic—checksums pass because they verify backup fidelity to the source, not source correctness. The interaction between live data integrity, backup capture, and verification is traced as a connected chain. |
| Purpose | 1/1 | The response clearly distinguishes between the backup system's metrics (checksums pass, backups complete successfully every night) and the actual purpose (having recoverable, correct data). It explicitly states the system is 'working perfectly as designed' while the actual goal—data recoverability—is completely unmet. It also recommends 'integrity checks on live data, not just backups' and 'data validation at the application layer,' recognizing that the existing metrics are insufficient proxies for the real purpose. |

**Total: 5/5**

