"""
CNS Lab 5: Simulation of Access Control Matrix and Illustration of User Updates Access Rights
Aim: To simulate an Access Control Matrix, demonstrate granting and revoking user access rights,
and analyze the performance of the access-control system by varying input size.
"""

import time
import random
import os
import matplotlib.pyplot as plt

# Ensure images directory exists
OUTPUT_IMG_DIR = os.path.join(os.path.dirname(__file__), "lab5_graphs")
os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

PERMISSIONS = ['R', 'W', 'X', 'D']
PERMISSION_DESC = {
    'R': 'Read',
    'W': 'Write',
    'X': 'Execute',
    'D': 'Delete'
}

class AccessControlMatrix:
    def __init__(self, num_users, num_resources, density=0.5, seed=42):
        self.num_users = num_users
        self.num_resources = num_resources
        self.users = [f"User_{i+1}" for i in range(num_users)]
        self.resources = [f"Res_{j+1}" for j in range(num_resources)]
        self.matrix = {}
        self.density = density
        if seed is not None:
            random.seed(seed)
        self._build_matrix()

    def _build_matrix(self):
        for u in self.users:
            self.matrix[u] = {}
            for r in self.resources:
                # Decide if this cell has permissions based on density
                if random.random() < self.density:
                    # Random subset of permissions
                    num_perms = random.randint(1, len(PERMISSIONS))
                    self.matrix[u][r] = set(random.sample(PERMISSIONS, num_perms))
                else:
                    self.matrix[u][r] = set()

    def check_access(self, user, resource, operation):
        if user not in self.matrix:
            return False, f"User {user} not found"
        if resource not in self.matrix[user]:
            return False, f"Resource {resource} not found"
        
        is_allowed = operation in self.matrix[user][resource]
        return is_allowed, f"{'GRANTED' if is_allowed else 'DENIED'}"

    def grant_permission(self, user, resource, operation):
        if user in self.matrix and resource in self.matrix[user]:
            self.matrix[user][resource].add(operation)
            return True
        return False

    def revoke_permission(self, user, resource, operation):
        if user in self.matrix and resource in self.matrix[user]:
            self.matrix[user][resource].discard(operation)
            return True
        return False

    def display(self, max_u=5, max_r=5):
        users_to_show = self.users[:max_u]
        res_to_show = self.resources[:max_r]
        header = f"{'User':<12}" + "".join([f"{r:<14}" for r in res_to_show])
        print(header)
        print("-" * len(header))
        for u in users_to_show:
            row_str = f"{u:<12}"
            for r in res_to_show:
                perms = "".join(sorted(list(self.matrix[u][r]))) if self.matrix[u][r] else "-"
                row_str += f"{perms:<14}"
            print(row_str)
        if len(self.users) > max_u or len(self.resources) > max_r:
            print(f"... [Truncated view: showing {len(users_to_show)}/{len(self.users)} users, {len(res_to_show)}/{len(self.resources)} resources]")


def run_experiment_suite():
    print("=" * 75)
    print("CNS LAB 5 - ACCESS CONTROL MATRIX SIMULATION & BENCHMARKING")
    print("=" * 75)

    test_configs = [
        {"name": "Test 1", "users": 5, "resources": 5, "requests": 10, "updates": 5},
        {"name": "Test 2", "users": 10, "resources": 10, "requests": 15, "updates": 10},
        {"name": "Test 3", "users": 15, "resources": 15, "requests": 20, "updates": 15},
        {"name": "Test 4", "users": 20, "resources": 20, "requests": 30, "updates": 20},
        {"name": "Test 5", "users": 50, "resources": 50, "requests": 40, "updates": 25},
    ]

    results = []

    for cfg in test_configs:
        u_cnt = cfg["users"]
        r_cnt = cfg["resources"]
        req_cnt = cfg["requests"]
        upd_cnt = cfg["updates"]

        # 1. Measure Matrix Creation Time
        # Repeat multiple runs for statistical accuracy
        runs = 200
        t0 = time.perf_counter_ns()
        for _ in range(runs):
            acm = AccessControlMatrix(u_cnt, r_cnt, density=0.5, seed=None)
        t1 = time.perf_counter_ns()
        creation_time_ms = ((t1 - t0) / runs) / 1_000_000.0

        # Create primary ACM instance for verification & update tests
        acm = AccessControlMatrix(u_cnt, r_cnt, density=0.5, seed=42)

        # Generate sample requests
        requests = []
        for _ in range(req_cnt):
            u = random.choice(acm.users)
            r = random.choice(acm.resources)
            op = random.choice(PERMISSIONS)
            requests.append((u, r, op))

        # 2. Measure Access Verification Time
        granted_count = 0
        denied_count = 0
        t0 = time.perf_counter_ns()
        for _ in range(runs):
            g_cnt = 0
            d_cnt = 0
            for u, r, op in requests:
                allowed, _ = acm.check_access(u, r, op)
                if allowed:
                    g_cnt += 1
                else:
                    d_cnt += 1
            granted_count = g_cnt
            denied_count = d_cnt
        t1 = time.perf_counter_ns()
        verification_time_ms = ((t1 - t0) / runs) / 1_000_000.0

        # Generate sample updates (grant/revoke)
        updates = []
        for i in range(upd_cnt):
            u = random.choice(acm.users)
            r = random.choice(acm.resources)
            op = random.choice(PERMISSIONS)
            action = 'GRANT' if i % 2 == 0 else 'REVOKE'
            updates.append((action, u, r, op))

        # 3. Measure Update Time
        t0 = time.perf_counter_ns()
        for _ in range(runs):
            for action, u, r, op in updates:
                if action == 'GRANT':
                    acm.grant_permission(u, r, op)
                else:
                    acm.revoke_permission(u, r, op)
        t1 = time.perf_counter_ns()
        update_time_ms = ((t1 - t0) / runs) / 1_000_000.0

        total_exec_time_ms = creation_time_ms + verification_time_ms + update_time_ms

        results.append({
            "name": cfg["name"],
            "users": u_cnt,
            "resources": r_cnt,
            "requests": req_cnt,
            "updates": upd_cnt,
            "creation_time_ms": round(creation_time_ms, 4),
            "verification_time_ms": round(verification_time_ms, 4),
            "update_time_ms": round(update_time_ms, 4),
            "total_time_ms": round(total_exec_time_ms, 4),
            "granted": granted_count,
            "denied": denied_count
        })

    # Print Table 1
    print("\n--- PERFORMANCE EXPERIMENT TABLE (Actual Measured Values) ---")
    print(f"{'Input Size':<25} | {'Matrix Creation (ms)':<20} | {'Verification (ms)':<18} | {'Update (ms)':<12} | {'Total Time (ms)':<15}")
    print("-" * 100)
    for r in results:
        size_label = f"{r['users']} users / {r['resources']} res ({r['name']})"
        print(f"{size_label:<25} | {r['creation_time_ms']:<20.4f} | {r['verification_time_ms']:<18.4f} | {r['update_time_ms']:<12.4f} | {r['total_time_ms']:<15.4f}")

    # Additional Experiment: Permission Density
    print("\n--- ADDITIONAL EXPERIMENT: PERMISSION DENSITY (50 users / 50 resources) ---")
    densities = [0.10, 0.25, 0.50, 0.75, 1.00]
    density_results = []
    fixed_u = 50
    fixed_r = 50
    fixed_requests = [(f"User_{random.randint(1, fixed_u)}", f"Res_{random.randint(1, fixed_r)}", random.choice(PERMISSIONS)) for _ in range(50)]

    for d in densities:
        # Measure processing time (matrix creation + 50 verifications)
        runs = 100
        t0 = time.perf_counter_ns()
        for _ in range(runs):
            acm_d = AccessControlMatrix(fixed_u, fixed_r, density=d, seed=None)
            for u, res, op in fixed_requests:
                acm_d.check_access(u, res, op)
        t1 = time.perf_counter_ns()
        density_proc_time_ms = ((t1 - t0) / runs) / 1_000_000.0
        density_results.append({
            "density_pct": int(d * 100),
            "processing_time_ms": round(density_proc_time_ms, 4)
        })

    print(f"{'Permission Density':<20} | {'Processing Time (ms)':<20}")
    print("-" * 45)
    for dr in density_results:
        print(f"{str(dr['density_pct']) + '%':<20} | {dr['processing_time_ms']:<20.4f}")

    # Small & Large Demonstration
    print("\n" + "=" * 75)
    print("DETAILED DEMONSTRATION 1: SMALL INPUT (5 Users, 5 Resources)")
    print("=" * 75)
    demo_acm = AccessControlMatrix(5, 5, density=0.5, seed=101)
    print("\n[Initial Access Control Matrix]:")
    demo_acm.display(5, 5)

    print("\n[Access Requests & Verification]:")
    test_reqs = [
        ("User_1", "Res_1", "R"),
        ("User_1", "Res_2", "W"),
        ("User_2", "Res_3", "X"),
        ("User_3", "Res_1", "D"),
        ("User_4", "Res_5", "W")
    ]
    for u, res, op in test_reqs:
        allowed, status = demo_acm.check_access(u, res, op)
        print(f"Request: User '{u}' requests '{PERMISSION_DESC[op]} ({op})' on '{res}' -> Result: {status}")

    print("\n[Dynamic Access Updates]:")
    print("1. Granting 'W' (Write) and 'D' (Delete) to User_1 on Res_2...")
    demo_acm.grant_permission("User_1", "Res_2", "W")
    demo_acm.grant_permission("User_1", "Res_2", "D")
    allowed, status = demo_acm.check_access("User_1", "Res_2", "W")
    print(f"   -> Verifying User_1 on Res_2 for 'Write': {status}")
    allowed, status = demo_acm.check_access("User_1", "Res_2", "D")
    print(f"   -> Verifying User_1 on Res_2 for 'Delete': {status}")

    print("2. Revoking 'W' (Write) from User_1 on Res_2...")
    demo_acm.revoke_permission("User_1", "Res_2", "W")
    allowed, status = demo_acm.check_access("User_1", "Res_2", "W")
    print(f"   -> Verifying User_1 on Res_2 for 'Write' after revocation: {status}")

    print("\n[Updated Access Control Matrix]:")
    demo_acm.display(5, 5)

    # Plot Graphs
    plot_graphs(results, density_results)

    return results, density_results


def plot_graphs(results, density_results):
    users = [r["users"] for r in results]
    requests = [r["requests"] for r in results]
    updates = [r["updates"] for r in results]
    creation_times = [r["creation_time_ms"] for r in results]
    verification_times = [r["verification_time_ms"] for r in results]
    update_times = [r["update_time_ms"] for r in results]
    total_times = [r["total_time_ms"] for r in results]
    granted = [r["granted"] for r in results]
    denied = [r["denied"] for r in results]
    test_names = [r["name"] for r in results]

    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

    # Graph 1: Number of Users vs Execution Time
    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(users, total_times, marker='o', linewidth=2.2, color='#1f77b4', label='Total Execution Time (ms)')
    plt.plot(users, creation_times, marker='s', linewidth=1.8, linestyle='--', color='#ff7f0e', label='Matrix Creation Time (ms)')
    plt.title("Graph 1: Number of Users vs Execution Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Number of Users (Matrix Dimension)", fontsize=11, labelpad=8)
    plt.ylabel("Execution Time (ms)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(frameon=True)
    plt.tight_layout()
    g1_path = os.path.join(OUTPUT_IMG_DIR, "lab5_graph1_users_vs_time.png")
    plt.savefig(g1_path)
    plt.close()
    print(f"Saved: {g1_path}")

    # Graph 2: Number of Access Requests vs Verification Time
    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(requests, verification_times, marker='^', linewidth=2.2, color='#2ca02c', label='Verification Time (ms)')
    plt.title("Graph 2: Number of Access Requests vs Verification Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Number of Access Requests", fontsize=11, labelpad=8)
    plt.ylabel("Verification Time (ms)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(frameon=True)
    plt.tight_layout()
    g2_path = os.path.join(OUTPUT_IMG_DIR, "lab5_graph2_requests_vs_verification.png")
    plt.savefig(g2_path)
    plt.close()
    print(f"Saved: {g2_path}")

    # Graph 3: Number of Access Updates vs Update Time
    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(updates, update_times, marker='d', linewidth=2.2, color='#d62728', label='Update Time (ms)')
    plt.title("Graph 3: Number of Access Updates vs Update Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Number of Access Updates (Grant / Revoke)", fontsize=11, labelpad=8)
    plt.ylabel("Update Time (ms)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(frameon=True)
    plt.tight_layout()
    g3_path = os.path.join(OUTPUT_IMG_DIR, "lab5_graph3_updates_vs_time.png")
    plt.savefig(g3_path)
    plt.close()
    print(f"Saved: {g3_path}")

    # Graph 4: Permission Density vs Processing Time
    dens_pct = [dr["density_pct"] for dr in density_results]
    dens_time = [dr["processing_time_ms"] for dr in density_results]
    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(dens_pct, dens_time, marker='o', linewidth=2.2, color='#9467bd', label='Processing Time (ms)')
    plt.title("Graph 4: Permission Density vs Processing Time (50 Users / 50 Resources)", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Permission Density (%)", fontsize=11, labelpad=8)
    plt.ylabel("Processing Time (ms)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(frameon=True)
    plt.tight_layout()
    g4_path = os.path.join(OUTPUT_IMG_DIR, "lab5_graph4_density_vs_processing.png")
    plt.savefig(g4_path)
    plt.close()
    print(f"Saved: {g4_path}")

    # Graph 5: Granted Requests vs Denied Requests
    plt.figure(figsize=(8, 5), dpi=300)
    x = range(len(test_names))
    width = 0.35
    plt.bar([p - width/2 for p in x], granted, width=width, label='Granted Requests', color='#17becf', edgecolor='black', alpha=0.85)
    plt.bar([p + width/2 for p in x], denied, width=width, label='Denied Requests', color='#e377c2', edgecolor='black', alpha=0.85)
    plt.title("Graph 5: Granted Requests vs Denied Requests Across Tests", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Experiment Runs", fontsize=11, labelpad=8)
    plt.ylabel("Number of Requests", fontsize=11, labelpad=8)
    plt.xticks(x, [f"{t}\n({r['requests']} reqs)" for t, r in zip(test_names, results)])
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    plt.legend(frameon=True)
    plt.tight_layout()
    g5_path = os.path.join(OUTPUT_IMG_DIR, "lab5_graph5_granted_vs_denied.png")
    plt.savefig(g5_path)
    plt.close()
    print(f"Saved: {g5_path}")


if __name__ == "__main__":
    run_experiment_suite()
