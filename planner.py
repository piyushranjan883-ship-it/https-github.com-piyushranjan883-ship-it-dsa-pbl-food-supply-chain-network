"""Unit 3 and 4 - LCS, 0/1 knapsack and sum of subsets (backtracking)."""


def lcs_length(a, b):
    """Unit 3 - longest common subsequence length with a DP table."""
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[len(a)][len(b)]


def lcs_similarity(a, b):
    """Similarity in percent (spaces and capitals ignored)."""
    a = "".join(a.lower().split())
    b = "".join(b.lower().split())
    if not a or not b:
        return 0.0
    return 100.0 * lcs_length(a, b) / max(len(a), len(b))


def knapsack(items, limit):
    """Unit 3 - 0/1 knapsack. items = [(name, kg, value)].
    Returns (best_value, chosen_names)."""
    n = len(items)
    dp = [[0] * (limit + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, wt, val = items[i - 1]
        for w in range(limit + 1):
            dp[i][w] = dp[i - 1][w]
            if wt <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - wt] + val)
    chosen, w = [], limit
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(items[i - 1][0])
            w -= items[i - 1][1]
    return dp[n][limit], chosen[::-1]


def sum_of_subsets(items, target):
    """Unit 4 - backtracking. items = [(name, kg)].
    Returns every list of names whose weights add up to exactly target."""
    answers = []

    def go(index, chosen, total):
        if total == target:
            answers.append(list(chosen))
            return
        if index == len(items) or total > target:
            return                      # wrong path, go back
        chosen.append(items[index][0])
        go(index + 1, chosen, total + items[index][1])
        chosen.pop()                    # undo (backtrack)
        go(index + 1, chosen, total)

    go(0, [], 0)
    return answers
