# RLS Context Inspection Report
**Date:** nt.times_result(user=0.265625, system=0.046875, children_user=0.0, children_system=0.0, elapsed=0.0)

## 1. Database Configuration Check
| Table | RLS Enabled | Policies |
| :--- | :---: | :--- |
| `orders` | ✅ True | `tenant_isolation_policy` |
| `products` | ✅ True | `tenant_isolation_policy` |
| `companies` | ✅ True | `tenant_isolation_policy` |

## 2. Session Context Analysis
- **Initial Context:** `` (Expected: None/Null)
- **Context After Set:** `00000000-0000-0000-0000-000000000000`

### ✅ Context Propagation: SUCCESS